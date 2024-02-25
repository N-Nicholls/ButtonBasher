from objects.physchar import PhysChar
import random
import pygame

# basically a trapdoor that makes it passable if the obj on it presses down
class Spike(PhysChar): # if you're on it and press down, you fall through
    def __init__(self, game, pos):
        super().__init__(game, (pos[0], pos[1]), "./sprites/spike.png", True, False, 0.95, 0, )
        self.passable = 1

    def onTop(self, pc): 
        if self.rect.y >= pc.rect.y+3 and pc.velocity.y > 0 and pc.returnSubclass() is not "gib":
            self.game.state.gibbed((pc.rect.x, pc.rect.y), 15)
            pc.kill()
        # super().onTop(pc)

    def returnSubclass(self):
        return "spike"
        