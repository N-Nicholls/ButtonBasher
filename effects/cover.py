import pygame
from core.spritesheet import SpriteSheet

class Cover(pygame.sprite.Sprite):
    def __init__(self, object, direction, type):
        super(Cover, self).__init__()
        self.sheet = SpriteSheet("./sprites/ice_cover-sheet.png")
        self.object = object
        self.direction = direction    
        self.surf = self.sheet.image_at(1, object.game.block_size, object.game.block_size)
        self.rect = self.surf.get_rect(center=object.rect.center)
        self.frame = 1

    def update(self):
        if self.direction == "up":
            if self.object.cover_top.duration == 0:
                self.kill()
        '''if self.frame > 8:
            self.kill()
        self.surf = self.sheet.image_at(self.frame-1, 13, 13, 2.5)
        self.frame += 1'''