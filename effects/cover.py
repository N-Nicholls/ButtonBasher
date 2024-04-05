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
        match self.direction:
            case "bottom":
                self.surf = pygame.transform.rotate(self.surf, 180)
            case "left":
                self.surf = pygame.transform.rotate(self.surf, 90)
            case "right":
                self.surf = pygame.transform.rotate(self.surf, -90)

    def update(self):
        # print(f"duration:{self.object.cover_top.duration}")
        if (self.direction == "top" and self.object.cover_top.duration == 0) or \
        (self.direction == "bottom" and self.object.cover_bottom.duration == 0) or \
        (self.direction == "left" and self.object.cover_left.duration == 0) or \
        (self.direction == "right" and self.object.cover_right.duration == 0):
            if self.frame > 8:
                self.kill()
            self.surf = self.sheet.image_at(self.frame, self.object.game.block_size, self.object.game.block_size)
            match self.direction:
                case "bottom":
                    self.surf = pygame.transform.rotate(self.surf, 180)
                case "left":
                    self.surf = pygame.transform.rotate(self.surf, 90)
                case "right":
                    self.surf = pygame.transform.rotate(self.surf, -90)
            self.frame += 1
