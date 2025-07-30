"""A collection of simplified utilities."""

from importlib.metadata import version

package = "smpl_animation"

__version__ = version("smpl")
from smpl.animation import *
