import numpy as np

from models.direction import Directions
from collections import deque
from core.logging import log
from models.tile import Tile
from models.position import Position


class TileScorer:
    def __init__(self, state, origin, bomb_range, blocking_tiles=None):
        if blocking_tiles is None:
            blocking_tiles = [Tile.WALL, Tile.BLOCK]

        self.score_matrix = np.full((state.width, state.height), -1)

        positions_to_explore = deque([origin])

        while len(positions_to_explore) > 0:
            position_to_explore = positions_to_explore.pop()
            self.score_matrix[position_to_explore] = TileScorer.get_score(state, position_to_explore, bomb_range)

            for direction in Directions.tolist():
                next_position = position_to_explore.apply(direction)

                if state.includes(next_position) and state.tiles[next_position] not in blocking_tiles:
                    if self.score_matrix[next_position] < 0:
                        positions_to_explore.appendleft(next_position)

        log(f"\n{self.score_matrix.transpose()}")

    def get_best_tiles(self):
        max_score = np.amax(self.score_matrix)
        if max_score < 1:
            return None

        return [Position(x, y) for [x, y] in np.argwhere(self.score_matrix == max_score)]

    @staticmethod
    def get_score(state, position, bomb_range):
        bomb_positions = [bomb.position for bomb in state.bombs]
        if position in bomb_positions:
            return 0

        score = 0
        for direction in Directions.tolist():
            position_to_explore = position

            for _ in range(1, bomb_range + 1):
                position_to_explore = position_to_explore.apply(direction)
                if not state.includes(position_to_explore) or state.tiles[position_to_explore] == Tile.WALL:
                    break

                if state.tiles[position_to_explore] == Tile.BLOCK:
                    score += 1
                    break

        return score
