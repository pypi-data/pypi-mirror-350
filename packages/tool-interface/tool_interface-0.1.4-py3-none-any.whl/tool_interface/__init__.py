"""
tool_interface - Main Python package to access the 3DTrees backend from tool containers
"""

from importlib.metadata import version

try:
    __version__ = version("tool_interface")
except Exception:  # pragma: no cover
    # If the package is not installed, use a default version
    __version__ = "0.0.0"
