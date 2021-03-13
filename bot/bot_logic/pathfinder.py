import numpy as np
import random

from models.direction import Directions
from collections import deque
from core.logging import log
from models.tile import Tile


class Pathfinder:
    def __init__(self, state, origin, blocking_tiles=None):
        if blocking_tiles is None:
            blocking_tiles = [Tile.WALL, Tile.BLOCK]

        self.state = state
        self.distance_matrix = np.full((state.width, state.height), state.width * state.height)

        self.distance_matrix[origin] = 0
        positions_to_explore = deque([origin])

        while len(positions_to_explore) > 0:
            position_to_explore = positions_to_explore.pop()

            for direction in Directions.tolist():
                next_position = position_to_explore.apply(direction)
                next_distance = self.distance_matrix[position_to_explore] + 1

                if state.includes(next_position) and state.tiles[next_position] not in blocking_tiles:
                    if self.distance_matrix[next_position] > next_distance:
                        self.distance_matrix[next_position] = next_distance
                        positions_to_explore.appendleft(next_position)

    def get_distance_to(self, destination):
        return self.distance_matrix[destination]

    def get_closest_position(self, positions):
        shuffled_positions = random.sample(positions, len(positions))
        distances = [self.get_distance_to(position) for position in shuffled_positions]

        return shuffled_positions[np.argmin(distances)]

    def get_path_to(self, destination):
        path = [destination]
        position_to_explore = destination
        distance_left = self.distance_matrix[destination]

        while distance_left > 1:
            neighbours_positions = [position_to_explore.apply(direction) for direction in Directions.tolist()]
            valid_neighbours_positions = [neighbour_position for neighbour_position in neighbours_positions if self.state.includes(neighbour_position)]
            neighbours_distances = [self.distance_matrix[position] for position in valid_neighbours_positions]

            best_neighbour = valid_neighbours_positions[np.argmin(neighbours_distances)]
            path.append(best_neighbour)
            position_to_explore = best_neighbour
            distance_left = self.distance_matrix[best_neighbour]

        path.reverse()

        return path
