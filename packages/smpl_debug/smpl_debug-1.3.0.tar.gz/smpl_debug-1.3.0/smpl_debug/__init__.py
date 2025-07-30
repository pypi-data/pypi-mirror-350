"""A collection of simplified utilities."""

from importlib.metadata import version

package = "smpl_debug"

__version__ = version("smpl")
from smpl.debug import *
