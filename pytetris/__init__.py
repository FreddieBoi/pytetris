#!/usr/bin/env python
"""
pytetris is a Tetris clone written in python and pygame.
See https://github.com/FreddieBoi/pytetris for more 
information.
"""

__author__ = "Freddie Pettersson <freddieboi@gmail.com>"
__version_info__ = (1, 3, 0)
__version__ = '.'.join(map(str, __version_info__))
__license__ = "Copyriot"
__package__ = "pytetris"

from pytetris.figure import Figure
from pytetris.board import Board
from pytetris.game import Game
from pytetris.main import main, Main

__all__ = ['Figure', 'Board', 'Game', 'Main']

if __name__ == '__main__':
    main()
