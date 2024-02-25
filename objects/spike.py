from objects.physchar import PhysChar

# basically a trapdoor that makes it passable if the obj on it presses down
class Spike(PhysChar): # if you're on it and press down, you fall through
    def __init__(self, game, pos):
        super().__init__(game, (pos[0], pos[1]), 0.95, 0, "./sprites/spike.png")
        self.passable = 1

    def onTop(self, pc):    
        pc.kill()
        super().onTop(pc)

    def returnSubclass(self):
        return "spike"
        