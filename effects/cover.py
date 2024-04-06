import pygame
from core.spritesheet import SpriteSheet

class Cover(pygame.sprite.Sprite):
    def __init__(self, object, direction, type, duration):
        super(Cover, self).__init__()
        self.sheet = SpriteSheet("./sprites/ice_cover-sheet.png")
        self.object = object
        self.direction = direction
        self.duration = duration
        match type:
            case "sludge":
                self.level = 3
            case "fire":
                self.level = 4
            case "jump":
                self.level = 1
            case "ice":
                self.level = 0
            case "redbull":
                self.level = 2   
        self.surf = self.sheet.image_at(1, object.game.block_size, object.game.block_size, 1, None, self.level)
        self.rect = self.surf.get_rect(center = object.rect.center)
        self.frame = 1
        # self.created = True
        match self.direction:
            case "bottom":
                self.surf = pygame.transform.rotate(self.surf, 180)
            case "left":
                self.surf = pygame.transform.rotate(self.surf, 90)
            case "right":
                self.surf = pygame.transform.rotate(self.surf, -90)

    def update(self):
        # print(f"duration:{self.object.cover_top.duration}")
        self.rect = (self.object.rect.left, self.object.rect.top)
        self.object.static_update()
        '''if self.created == True:
            if self.frame <= 1:
                self.created = False
            self.surf = self.sheet.image_at(self.frame, self.object.game.block_size, self.object.game.block_size, 1, None, self.level)
            match self.direction:
                case "bottom":
                    self.surf = pygame.transform.rotate(self.surf, 180)
                case "left":
                    self.surf = pygame.transform.rotate(self.surf, 90)
                case "right":
                    self.surf = pygame.transform.rotate(self.surf, -90)
            self.frame -= 1'''
        if self.duration <= 0: # and self.created == False:
            if self.frame > 8:
                self.kill()
            self.surf = self.sheet.image_at(self.frame, self.object.game.block_size, self.object.game.block_size, 1, None, self.level)
            match self.direction:
                case "bottom":
                    self.surf = pygame.transform.rotate(self.surf, 180)
                case "left":
                    self.surf = pygame.transform.rotate(self.surf, 90)
                case "right":
                    self.surf = pygame.transform.rotate(self.surf, -90)
            self.frame += 1
        self.duration -= 1
