from objects.physchar import PhysChar
import math
from pygame.locals import K_DOWN, K_UP, K_LEFT, K_RIGHT

# phys obj that can be controlled
class Player(PhysChar):

    def __init__(self, game, controls, xpos, ypos, fric = 0.95, elas = 1, kg = 1, red = 0, green = 255, blue = 255):
        self.controls = controls

        super().__init__(game, xpos, ypos, game.block_size, game.block_size, fric, elas, kg, red, green, blue) 
    
    def update(self, pressed_keys):
        # movement
        self.printStuff() # one frame behind, shouldn't make a difference I think
        self.controls = pressed_keys # this might be very stupid, but it means obj can see what the user is pressing
        if self.controls[K_DOWN] and self.speedY < self.maxSpeed:
            self.speedY += 1
        if self.controls[K_UP] and self.speedY > -self.maxSpeed and self.ON_GROUND > 0 and self.IN_LIQUID == 0:
            self.speedY -= math.fabs(10 * self.JUMP_MULT)
        if self.controls[K_UP] and self.speedY > -self.maxSpeed and self.IN_LIQUID == 1:
            self.speedY -= 1
        if self.controls[K_LEFT] and self.speedX > -self.maxSpeed:
            self.speedX -= 1
        if self.controls[K_RIGHT] and self.speedX < self.maxSpeed:
            self.speedX += 1

        self.speedX += (self.GRAVITYx)*self.mass + self.ON_CONVEYORX # additives to speed
        self.speedY += (self.GRAVITYy - self.buoyantConst)*self.mass + self.ON_CONVEYORY# note: buoyant force can't be directional, onyl down
        super().update()