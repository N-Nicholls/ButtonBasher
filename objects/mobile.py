from objects.physchar import PhysChar
from core.vector import Vector

class Mobile(PhysChar):
    def __init__(self, game, position, next = (0, 0), speed = 1):
        super().__init__(game, position[0], position[1], game.block_size*3, game.block_size/2, 0.80, 0, 100, 100, 100)
        self.speedMult = speed
        self.velocity = Vector(0, 0)

    def update(self):
        self.move()


    def move(self):
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
