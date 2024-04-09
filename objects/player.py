from core.vector import Vector
from objects.physchar import PhysChar
import pygame

# phys obj that can be controlled
class Player(PhysChar):

    def __init__(self, game, controls, pos):
        super().__init__(game, pos, "./sprites/player1-sheet.png", False, False, 0.95, 1)
        self.controls = controls
        self.maxSpeed = 10 # max speed for adding movement
        self.jump_mult = 1
        self.canBreath = True
        self.direction = 1
        self.frame = 1
        self.frameDelay = 5
        self.jumpAmt = 3
        self.charges = []

    def update(self, pressed_keys):
        # movement
        self.printStuff() # debug

        while len(self.charges) < self.jumps:
            self.charges.append(self.game.state.charge(self))
        while len(self.charges) > self.jumps:
            temp = self.charges.pop()
            temp.frame = 1
            temp.killed = True

        # frame stuff
        if self.frameDelay == 5:
            self.frame += 1
            self.frameDelay = 0
        currFrame = (self.frame%6)+1
        self.surf = self.sheet.image_at(currFrame-1, self.width, self.height)
        if self.frame >= 30:
            self.frame = 1
        self.frameDelay +=1
        if self.direction != 1:
            self.surf = pygame.transform.flip(self.surf, True, False)

        self.controls = pressed_keys
        if self.controls[self.game.controls['down']] and self.velocity.y < self.maxSpeed:
            self.velocity += Vector(0, 1)
        if self.controls[self.game.controls['up']] and self.on_ground > 0 and self.velocity.y > -self.maxSpeed:
            self.velocity += Vector(0, -14 * self.jump_mult)
            self.jumpCooldown = 10
        if self.controls[self.game.controls['up']] and self.jumps > 0 and self.jumpCooldown == 0 and self.in_liquid != 1 and self.velocity.y > -self.maxSpeed:
            self.game.state.jet((self.rect.x, self.rect.y), self)
            self.velocity.y = 0
            self.velocity += Vector(0, -14) * 1.5
            self.jumps -= 1
            self.jumpCooldown = 10
        if self.controls[self.game.controls['up']] and self.in_liquid == 1 and self.velocity.y > -self.maxSpeed:
            self.velocity += Vector(0, -1)
        if self.controls[self.game.controls['left']] and self.velocity.x > -self.maxSpeed:
            if self.direction != -1:
                self.direction *= -1
            self.velocity += Vector(-1, 0)
        if self.controls[self.game.controls['right']] and self.velocity.x < self.maxSpeed:
            self.velocity += Vector(1, 0)
            if self.direction != 1:
                self.direction *= -1
        super().update()

    def printStuff(self):
        # Format velocity components with fixed decimal places
        vx, vy = self.velocity.x, self.velocity.y
        formatted_velocity = f"({vx:.2f}, {vy:.2f})"
        
        # Format boolean values to ensure consistent length
        formatted_on_ground = str(self.on_ground > 0).ljust(5)  # 'True ' or 'False'
        formatted_in_liquid = str(self.in_liquid).ljust(5)  # 'True ' or 'False'
        
        # Use formatted string literals with fixed spacing
        print(f"xpos: {self.rect.x:<4} ypos: {self.rect.y:<4} velocity: {formatted_velocity:<15} on ground: {formatted_on_ground} in liquid: {formatted_in_liquid}" + " Jump Mult:" + str(self.jump_mult) + " Frame:" + str((self.frame%6)+1))
        # print(f"Ground: {self.on_ground} Roof: {self.on_roof} Left:  {self.on_left} Right: {self.on_right}")
        # print(f"Charges: {self.jumps} Cooldown: {self.jumpCooldown}")
        
    def returnSubclass(self):
        return "player"
    def returnMobile(self):
        return True