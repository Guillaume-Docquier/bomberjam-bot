from collections import namedtuple

from core.enumerable_enum import Enumerable
from models.action import Action


Direction = namedtuple("Direction", ["action", "delta_x", "delta_y"])


class Directions(Enumerable):
    UP = Direction(Action.UP, 0, -1)
    LEFT = Direction(Action.LEFT, -1, 0)
    DOWN = Direction(Action.DOWN, 0, 1)
    RIGHT = Direction(Action.RIGHT, 1, 0)
    STAY = Direction(Action.STAY, 0, 0)
