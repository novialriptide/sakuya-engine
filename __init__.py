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
from .tile import *
from .time import *

__version__ = "2.0.1"
print(f"sakuya engine {__version__} by novial (using pygame {pg_ver})\nsource code: https://github.com/novialriptide/Sakuya")