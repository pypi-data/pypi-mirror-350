"""
pytadata_entriz ― Uniform DataFrame writer for AWS or GCP back-ends.
"""

from importlib.metadata import version as _v
from .main import Calculator

__all__ = ["Calculator", "__version__"]
__version__: str = _v(__name__)
