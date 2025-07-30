"""A collection of simplified utilities."""

from importlib.metadata import version

package = "smpl_doc"
__version__ = version("smpl")
from smpl.doc import *
