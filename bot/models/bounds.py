from models.position import Position


class Bounds:
    def __init__(self, width, height, origin=(0, 0)):
        self.origin = Position(*origin)
        self.max_position = Position(self.origin.x + width - 1, self.origin.y + height - 1)
        self.shape = (width, height)

    def contains(self, position):
        return self.origin.x <= position.x <= self.max_position.x and self.origin.y <= position.y <= self.max_position.y

    def __str__(self):
        return f"Bounds(origin={self.origin}, max_position={self.max_position}, shape={self.shape})"
