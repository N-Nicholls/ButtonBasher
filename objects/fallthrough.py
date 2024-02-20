from objects.physchar import PhysChar

# basically a trapdoor that makes it passable if the obj on it presses down
class FallThrough(PhysChar): # if you're on it and press down, you fall through
    def __init__(self, game, xpos, ypos):
        super().__init__(game, xpos, ypos-game.block_size/4-1, game.block_size, game.block_size/2, 0.95, 0, 0, 100, 0)

    def update(self):
        if self.passable != 0:
             self.passable -= 1

    def onTop(self, pc):    
        if pc.controls[self.game.controls["down"]] and pc.on_ground > 0:
            self.passable = 15
        super().onTop(pc)
        