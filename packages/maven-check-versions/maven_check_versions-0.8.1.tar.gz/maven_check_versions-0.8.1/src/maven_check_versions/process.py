#!/usr/bin/python3
"""This file provides process functions"""

import logging
import os
import threading
# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

import maven_check_versions.cache as _cache
import maven_check_versions.config as _config
import maven_check_versions.cveutils as _cveutils
import maven_check_versions.logutils as _logutils
import maven_check_versions.utils as _utils
import requests
import urllib3
from bs4 import BeautifulSoup
from maven_check_versions.config import Config, Arguments
from maven_check_versions.cveutils import Vulnerability

process_dependency_lock = threading.Lock()


def process_main(arguments: Arguments) -> None:
    """
    Orchestrates the main processing logic for checking Maven dependencies.

    Args:
        arguments (Arguments): Command-line arguments.
                May specify 'pom_file', 'find_artifact', or rely on config for POM files.
    """
    config = _config.get_config(arguments)

    if not _config.get_config_value(config, arguments, 'warnings', 'urllib3'):
        urllib3.disable_warnings()

    cache_disabled = _config.get_config_value(config, arguments, 'cache_off', default=False)
    cache_data = _cache.load_cache(config, arguments) if not cache_disabled else None

    if pom_file := arguments.get('pom_file'):
        process_pom(cache_data, config, arguments, pom_file)
    elif artifact_to_find := arguments.get('find_artifact'):
        process_artifact(cache_data, config, arguments, artifact_to_find)
    else:
        for _, pom in _config.config_items(config, 'pom_files'):
            process_pom(cache_data, config, arguments, pom)

    _cache.save_cache(config, arguments, cache_data)


def process_pom(
        cache_data: Optional[dict], config: Config, arguments: Arguments,
        pom_path: str, prefix: Optional[str] = None
) -> None:
    """
    Processes a single POM file by extracting dependencies, checking versions,
    and optionally processing modules and vulnerabilities.

    Args:
        cache_data (Optional[dict]): Cache data.
        config (Config): Parsed YAML as dict.
        arguments (Arguments): Command-line arguments.
        pom_path (str): Local path or URL to the POM file to process.
        prefix (str, optional): Prefix to prepend to the artifact name in logs (default is None).
    """
    verify_ssl = _config.get_config_value(config, arguments, 'verify', 'requests', default=True)

    tree = _utils.get_pom_tree(pom_path, verify_ssl, config, arguments)
    root = tree.getroot()
    ns_mapping = {'xmlns': 'http://maven.apache.org/POM/4.0.0'}  # NOSONAR

    artifact_name = _utils.get_artifact_name(root, ns_mapping)
    if prefix is not None:
        artifact_name = f"{prefix} / {artifact_name}"
    logging.info(f"=== Processing: {artifact_name} ===")

    dependencies = _utils.collect_dependencies(root, ns_mapping, config, arguments)

    cve_data = _cveutils.get_cve_data(config, arguments, dependencies, root, ns_mapping)

    if _config.get_config_value(config, arguments, 'threading', default=True):
        max_threads = _config.get_config_value(config, arguments, 'max_threads')

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            for future in as_completed([
                executor.submit(process_dependency,
                                cache_data, config, arguments, dep, ns_mapping, root, verify_ssl, cve_data)
                for dep in dependencies
            ]):
                try:
                    future.result()
                except Exception as e:  # pragma: no cover
                    logging.error(f"Error processing dependency: {e}")
    else:
        for dep in dependencies:
            process_dependency(cache_data, config, arguments, dep, ns_mapping, root, verify_ssl, cve_data)

    process_modules_if_required(cache_data, config, arguments, root, pom_path, ns_mapping, artifact_name)


def process_dependency(
        cache_data: Optional[dict], config: Config, arguments: Arguments, dependency: ET.Element, ns_mapping: dict,
        root: ET.Element, verify_ssl: bool, cve_data: Optional[dict[str, list[Vulnerability]]] = None
) -> None:
    """
    Processes dependency in a POM file.

    Args:
        cache_data (Optional[dict]): Cache dictionary for storing dependency data, or None if disabled.
        config (Config): Configuration dictionary parsed from YAML.
        arguments (Arguments): Command-line arguments.
        dependency (ET.Element): Dependency.
        ns_mapping (dict): XML namespace mapping.
        root (ET.Element): Root element of the POM file.
        verify_ssl (bool): SSL verification flag.
        cve_data (dict[str, list[Vulnerability]]): CVE Data.
    """
    group, artifact = _utils.get_dependency_identifiers(dependency, ns_mapping)
    if not artifact or not group:
        logging.error("Missing artifactId or groupId in a dependency.")
        return

    version, skip_flag = _utils.get_version(config, arguments, ns_mapping, root, dependency)
    if skip_flag is True:
        _logutils.log_skip_if_required(config, arguments, group, artifact, version)
        return

    with process_dependency_lock:
        _logutils.log_search_if_required(config, arguments, group, artifact, version)

        processed = False
        if cache_data is not None and cache_data.get(f"{group}:{artifact}") is not None and \
                _cache.process_cache_artifact(config, arguments, cache_data, artifact, group, version):
            processed = True

        if not processed and \
                not process_repositories(artifact, cache_data, config, group, arguments, verify_ssl, version):
            logging.warning(f"Not Found: {group}:{artifact}:{version}")

        _cveutils.log_vulnerability(config, arguments, group, artifact, version, cve_data)


def process_repositories(
        artifact: str, cache_data: Optional[dict], config: Config, group: str,
        arguments: Arguments, verify_ssl: bool, version: Optional[str]
):
    """
    Processes repositories to find a dependency.

    Args:
        artifact (str): Artifact ID.
        cache_data (Optional[dict]): Cache data.
        config (Config): Parsed YAML as dict.
        group (str): Group ID.
        arguments (Arguments): Command-line arguments.
        verify_ssl (bool): SSL verification flag.
        version (Optional[str]): Dependency version.

    Returns:
        bool: True if the dependency is found, False otherwise.
    """
    if len(items := _config.config_items(config, 'repositories')):
        for repository_key in items:
            if (process_repository(
                    cache_data, config, arguments, group, artifact, version,
                    repository_key, verify_ssl)):
                return True
    return False


def process_modules_if_required(
        cache_data: Optional[dict], config: Config, arguments: Arguments, root: ET.Element,
        pom_path: str, ns_mapping: dict, prefix: Optional[str] = None
) -> None:
    """
    Processes modules in a POM file if required.

    Args:
        cache_data (Optional[dict]): Cache data.
        config (Config): Parsed YAML as dict.
        arguments (Arguments): Command-line arguments.
        root (ET.Element): Root element of the POM file.
        pom_path (str): Path to the POM file.
        ns_mapping (dict): XML namespace mapping.
        prefix (str, optional): Prefix for the artifact name.
    """
    if _config.get_config_value(config, arguments, 'process_modules', default=False):
        directory_path = os.path.dirname(pom_path)
        modules = root.findall('.//xmlns:modules/xmlns:module', namespaces=ns_mapping)
        module_paths = [f"{directory_path}/{module.text}/pom.xml" for module in modules]
        valid_module_paths = [p for p in module_paths if p.startswith('http') or os.path.exists(p)]

        if _config.get_config_value(config, arguments, 'threading', default=True):
            max_threads = _config.get_config_value(config, arguments, 'max_threads', default=8)
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                for future in as_completed([
                    executor.submit(process_pom, cache_data, config, arguments, module_path, prefix)
                    for module_path in valid_module_paths
                ]):
                    try:
                        future.result()
                    except Exception as e:  # pragma: no cover
                        logging.error(f"Error processing module: {e}")
        else:
            for module_path in valid_module_paths:
                process_pom(cache_data, config, arguments, module_path, prefix)


def process_artifact(
        cache_data: Optional[dict], config: Config, arguments: Arguments,
        artifact_to_find: str
) -> None:
    """
    Processes the search for a specified artifact.

    Args:
        cache_data (Optional[dict]): Cache data.
        config (Config): Parsed YAML as dict.
        arguments (Arguments): Command-line arguments.
        artifact_to_find (str): Artifact to search for in groupId:artifactId:version format.
    """
    verify_ssl = _config.get_config_value(config, arguments, 'verify', 'requests', default=True)
    group, artifact, version = artifact_to_find.split(':', maxsplit=2)

    _logutils.log_search_if_required(config, arguments, group, artifact, version)

    dependency_found = False
    for repository_key in _config.config_items(config, 'repositories'):
        if (dependency_found := process_repository(
                cache_data, config, arguments, group, artifact, version,
                repository_key, verify_ssl)):
            break
    if not dependency_found:
        logging.warning(f"Not Found: {group}:{artifact}, current:{version}")


def process_repository(
        cache_data: Optional[dict], config: Config, arguments: Arguments, group: str, artifact: str,
        version: Optional[str], repository_key: str, verify_ssl: bool
) -> bool:
    """
    Processes a repository section.

    Args:
        cache_data (Optional[dict]): Cache data.
        config (Config): Parsed YAML as dict.
        arguments (Arguments): Command-line arguments.
        group (str): Group ID.
        artifact (str): Artifact ID.
        version (Optional[str]): Artifact version.
        repository_key (str): Repository section key.
        verify_ssl (bool): SSL verification flag.

    Returns:
        bool: True if the dependency is found, False otherwise.
    """
    auth_info: Optional[tuple[str, str]] = None
    if _config.get_config_value(config, arguments, 'auth', repository_key, default=False):
        auth_info = _utils.get_auth_info(arguments, config, repository_key)

    base_url = _config.get_config_value(config, arguments, 'base', repository_key)
    path_suffix = _config.get_config_value(config, arguments, 'path', repository_key)
    repository_name = _config.get_config_value(config, arguments, 'repo', repository_key)

    path = f"{base_url}/{path_suffix}"
    if repository_name is not None:
        path = f"{path}/{repository_name}"
    path = f"{path}/{group.replace('.', '/')}/{artifact}"

    with requests.Session() as session:
        response = session.get(path + '/maven-metadata.xml', auth=auth_info, verify=verify_ssl)

        if response.status_code == 200:
            tree = ET.ElementTree(ET.fromstring(response.text))
            version_elements = tree.getroot().findall('.//version')
            available_versions = [v.text for v in version_elements if v.text]
            available_versions.reverse()

            if _utils.check_versions(
                    cache_data, config, arguments, group, artifact, version, repository_key,
                    path, auth_info, verify_ssl, available_versions, response):
                return True

    if _config.get_config_value(config, arguments, 'service_rest', repository_key, default=False):
        return service_rest(
            cache_data, config, arguments, group, artifact, version,
            repository_key, base_url, auth_info, verify_ssl)

    return False


def service_rest(
        cache_data: Optional[dict], config: Config, arguments: Arguments, group: str, artifact: str,
        version: Optional[str], repository_key: str, base_url: str,
        auth_info: Optional[tuple[str, str]], verify_ssl: bool
) -> bool:
    """
    Processes REST services for a repository.

    Args:
        cache_data (Optional[dict]): Cache data.
        config (Config): Parsed YAML as dict.
        arguments (Arguments): Command-line arguments.
        group (str): Group ID.
        artifact (str): Artifact ID.
        version (Optional[str]): Artifact version.
        repository_key (str): Repository section name.
        base_url (str): Base URL of the repository.
        auth_info (Optional[tuple[str, str]]): Authentication credentials.
        verify_ssl (bool): SSL verification flag.

    Returns:
        bool: True if the dependency is found, False otherwise.
    """
    repo = _config.get_config_value(config, arguments, 'repo', repository_key)
    path = f"{base_url}/service/rest/repository/browse/{repo}"
    path = f"{path}/{group.replace('.', '/')}/{artifact}"

    with requests.Session() as session:
        response = session.get(path + '/maven-metadata.xml', auth=auth_info, verify=verify_ssl)

        if response.status_code == 200:
            tree = ET.ElementTree(ET.fromstring(response.text))
            version_elements = tree.getroot().findall('.//version')
            available_versions = [v.text for v in version_elements if v.text]
            available_versions.reverse()

            if _utils.check_versions(
                    cache_data, config, arguments, group, artifact, version, repository_key,
                    path, auth_info, verify_ssl, available_versions, response):
                return True

        response = session.get(path + '/', auth=auth_info, verify=verify_ssl)

        if response.status_code == 200:
            table = BeautifulSoup(response.text, 'html.parser').find('table')
            if table is None:  # pragma: no cover
                logging.error(f"Failed to parse versions from HTML at {path}")
                return False

            version_links = table.find_all('a')[1:]  # type: ignore
            path = f"{base_url}/repository/{repo}/{group.replace('.', '/')}/{artifact}"
            available_versions = [v.text for v in version_links if v.text]
            available_versions.reverse()

            if _utils.check_versions(
                    cache_data, config, arguments, group, artifact, version, repository_key,
                    path, auth_info, verify_ssl, available_versions, response):
                return True

    return False
