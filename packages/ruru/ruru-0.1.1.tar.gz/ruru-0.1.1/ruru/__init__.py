"""
Ruru - A powerful CLI tool for managing and versioning prompts across projects.

Ruru helps developers manage, version, and sync prompt files (like .cursorrules)
across multiple projects with a simple command-line interface.
"""

__version__ = "0.1.0"
__author__ = "Ruru Team"
__email__ = "me@ekkyarmandi.com"
__license__ = "MIT"

from .main import cli

__all__ = ["cli"]
