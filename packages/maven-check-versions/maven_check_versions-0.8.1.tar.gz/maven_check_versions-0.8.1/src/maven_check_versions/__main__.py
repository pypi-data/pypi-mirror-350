#!/usr/bin/python3
"""Entry point for running maven_check_versions as a module with 'python -m'."""
import sys

from . import main

if __name__ == "__main__":
    sys.exit(main())
