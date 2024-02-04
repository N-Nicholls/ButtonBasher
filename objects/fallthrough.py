from objects.block import Block
from pygame.locals import K_DOWN #only whats needed
import pygame

# basically a trapdoor that makes it passable if the obj on it presses down
class FallThrough(Block): # if you're on it and press down, you fall through
    def __init__(self, game, xpos, ypos, fric = 0.95, elas = 0, kg = 1, red = 0, green = 100, blue = 0):
        super().__init__(game, xpos, ypos, fric, elas, kg, red, green, blue)
        self.surf = pygame.Surface((game.block_size, game.block_size/2))
        self.surf.fill((red, green, blue))

    def onTop(self, pc):
        pc.ON_GROUND = pc.ON_GROUND_FRAMES
        pc.JUMP_MULT = 1 + self.elasticity
        if pc.controls[K_DOWN] and pc.ON_GROUND > 0:
            self.passable = self.passable_frames
        else:
            if self.passable != 0:
                self.passable -= 1

    def update(self):
        self.passable -= 1
