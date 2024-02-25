from core.vector import Vector
from objects.physchar import PhysChar
import pygame

# phys obj that can be controlled
class Player(PhysChar):

    def __init__(self, game, controls, pos):
        super().__init__(game, pos, 0.95, 1, "./sprites/player.png")
        self.controls = controls
        self.maxSpeed = 10 # max speed for adding movement
        self.jump_mult = 1
        self.direction = 1
    
    def update(self, pressed_keys):
        # movement
        self.printStuff()

        self.controls = pressed_keys
        if self.controls[self.game.controls['down']] and self.velocity.y < self.maxSpeed:
            self.velocity += Vector(0, 1)
        if self.controls[self.game.controls['up']] and self.on_ground > 0 and self.velocity.y > -self.maxSpeed:
            self.velocity += Vector(0, -10 * self.jump_mult)
        if self.controls[self.game.controls['up']] and self.in_liquid == 1 and self.velocity.y > -self.maxSpeed:
            self.velocity += Vector(0, -1)
        if self.controls[self.game.controls['left']] and self.velocity.x > -self.maxSpeed:
            if self.direction != -1:
                self.surf = pygame.transform.flip(self.surf, True, False)
                self.direction *= -1
            self.velocity += Vector(-1, 0)
        if self.controls[self.game.controls['right']] and self.velocity.x < self.maxSpeed:
            self.velocity += Vector(1, 0)
            if self.direction != 1:
                self.surf = pygame.transform.flip(self.surf, True, False)
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
        print(f"xpos: {self.rect.x:<4} ypos: {self.rect.y:<4} velocity: {formatted_velocity:<15} on ground: {formatted_on_ground} in liquid: {formatted_in_liquid}" + " Jump Mult:" + str(self.jump_mult))

    def returnSubclass(self):
        return "player"
    def returnMobile(self):
        return True