import math
from objects.block import Block

# Jump Pad applies constant speed for as long as you're on it, works for game ig
class Conveyor(Block): #1-left, 2-right, 3-up, 4-down
    def __init__(self, game, xpos, ypos, direct = 0, speedCon = 5, kg = 1):
        self.direction = direct
        self.speed = speedCon
        self.game = game
        super().__init__(game, xpos, ypos, 0.92, 0, kg, 100, 100, 0)

    def onTop(self, pc):
        pc.ON_GROUND = pc.ON_GROUND_FRAMES
        pc.JUMP_MULT = 1 + self.elasticity
        match self.direction:
            case 1:
                if math.fabs(pc.speedX) < pc.maxSpeed*1.5: # I feel like theres a better way to do these if
                    pc.ON_CONVEYORX += -self.speed # prevents gaining too much speed
            case 2:
                if math.fabs(pc.speedX) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORX += self.speed 
            case 3:
                if math.fabs(pc.speedY) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORY += -self.speed
            case 4:
                if math.fabs(pc.speedY) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORY += self.speed
            case _:
                pass

    def onLeft(self, pc): #doesn't work, as well as right
        match self.direction:
            case 1:
                if math.fabs(pc.speedX) < pc.maxSpeed*1.5: 
                    pc.ON_CONVEYORX += -self.speed 
            case 2:
                if math.fabs(pc.speedX) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORX += self.speed 
            case 3:
                if math.fabs(pc.speedY) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORY += -self.speed
            case 4:
                if math.fabs(pc.speedY) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORY += self.speed
            case _:
                pass
    def onRight(self, pc):
        match self.direction:
            case 1:
                if math.fabs(pc.speedX) < pc.maxSpeed*1.5: 
                    pc.ON_CONVEYORX += -self.speed 
            case 2:
                if math.fabs(pc.speedX) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORX += self.speed 
            case 3:
                if math.fabs(pc.speedY) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORY += -self.speed
            case 4:
                if math.fabs(pc.speedY) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORY += self.speed
            case _:
                pass
    def onBottom(self, pc): # For Mr. Dixon, PhD
        match self.direction:
            case 1:
                if math.fabs(pc.speedX) < pc.maxSpeed*1.5: 
                    pc.ON_CONVEYORX += -self.speed 
            case 2:
                if math.fabs(pc.speedX) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORX += self.speed 
            case 3:
                if math.fabs(pc.speedY) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORY += -self.speed
            case 4:
                if math.fabs(pc.speedY) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORY += self.speed
            case _:
                pass