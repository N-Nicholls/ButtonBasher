import pygame
from core.spritesheet import SpriteSheet

class Jet(pygame.sprite.Sprite):
    def __init__(self, pos, object):
        super(Jet, self).__init__()
        self.sheet = SpriteSheet("./sprites/jet-sheet.png")
        # rendering
        
        # self.object = object
        self.surf = self.sheet.image_at(0, 100, 25, .5)
        self.rect = self.surf.get_rect(center=(pos[0]+ 22, pos[1] + 30))
        # self.rect.y +30
        self.frame = 1

    def update(self):

        if self.frame > 8:
            self.kill()
        self.surf = self.sheet.image_at(self.frame-1, 13, 13, 2.5)
        self.frame += 1


        # self.rect.x = self.object.rect.x - 12.5
        # self.rect.y = self.object.rect.y + 30