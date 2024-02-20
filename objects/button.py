from objects.physchar import PhysChar
from core.vector import Vector

class Button(PhysChar):
    def __init__(self, game, pos, direction = "up"):
        super().__init__(game, pos[0], pos[1], game.block_size, game.block_size, 0.92, 0, 100, 100, 100)
        self.pressed = False

    def update(self):
        super().update()

    def returnSubclass(self):
        return "button"

    def returnMobile(self):
        return True