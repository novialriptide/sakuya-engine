"""
SakuyaEngine (c) 2020-2021 Andrew Hong
This code is licensed under GNU LESSER GENERAL PUBLIC LICENSE (see LICENSE for details)
"""
from .__version__ import GAME_VERSION
from .ai import *
from .bar import *
from .bullets import *
from .camera import *
from .client import *
from .clock import *
from .controllers import *
from .draw import *
from .effect_circle import *
from .effect_rain import *
from .effects import *
from .entity import *
from .errors import *
from .events import *
from .lights import *
from .locals import *
from .math import *
from .scene import *
from .text import *
from .tile import *

from pygame import __version__ as pg_ver



print(
    f"sakuya engine {GAME_VERSION} by novial (using pygame {pg_ver})\nsource code: https://github.com/novialriptide/Sakuya"
)
