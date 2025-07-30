# -*- coding: utf-8 -*-

"""Top-level package for SEAMM_FF_Util."""

from .forcefield import Forcefield  # noqa: F401
from .ff_assigner import FFAssigner, ForcefieldAssignmentError  # noqa: F401
from .tabulate_function import tabulate_angle  # noqa: F401

# Handle versioneer
from ._version import get_versions

__author__ = """Paul Saxe"""
__email__ = "psaxe@molssi.org"
versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
