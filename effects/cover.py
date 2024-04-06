import pygame
from core.spritesheet import SpriteSheet

class Cover(pygame.sprite.Sprite):
    def __init__(self, object, direction, type, duration):
        super(Cover, self).__init__()
        self.sheet = SpriteSheet("./sprites/ice_cover-sheet.png")
        self.object = object
        self.direction = direction
        self.duration = duration
        self.originalDur = duration
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
        if self.duration <= 8:
            if self.duration == 0:
                self.kill()
            self.surf = self.sheet.image_at(self.calculate_frame(), self.object.game.block_size, self.object.game.block_size, 1, None, self.level)
            match self.direction:
                case "bottom":
                    self.surf = pygame.transform.rotate(self.surf, 180)
                case "left":
                    self.surf = pygame.transform.rotate(self.surf, 90)
                case "right":
                    self.surf = pygame.transform.rotate(self.surf, -90)
        self.duration -= 1

    def calculate_frame(self):
        # Ensure duration is within the expected range
        if self.duration > 8:
            return 1  # If duration is above 8, frame is always 1
        else:
            # Calculate frame based on duration, where duration 8 = frame 1, and duration 1 = frame 8
            return 9 - self.duration  # This directly maps the duration to the frame number





        """self.object.static_update()
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
        self.duration -= 1"""
