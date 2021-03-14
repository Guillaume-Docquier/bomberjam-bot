from core.json_serializable import JSONSerializable
from .position import Position

from core.logging import log


class Player(JSONSerializable):
    """
    The game representation of a player.

    Attributes:
        id: The id of the player
        name: The name of the player
        position: The (x, y) coordinates of the player
        starting_corner: The starting corner of a player
        bombs_left: The number of bombs a player can still use
        max_bombs: The maximum number of bombs a player can use at a time
        bomb_range: The range of this player's bombs
        is_alive: This will be False when the player is eliminated during the sudden death period
        timed_out: True if the player failed to give an Action
        respawning: The time before the player respawns
        score: The score of the player
        color: The color of the player
    """

    def __init__(self, player_json, all_bombs):
        """
        :param player_json: A player in json formatted dict
        """
        self.id = player_json["id"]
        self.name = player_json["name"]
        self.position = Position(player_json["x"], player_json["y"])
        self.starting_corner = player_json["startingCorner"]
        self.bombs_left = player_json["bombsLeft"]
        self.max_bombs = player_json["maxBombs"]
        self.bomb_range = player_json["bombRange"]
        self.is_alive = player_json["isAlive"]
        self.timed_out = player_json["timedOut"]
        self.respawning = player_json["respawning"]
        self.score = player_json["score"]
        self.color = player_json["color"]

        self.next_bomb_in = self.respawning

        my_bomb_countdowns = [bomb.countdown for bomb in all_bombs if bomb.player_id == self.id]
        if len(my_bomb_countdowns) > 0:
            self.next_bomb_in = max(self.respawning, min(my_bomb_countdowns))
