from pygame import __version__ as pg_ver

from .animation import *
from .entity import *
from .math import *
from .object import *
from .particles import *
from .text import *
from .tilemap import *
from .time import *
from .vector import *
from .world import *

__version__ = "1.0"
print(f"running sakuya {__version__} (pygame {pg_ver}) by novial\nsource code: https://github.com/novialriptide/Sakuya")