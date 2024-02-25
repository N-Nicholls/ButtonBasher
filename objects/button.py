from objects.physchar import PhysChar
from core.vector import Vector

class Button(PhysChar):
    def __init__(self, game, pos, direction = "up"):
        super().__init__(game, pos, "./sprites/error.png", False, False, 0.92, 0)
        self.pressed = False

    def update(self):
        super().update()

    def returnSubclass(self):
        return "button"

    def returnMobile(self):
        return True