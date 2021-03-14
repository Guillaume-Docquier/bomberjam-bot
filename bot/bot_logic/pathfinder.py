import numpy as np
import random
from collections import deque

from models.direction import Directions
from models.tile import Tile

from core.logging import log

DISTANCE_PENALTY_FOR_PLAYER = 2


class Pathfinder:
    def __init__(self, state, origin, safety_advisor, blocking_tiles=None):
        if blocking_tiles is None:
            blocking_tiles = [Tile.WALL, Tile.BLOCK]

        self.state = state
        self.max_distance = state.width * state.height
        self.safety_advisor = safety_advisor
        self.distance_matrix = np.full((state.width, state.height), self.max_distance)

        self.distance_matrix[origin] = 0

        positions_to_explore = deque([origin])
        while len(positions_to_explore) > 0:
            position_to_explore = positions_to_explore.pop()

            for direction in Directions.tolist():
                next_position = position_to_explore.apply(direction)
                next_distance = self.distance_matrix[position_to_explore] + 1

                if state.includes(next_position) and state.tiles[next_position] not in blocking_tiles:
                    bomb_at_next_position = next((bomb for bomb in state.bombs if bomb.position == next_position), None)
                    if bomb_at_next_position:
                        next_distance += bomb_at_next_position.countdown
                    else:
                        player_at_next_position = next((player for player in state.other_players if player.position == next_position), None)
                        if player_at_next_position:
                            next_distance += DISTANCE_PENALTY_FOR_PLAYER

                    if self.distance_matrix[next_position] > next_distance and self.safety_advisor.is_safe(next_position, next_distance):
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
        if distance_left == self.max_distance:
            return None

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
