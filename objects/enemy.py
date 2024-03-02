import random
from core.vector import Vector
from objects.physchar import PhysChar
import pygame


class Enemy(PhysChar): 
    def __init__(self, game, pos):
        self.speed = random.randint(1, 3)
        super().__init__(game, pos, "./sprites/enemy-sheet.png", False, False, 0.95, 0) # gets more red the faster they are
        self.velocity = Vector(0, 0)
        x = [-1, 1]
        self.direction = random.choice(x)
        self.maxSpeed = 5
        self.canBreath = True
        self.frameDelay = 5
        self.frame = 1
    
    def canMove(self):
        nextPos = self.rect.copy()
        nextPos.x += 20*self.direction
        nextPos.y += 20

        for block in self.game.state.blocks:
            if nextPos.colliderect(block.rect) and block.passable == 0:
                return True
        self.direction *= -1
        return False


    def update(self):
        if self.canMove() and abs(self.velocity) < self.maxSpeed:
            self.velocity += Vector(self.speed*self.direction, 0)
            if self.frameDelay == 5:
                self.frame += 1
                self.frameDelay = 0
            currFrame = (self.frame%6)+1
            self.surf = self.sheet.image_at(currFrame-1, self.width, self.height)
            if self.frame >= 30:
                self.frame = 1
            self.frameDelay +=1
            if self.direction != 1:
                self.surf = pygame.transform.flip(self.surf, True, False)

        super().update()

    def returnSubclass(self):
        return "enemy"
    
    def returnMobile(self):
        return True