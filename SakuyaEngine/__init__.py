"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from pygame import __version__ as pg_ver

from .ai import *
from .animation import *
from .bar import *
from .bullets import *
from .button import *
from .entity import *
from .errors import *
from .events import *
from .lights import *
from .math import *
from .effect_fire import *
from .effect_particles import *
from .effect_rain import *
from .effects import *
from .physics import *
from .scene import *
from .text import *
from .tile import *
from .waves import *

__version__ = "2.2.1"
print(
    f"sakuya engine {__version__} by novial (using pygame {pg_ver})\nsource code: https://github.com/novialriptide/Sakuya"
)
