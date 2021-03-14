import random

from models.action import Action
from .safety_advisor import SafetyAdvisor
from .pathfinder import Pathfinder
from .tile_scorer import TileScorer

from core.logging import log


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

    def compute_next_action(self, state):
        """
        Computes the next action your bot should do based on the current game state.

        :param state: The current game state
        :return: Action
        """
        my_player = state.current_player
        safety_advisor = SafetyAdvisor(state)
        pathfinder = Pathfinder(state, my_player.position, safety_advisor)
        tile_scorer = TileScorer(state, my_player.position, my_player.bomb_range, pathfinder, safety_advisor)

        best_tile_positions = tile_scorer.get_best_tiles()
        if best_tile_positions is None:
            return Action.STAY

        best_tile_position = pathfinder.get_closest_position(best_tile_positions)
        if best_tile_position == my_player.position:
            return Action.BOMB

        path_to_best_tile = pathfinder.get_path_to(best_tile_position)
        direction = my_player.position.get_direction_to(path_to_best_tile[0])

        return direction.action
