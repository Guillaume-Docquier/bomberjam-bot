from collections import namedtuple

from core.logging import log
from .direction import Directions

PositionNT = namedtuple("Position", ["x", "y"])


class Position(PositionNT):
    def apply(self, direction):
        return Position(self.x + direction.delta_x, self.y + direction.delta_y)

    def get_direction_to(self, position):
        delta_x = position.x - self.x
        if delta_x > 1:
            delta_x = delta_x / abs(delta_x)

        delta_y = position.y - self.y
        if delta_y > 1:
            delta_y = delta_y / abs(delta_y)

        return next(direction for direction in Directions.tolist() if direction.delta_x == delta_x and direction.delta_y == delta_y)
