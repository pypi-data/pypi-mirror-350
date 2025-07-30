"""A collection of simplified utilities."""

from importlib.metadata import version

package = "smpl_parallel"

__version__ = version("smpl")

from smpl.parallel import *
