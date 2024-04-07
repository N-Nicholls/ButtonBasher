import pygame
from core.vector import Vector
import random
from core.spritesheet import SpriteSheet

# note: liquid modifies your new move speed, but doesn't actively slow you down like frictio
# because then you stop moving after awhile and gravity doesn't work. So you maintain speed inside
class Liquid(pygame.sprite.Sprite):

    def __init__(self, game, pos, sheetPath = "./sprites/error.png", randHor = False, randVert = False, alpha = 100,  vis = 1, buoy = 0, drownable = True):
        super(Liquid, self).__init__()
        self.sheet = SpriteSheet(sheetPath)
        self.game = game
        self.width = game.block_size 
        self.height = game.block_size
        self.surf = self.sheet.image_at(0, self.width, self.height)
        self.rect = self.surf.get_rect(center=pos)
        if randHor:
            choice1 = random.randint(0, 1)
            if choice1 == 0:
                self.surf = pygame.transform.flip(self.surf, True, False)
                self.rect.y -1
        if randVert:
            choice2 = random.randint(0, 1)
            if choice2 == 0:
                self.surf = pygame.transform.flip(self.surf, False, True)
        self.surf.set_alpha(alpha)
        self.drownable = drownable
        self.viscosity = vis
        self.buoyantForce = buoy


    def inside(self, pc):
        if pc.passable == 0:
            pc.in_liquid = True
            if self.drownable:
                pc.drowning = True
            pc.velocity *= self.viscosity
            pc.velocity += pc.gravity - Vector(0, self.buoyantForce)
