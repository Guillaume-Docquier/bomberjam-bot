import numpy as np

from models.direction import Directions
from collections import deque
from core.logging import log
from models.tile import Tile
from models.position import Position


UNVISITED = -100.0
BAD_SCORE = -1.0
GOOD_SCORE = 1.0


class TileScorer:
    def __init__(self, state, origin, bomb_range, pathfinder, blocking_tiles=None):
        if blocking_tiles is None:
            blocking_tiles = [Tile.WALL, Tile.BLOCK]

        self.pathfinder = pathfinder
        self.bomb_reach_matrix = TileScorer.__compute_bomb_reach_matrix(state)
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
        if max_score <= BAD_SCORE:
            return None

        return [Position(x, y) for [x, y] in np.argwhere(self.score_matrix == max_score)]

    def get_score(self, position):
        return self.score_matrix[position]

    def compute_score(self, state, position, bomb_range):
        if self.bomb_reach_matrix[position]:
            return BAD_SCORE

        score = 0.0
        for direction in Directions.tolist():
            position_to_explore = position

            for _ in range(1, bomb_range + 1):
                position_to_explore = position_to_explore.apply(direction)
                if not state.includes(position_to_explore) or state.tiles[position_to_explore] == Tile.WALL:
                    break

                if state.tiles[position_to_explore] == Tile.BLOCK:
                    if not self.bomb_reach_matrix[position_to_explore]:
                        score += GOOD_SCORE
                    break

        distance_factor = self.pathfinder.get_distance_to(position) * 0.1 + 1.0

        return score / distance_factor

    @staticmethod
    def __compute_bomb_reach_matrix(state):
        bomb_reach_matrix = np.full((state.width, state.height), False)
        for bomb in state.bombs:
            bomb_reach_matrix[bomb.position] = True
            for direction in Directions.tolist():
                position_to_explore = bomb.position

                for _ in range(1, bomb.range + 1):
                    position_to_explore = position_to_explore.apply(direction)
                    if not state.includes(position_to_explore) or state.tiles[position_to_explore] == Tile.WALL:
                        break

                    bomb_reach_matrix[position_to_explore] = True
                    if state.tiles[position_to_explore] == Tile.BLOCK:
                        break

        return bomb_reach_matrix
