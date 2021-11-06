from pygame import __version__ as pg_ver

from .errorhandler import *

from .ai import *
from .animation import *
from .bossbar import *
from .button import *
from .entity import *
from .math import *
from .object import *
from .particles import *
from .replay import *
from .text import *
from .tilemap import *
from .time import *
from .world import *

def init(pixels_per_unit=8, tps=16):
    global PIXELS_PER_UNIT
    global TICKS_PER_SECOND

    PIXELS_PER_UNIT = pixels_per_unit
    TICKS_PER_SECOND = tps

__version__ = "1.0"
print(f"running sakuya {__version__} by novial (using pygame {pg_ver})\nsource code: https://github.com/novialriptide/Sakuya")