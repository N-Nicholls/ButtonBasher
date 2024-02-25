from objects.physchar import PhysChar
from core.vector import Vector
import random

class Gib(PhysChar):
    def __init__(self, game, pos,):
        super().__init__(game, pos, "./sprites/gib1-sheet.png", True, False, 0.92, 0, )
        x = random.randint(-8, 8)
        y = random.randint(-8, -1)
        gibChoice = random.randint(1, 8) - 1
        gibSize = random.randint(1, 2)
        self.velocity = Vector(x, y)
        self.surf = self.sheet.image_at(gibChoice, 13, 13, gibSize)
        self.lifeSpan = random.randint(self.game.frame_rate, self.game.frame_rate*4)

    def update(self):
        if self.lifeSpan <= 0:
            self.kill()
        else:
            self.lifeSpan -= 1
        super().update()

    def returnSubclass(self):
        return "gib"

    def returnMobile(self):
        return True