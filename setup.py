from distutils.core import setup

from SakuyaEngine.__version__ import GAME_VERSION

setup(
    name="SakuyaEngine",
    author="Andrew Hong",
    author_email="novialriptide@gmail.com",
    url="https://github.com/novialriptide/SakuyaEngine",
    packages=["SakuyaEngine"],
    version=str(GAME_VERSION),
)
