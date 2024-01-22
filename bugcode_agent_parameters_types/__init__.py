"""Top-level package for bugcode_agent_parameters_types."""

__author__ = """Bugcode Development Team"""
__email__ = "devel@khulnasoft.com"
__version__ = "1.3.1"

from pathlib import Path
from typing import Union


def manifests_folder() -> Union[Path, str]:
    return Path(__file__).parent / "static" / "manifests"