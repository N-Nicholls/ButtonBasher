import pygame
from core.spritesheet import SpriteSheet

class Bar(pygame.sprite.Sprite):
    def __init__(self, game, object):
        super(Bar, self).__init__()
        self.game = game
        self.object = object
        self.sheet = SpriteSheet("./sprites/bar.png")
        # rendering
        self.surf = self.sheet.image_at(0, 200, 50, .5)
        self.rect = self.surf.get_rect(center =(object.rect.x, object.rect.y))
        self.rect.y - 80
        self.frame = 1

    def update(self):
        if self.object.breath == 10*self.game.frame_rate:
            self.rect.x = -10
            self.rect.y = -10
        else:
            if self.object not in self.game.state.player:
                self.kill()
            self.frame = (10*self.game.frame_rate - self.object.breath) * 2.4 // self.game.frame_rate % 25
            # print(self.frame)
            self.surf = self.sheet.image_at(self.frame, 200, 50, .5)
            self.rect.x = self.object.rect.x - 12.5
            self.rect.y = self.object.rect.y - 40