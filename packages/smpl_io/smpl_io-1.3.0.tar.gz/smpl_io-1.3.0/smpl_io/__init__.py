"""A collection of simplified utilities."""

from importlib.metadata import version

package = "smpl_io"

__version__ = version("smpl")

from smpl.io import *
