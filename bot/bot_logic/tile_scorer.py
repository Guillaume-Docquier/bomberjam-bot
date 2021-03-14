import numpy as np
from collections import deque

from models.direction import Directions
from models.tile import Tile
from models.position import Position

from core.logging import log

UNVISITED = -99.0
DANGEROUS_SCORE = -1.0
BLOCK_SCORE = 1.0

DISTANCE_IMPORTANCE = 0.1


class TileScorer:
    def __init__(self, state, origin, bomb_range, pathfinder, safety_advisor, blocking_tiles=None):
        if blocking_tiles is None:
            blocking_tiles = [Tile.WALL, Tile.BLOCK]

        self.pathfinder = pathfinder
        self.safety_advisor = safety_advisor
        self.score_matrix = np.full((state.width, state.height), UNVISITED)

        positions_to_explore = deque([origin])

        while len(positions_to_explore) > 0:
            position_to_explore = positions_to_explore.pop()
            self.score_matrix[position_to_explore] = self.compute_score(state, position_to_explore, bomb_range)

            for direction in Directions.tolist():
                next_position = position_to_explore.apply(direction)

                if state.includes(next_position) and state.tiles[next_position] not in blocking_tiles:
                    if self.score_matrix[next_position] == UNVISITED:
                        positions_to_explore.appendleft(next_position)

    def get_best_tiles(self):
        max_score = np.amax(self.score_matrix)
        if max_score <= DANGEROUS_SCORE:
            return None

        return [Position(x, y) for [x, y] in np.argwhere(self.score_matrix == max_score)]

    def get_score(self, position):
        return self.score_matrix[position]

    def compute_score(self, state, position, bomb_range):
        distance = self.pathfinder.get_distance_to(position)
        if self.safety_advisor.is_dangerous(position, when=distance, wait=max(0, state.current_player.next_bomb_in - distance)):
            return DANGEROUS_SCORE

        score = 0.0
        for direction in Directions.tolist():
            position_to_explore = position

            for _ in range(1, bomb_range + 1):
                position_to_explore = position_to_explore.apply(direction)
                if not state.includes(position_to_explore) or state.tiles[position_to_explore] == Tile.WALL:
                    break

                if state.tiles[position_to_explore] == Tile.BLOCK:
                    if self.safety_advisor.is_safe(position_to_explore):
                        score += BLOCK_SCORE
                    break

        distance_factor = 1.0 + distance * DISTANCE_IMPORTANCE

        return score / distance_factor
