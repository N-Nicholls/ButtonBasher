from objects.physchar import PhysChar

class Block(PhysChar): # can be collided with, cannot collide itself (won't move)
    def __init__(self, game, xpos, ypos, fric =0.95, elas = 0, kg = 1, red = 150, green = 75, blue = 0):
        # self.width = width if width is not None else game.block_size # because wiidth height params can't see Game class
        # self.height = height if height is not None else game.block_size
        super().__init__(game, xpos, ypos, game.block_size, game.block_size, fric, elas, kg, red, green, blue)