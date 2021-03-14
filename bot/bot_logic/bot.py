import random

from models.action import Action
from .safety_advisor import SafetyAdvisor
from .pathfinder import Pathfinder
from .tile_scorer import TileScorer

from core.logging import log

I_JUST_DIED = 10


class Bot:
    """
    Your Bomberjam bot.
    NAME should be your bot name. It cannot contain spaces or special characters.
    compute_next_action(state) should return an Action given a state.
    You can also add anything you need!
    """
    NAME = f"Guid{random.randint(0, 10000)}"

    def __init__(self, bot_id):
        self.bot_id = bot_id
        self.deaths = 0

    def compute_next_action(self, state):
        """
        Computes the next action your bot should do based on the current game state.

        :param state: The current game state
        :return: Action
        """
        my_player = state.current_player

        if my_player.respawning == I_JUST_DIED:
            self.deaths += 1

        safety_advisor = SafetyAdvisor(state)
        pathfinder = Pathfinder(state, my_player.position, safety_advisor)
        tile_scorer = TileScorer(state, my_player.position, my_player.bomb_range, pathfinder, safety_advisor)

        log(f"\n{safety_advisor.bomb_reach_matrix.transpose()}")
        log(f"\n{pathfinder.distance_matrix.transpose()}")
        log(f"\n{tile_scorer.score_matrix.transpose()}")

        best_tile_positions = tile_scorer.get_best_tiles()
        if best_tile_positions is None:
            return Action.STAY

        best_tile_position = pathfinder.get_closest_position(best_tile_positions)
        log(f"Best position: {best_tile_position} with score {tile_scorer.get_score(best_tile_position)}")
        if best_tile_position == my_player.position:
            return Action.BOMB

        path_to_best_tile = pathfinder.get_path_to(best_tile_position)
        if path_to_best_tile is None:
            return Action.STAY

        direction = my_player.position.get_direction_to(path_to_best_tile[0])

        return direction.action
