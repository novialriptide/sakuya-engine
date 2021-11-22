from pygame import __version__ as pg_ver

from .ai import *
from .animation import *
from .bar import *
from .button import *
from .entity import *
from .errors import *
from .math import *
from .physics import *
from .scene import *
from .text import *
from .tilemap import *
from .tileset import *
from .time import *
from .world import *

__version__ = "1.1"
print(f"running sakuya {__version__} by novial (using pygame {pg_ver})\nsource code: https://github.com/novialriptide/Sakuya")