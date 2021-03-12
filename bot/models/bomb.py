from core.json_serializable import JSONSerializable
from .position import Position


class Bomb(JSONSerializable):
    """
    The game representation of a bomb.

    Attributes:
        countdown: A bomb explodes when its countdown reaches 0
        player_id: The id of the played who owns this bomb
        range: Represents how far the bomb explosion can reach. A range of 0 will only burn the tile where the bomb is
        position: The (x, y) coordinates of the bomb
    """

    def __init__(self, bomb_json):
        """
        :param bomb_json: A bomb in json formatted dict
        """
        self.countdown = bomb_json["countdown"]
        self.player_id = bomb_json["playerId"]
        self.range = bomb_json["range"]
        self.position = Position(bomb_json["x"], bomb_json["y"])
