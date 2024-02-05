import math
from objects.physchar import PhysChar
from core.vector import Vector

# Jump Pad applies constant speed for as long as you're on it, works for game ig
class Conveyor(PhysChar): #1-left, 2-right, 3-up, 4-down
    """def __init__(self, game, xpos, ypos, direct = 0, speedCon = 5, kg = 1):
        self.direction = direct
        self.speed = speedCon
        self.game = game
        super().__init__(game, xpos, ypos, 0.92, 0, kg, 100, 100, 0)

    def onTop(self, pc):
        pc.ON_GROUND = 1
        pc.JUMP_MULT = 1 + self.elasticity
        if abs(pc.velocity) < pc.maxSpeed*1.5: # only lets you get 1.5 times speed
            match self.direction:
                case 1:
                        pc.velocity += Vector(-self.speed, 0) # prevents gaining too much speed
                case 2:
                        pc.velocity += Vector(self.speed, 0)
                case 3:
                        pc.velocity += Vector(0, -self.speed)
                case 4:
                        pc.velocity += Vector(0, self.speed)
                case _:
                    pass

    def onLeft(self, pc): #doesn't work, as well as right
        pc.ON_GROUND = 1
        pc.JUMP_MULT = 1 + self.elasticity
        if abs(pc.velocity) < pc.maxSpeed*1.5: # only lets you get 1.5 times speed
            match self.direction:
                case 1:
                        pc.velocity += Vector(-self.speed, 0) # prevents gaining too much speed
                case 2:
                        pc.velocity += Vector(self.speed, 0)
                case 3:
                        pc.velocity += Vector(0, -self.speed)
                case 4:
                        pc.velocity += Vector(0, self.speed)
                case _:
                    pass
    def onRight(self, pc):
        pc.ON_GROUND = 1
        pc.JUMP_MULT = 1 + self.elasticity
        if abs(pc.velocity) < pc.maxSpeed*1.5: # only lets you get 1.5 times speed
            match self.direction:
                case 1:
                        pc.velocity += Vector(-self.speed, 0) # prevents gaining too much speed
                case 2:
                        pc.velocity += Vector(self.speed, 0)
                case 3:
                        pc.velocity += Vector(0, -self.speed)
                case 4:
                        pc.velocity += Vector(0, self.speed)
                case _:
                    pass
    def onBottom(self, pc): # For Mr. Dixon, PhD
        pc.ON_GROUND = 1
        pc.JUMP_MULT = 1 + self.elasticity
        if abs(pc.velocity) < pc.maxSpeed*1.5: # only lets you get 1.5 times speed
            match self.direction:
                case 1:
                        pc.velocity += Vector(-self.speed, 0) # prevents gaining too much speed
                case 2:
                        pc.velocity += Vector(self.speed, 0)
                case 3:
                        pc.velocity += Vector(0, -self.speed)
                case 4:
                        pc.velocity += Vector(0, self.speed)
                case _:
                    pass"""