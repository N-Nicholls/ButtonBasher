from objects.physchar import PhysChar
from core.vector import Vector

# Jump Pad applies constant speed for as long as you're on it, works for game ig
class Conveyor(PhysChar): #1-left, 2-right, 3-up, 4-down
    def __init__(self, game, pos, direct = None, speedCon = 5):
        self.direction = direct
        self.speed = speedCon
        self.game = game
        super().__init__(game, pos, "./sprites/error.png", False, False, 0.92, 0)

    def onTop(self, pc):
        super().onTop(pc)
        if abs(pc.velocity) < pc.maxSpeed*1.5: # only lets you get 1.5 times speed
            match self.direction:
                case "left":
                    pc.velocity += Vector(-self.speed, 0) # prevents gaining too much speed
                case "right":
                    pc.velocity += Vector(self.speed, 0)
                case "up":
                    pc.velocity += Vector(0, -self.speed)
                case "down":
                    pc.velocity += Vector(0, self.speed)
                case _:
                    pass
                        
    def onLeft(self, pc):
        super().onLeft(pc)
        if abs(pc.velocity) < pc.maxSpeed*1.5: # only lets you get 1.5 times speed
            match self.direction:
                case "left":
                    pc.velocity += Vector(-self.speed, 0) # prevents gaining too much speed
                case "right":
                    pc.velocity += Vector(self.speed, 0)
                case "up":
                    pc.velocity += Vector(0, -self.speed)
                case "down":
                    pc.velocity += Vector(0, self.speed)
                case _:
                    pass
    

    def onRight(self, pc):
        super().onRight(pc)
        if abs(pc.velocity) < pc.maxSpeed*1.5: # only lets you get 1.5 times speed
            match self.direction:
                case "left":
                    pc.velocity += Vector(-self.speed, 0) # prevents gaining too much speed
                case "right":
                    pc.velocity += Vector(self.speed, 0)
                case "up":
                    pc.velocity += Vector(0, -self.speed)
                case "down":
                    pc.velocity += Vector(0, self.speed)
                case _:
                    pass
        
    def onBottom(self, pc): # For Mr. Dixon, PhD
        super().onBottom(pc)
        if abs(pc.velocity) < pc.maxSpeed*1.5: # only lets you get 1.5 times speed
            match self.direction:
                case "left":
                    pc.velocity += Vector(-self.speed, 0) # prevents gaining too much speed
                case "right":
                    pc.velocity += Vector(self.speed, 0)
                case "up":
                    pc.velocity += Vector(0, -self.speed)
                case "down":
                    pc.velocity += Vector(0, self.speed)
                case _:
                    pass
