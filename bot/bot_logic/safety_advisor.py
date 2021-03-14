import numpy as np

from models.direction import Directions
from models.tile import Tile

from core.logging import log

SAFE = 999


def by_countdown(bomb):
    return bomb.countdown


class SafetyAdvisor:
    def __init__(self, state):
        self.bomb_reach_matrix = np.full(state.bounds.shape, SAFE)

        for bomb in sorted(state.bombs, key=by_countdown):
            effective_bomb_countdown = min(bomb.countdown, self.bomb_reach_matrix[bomb.position])
            self.bomb_reach_matrix[bomb.position] = effective_bomb_countdown

            for direction in Directions.tolist():
                position_to_explore = bomb.position

                for _ in range(1, bomb.range + 1):
                    position_to_explore = position_to_explore.apply(direction)
                    if not state.bounds.contains(position_to_explore) or state.tiles[position_to_explore] == Tile.WALL:
                        break

                    self.bomb_reach_matrix[position_to_explore] = min(effective_bomb_countdown, self.bomb_reach_matrix[position_to_explore])
                    if state.tiles[position_to_explore] == Tile.BLOCK:
                        break

    def is_dangerous(self, position, when=None, wait=0):
        if when is None:
            return self.bomb_reach_matrix[position] != SAFE

        # A tile you're on is dangerous now if its cooldown is 1
        # A tile you're not on is dangerous now if its cooldown is 0
        # This is because bombs explode at the start of the tick, preventing any action for a bot that's in range of a bomb,
        # and the fire lasts the whole tick, burning any bot moving in
        return 0 <= self.bomb_reach_matrix[position] - when <= 1 + wait

    def is_safe(self, position, when=None, wait=0):
        return not self.is_dangerous(position, when, wait)
