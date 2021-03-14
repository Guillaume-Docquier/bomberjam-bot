import json
import numpy as np

from core.json_serializable import JSONSerializable
from models.bounds import Bounds
from models.player import Player
from models.bomb import Bomb
from models.bonus import Bonus

from core.logging import log


class State(JSONSerializable):
    """
    The complete game representation.

    Game Attributes:
        tiles: Represents the map in a numpy array. You can access any Tile with state.tiles[x, y]
        tick: The current game tick
        is_finished: whether or not the game is finished
        players: A list with all players in the game
        bombs: A list with all bombs in the game
        bonuses: A list with all bonuses in the game
        bounds: A representation of the game bounds (x and y)
        sudden_death_countdown: When the sudden death countdown reaches 0, the sudden death starts
        is_sudden_death_enabled: True when sudden death is active. During sudden death, respawning is disabled

    Utility Attributes
        my_bot: Represents the current player.
    """

    def __init__(self, state_string, current_player_id):
        """
        :param state_string: A json string representing the state
        :param current_player_id: The id of the current player
        """
        json_state = json.loads(state_string)

        self.tick = json_state["tick"]
        self.is_finished = json_state["isFinished"]
        self.bombs = [Bomb(bomb_json) for bomb_json in json_state["bombs"].values()]
        self.bonuses = [Bonus(bonus_json) for bonus_json in json_state["bonuses"].values()]
        self.bounds = Bounds(json_state["width"], json_state["height"])
        self.sudden_death_countdown = json_state["suddenDeathCountdown"]
        self.is_sudden_death_enabled = json_state["isSuddenDeathEnabled"]
        self.tiles = np.array(list(json_state["tiles"])).reshape(self.bounds.shape[::-1]).transpose()

        all_players = [Player(player_json, self.bombs) for player_json in json_state["players"].values()]
        self.other_players = [player for player in all_players if player.id != current_player_id]
        self.current_player = [player for player in all_players if player.id == current_player_id][0]

    def __get_dict__(self):
        """
        A numpy array is not JSON serializable so we force it to a list

        :return: dict
        """
        dict_copy = self.__dict__.copy()
        dict_copy['tiles'] = dict_copy['tiles'].tolist()

        return dict_copy
