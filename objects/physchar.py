import pygame
import math
from core.vector import Vector

class PhysChar(pygame.sprite.Sprite):
    def __init__(self, game, xpos = 0, ypos = 0, width = None, height = None, fric = 0.95, elas = 1, red = 0, green = 255, blue = 255):
        super(PhysChar, self).__init__()
        self.game = game
        # rendering
        self.width = width if width is not None else game.block_size # because width height params can't see Game class
        self.height = height if height is not None else game.block_size
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((red, green, blue))
        self.rect = self.surf.get_rect(center = (xpos, ypos))
        # physics
        self.velocity = Vector(0, 0)
        self.friction = fric
        self.elasticity = elas
        self.passable = 0
        self.on_ground = 0
        self.in_liquid = False
        # effects
        self.gravity = Vector(0, 0.6)

    def update(self):
        # effects
        self.velocity += self.gravity
        if self.on_ground > 0:
            self.on_ground -= 1
        self.in_liquid = False

        # optimises calculations
        if math.fabs(self.velocity.x) < 0.3:
            self.velocity.x = 0
        if math.fabs(self.velocity.y) < 0.3:
            self.velocity.y = 0

        # maintains movement
        self.move(self.velocity.x, 0)
        self.move(0, self.velocity.y)

        

    # collision stuff per direction individually
    def move(self, dx, dy):
        self.moveSingleAxis(dx, 0)
        self.moveSingleAxis(0, dy)

    def moveSingleAxis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        for block in self.game.state.blocks:
            if self.rect.colliderect(block.rect) and block.passable == 0:
                    if dx > 0: # moving right
                        self.rect.right = block.rect.left
                        block.onLeft(self)
                    if dx < 0: # moving left
                        self.rect.left = block.rect.right
                        block.onRight(self)
                    if dy > 0: # moving down
                        self.rect.bottom = block.rect.top
                        block.onTop(self)
                    if dy < 0: # moving up
                        self.rect.top = block.rect.bottom
                        block.onBottom(self)


    def onTop(self, pc):
        pc.on_ground = 3
        pc.jump_mult = self.elasticity + pc.elasticity
        pc.velocity = Vector(pc.velocity.x, -pc.velocity.y*self.elasticity)*self.friction
        pass
    def onBottom(self, pc):
        pc.velocity = Vector(pc.velocity.x, -pc.velocity.y*self.elasticity)*self.friction
        pass
    def onLeft(self, pc):
        pc.velocity = Vector(-pc.velocity.x*self.elasticity, pc.velocity.y)*self.friction
        pass
    def onRight(self, pc):
        pc.velocity = Vector(-pc.velocity.x*self.elasticity, pc.velocity.y)*self.friction


    


    


    """
    def moveSingleAxis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # collision w/ blocks and walls
        for block in self.game.state.blocks:
            if block.passable <= 0:
                if self.rect.colliderect(block.rect):
                    avgElas = (self.elasticity*block.elasticity)/2
                    if dx > 0: # moving right 
                        self.rect.right = block.rect.left
                        self.velocity += Vector(-self.velocity.x*avgElas*block.friction, 0) # bounce
                        block.onLeft(self)
                    if dx < 0: # moving left
                        self.rect.left = block.rect.right
                        self.velocity += Vector(-self.velocity.x*avgElas*block.friction, 0) # bounce
                        block.onRight(self)
                    if dy > 0: # moving down
                        self.rect.bottom = block.rect.top
                        self.velocity += Vector(0, -self.velocity.y*avgElas*block.friction) # stop falling, makes it so you don't bounce
                        block.onTop(self)
                    if dy < 0: # moving up
                        self.rect.top = block.rect.bottom
                        self.velocity += Vector(0, -self.velocity.y*avgElas*block.friction) # bounce
                        block.onBottom(self)
            else:
                block.update()

        for liquid in self.game.state.liquids:
            if self.rect.colliderect(liquid.rect):
                liquid.inside(self)


        '''if self.rect.left < 0: # moving left
            self.rect.left = 0
            self.speedX += 1
        if self.rect.right > SCREEN_WIDTH: # moving right
            self.rect.right = SCREEN_WIDTH
            self.speedX -= 1
        if self.rect.top <= 0: # moving up
            self.rect.top = 0
            self.speedY += 1
        if self.rect.bottom >= SCREEN_HEIGHT: # moving down
            self.rect.bottom = SCREEN_HEIGHT
            self.speedY -= 1
            self.ON_GROUND = self.ON_GROUND_FRAMES # reset on ground timer'''



    def update(self):  
        # Tag controlling if on ground. Every frame lowers by 1, if 0, then on ground
        # total frames allowed depends on ON_GROUND_FRAMES
        if self.ON_GROUND > 0:
            self.ON_GROUND -= 1
        self.ON_CONVEYORX = 0
        self.ON_CONVEYORY = 0
        if self.effectFrames > 0:
            self.effectFrames -= 1
        self.buoyantConst = 0
        self.viscosityConst = 1
        self.IN_LIQUID = 0
        self.JUMP_MULT = 1

        # maintains movement
        self.move(self.velocity.x, 0)
        self.move(0, self.velocity.y)

        # optimises calculations
        if math.fabs(self.velocity.x) < 0.2:
            self.velocity.x = 0
        if math.fabs(self.velocity.y) < 0.2:
            self.velocity.y = 0"""