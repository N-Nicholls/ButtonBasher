import random
from core.vector import Vector
from objects.physchar import PhysChar


class Enemy(PhysChar): 
    def __init__(self, game, pos):
        self.speed = random.randint(1, 3)
        super().__init__(game, pos[0], pos[1], game.block_size, game.block_size, 0.95, 0, 255*(self.speed/3), 0, 0) # gets more red the faster they are
        self.velocity = Vector(0, 0)
        x = [-1, 1]
        self.direction = random.choice(x)
        self.maxSpeed = 5
    
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

        super().update()

    def returnSubclass(self):
        return "enemy"
    
    def returnMobile(self):
        return True