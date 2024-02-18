from objects.physchar import PhysChar
from core.vector import Vector

class Elevator(PhysChar):
    def __init__(self, game, position, next = (0, 0), speed = 1):
        super().__init__(game, position[0], position[1], game.block_size*3, game.block_size/2, 0.80, 0, 100, 100, 100)
        self.speedMult = speed
        self.velocity = Vector(0, 0)
        self.position = (self.rect.centerx, self.rect.centery)
        self.next = (next[0], next[1])
        self.pointA = self.position[0], self.position[1]
        self.pointB = self.next[0], self.next[1]

    def update(self):
        if self.position == self.pointA:
            self.next = self.pointB
        elif self.position == self.pointB:
            self.next = self.pointA
        self.move()


    def move(self):
        self.velocity = (0, 0)
        self.position = (self.rect.centerx, self.rect.centery)
        self.velocity = Vector(self.next[0] - self.position[0], self.next[1] - self.position[1]).normalize() * self.speedMult
        self.moveSingleAxis(self.velocity.x, 0)
        self.moveSingleAxis(0, self.velocity.y)

    def moveSingleAxis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        for block in self.game.state.mobiles:
            if self.rect.colliderect(block.rect) and block.passable == 0:
                    if dx > 0: # moving right
                        self.rect.right = block.rect.left
                        # block.onLeft(self)
                    if dx < 0: # moving left
                        self.rect.left = block.rect.right
                        # block.onRight(self)
                    if dy > 0: # moving down
                        self.rect.bottom = block.rect.top
                        # block.onTop(self)
                    if dy < 0: # moving up
                        self.rect.top = block.rect.bottom
                        # block.onBottom(self)

    def returnSubclass(self):
        return "elevator"
