import pygame
from core.spritesheet import SpriteSheet

class Sword(pygame.sprite.Sprite):
    def __init__(self, game, pos, direction):
        super(Sword, self).__init__()
        self.game = game
        self.sheet = SpriteSheet("./sprites/sword-sheet.png")
        # rendering
        self.surf = self.sheet.image_at(0, 13, 13, 2)
        self.rect = self.surf.get_rect(center=pos)
        self.rect.x += 40*direction
        self.rect.y + 20
        self.direction = direction
        self.frame = 1

    def update(self):
        if self.frame > 8:
            self.kill()
        self.surf = self.sheet.image_at(self.frame-1, 13, 13, 2.5)

        if self.direction == -1:
            self.surf = pygame.transform.flip(self.surf, True, False)
        self.frame += 1

    















