import pygame
import math
from core.vector import Vector

class PhysChar(pygame.sprite.Sprite):
    maxSpeed = 10
    speedX = 0
    speedY = 0
    ON_GROUND = 0 # timer 3 to 0, if 0, then on ground
    ON_GROUND_FRAMES = 3 # since it carrys over a bit, you can do long/small jumps
    IN_LIQUID = 0
    JUMP_MULT = 1
    GRAVITYy = 0.6 #vectorized
    GRAVITYx = 0
    ON_CONVEYORX = 0
    ON_CONVEYORY = 0
    mass = 1 # used for gravity and buoyancy
    viscosityConst = 1 # how much it slows you down
    buoyantConst = 0 # how much it pushes you up
    effectFrames = 1 # how long the multiplier lasts

    effects = [ 
        ON_GROUND, JUMP_MULT, GRAVITYy, GRAVITYx, ON_CONVEYORX, ON_CONVEYORY, viscosityConst, buoyantConst,
    ]

    def __init__(self, game, xpos = 0, ypos = 0, width = None, height = None, fric = 0.95, elas = 0, kg = 1, red = 255, green = 255, blue = 255):
        super(PhysChar, self).__init__()
        self.game = game
        self.width = width if width is not None else game.block_size # because wiidth height params can't see Game class
        self.height = height if height is not None else game.block_size
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((red, green, blue))
        self.rect = self.surf.get_rect(center = (xpos, ypos))
        self.friction = fric
        self.elasticity = elas
        self.mass = kg # note: this does not mean the character is 1 fucking kilogram
        self.passable = 0
        self.passable_frames = game.frame_rate/2 # roughly 1/2 sec

    # "abstract" functions for dynamic objects
    def onTop(self, pc): # called by block, parameter is player
        pc.ON_GROUND = pc.ON_GROUND_FRAMES
        pc.JUMP_MULT = 1 + self.elasticity
    def onBottom(self, pc):
        pass
    def onLeft(self, pc):
        pass
    def onRight(self, pc):
        pass

    def move(self, dx, dy):
        if dx != 0:
            self.moveSingleAxis(dx, 0)
        if dy != 0:
            self.moveSingleAxis(0, dy)

    def moveSingleAxis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

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

        # collision w/ blocks and walls
        for block in self.game.state.blocks:
            if block.passable <= 0:
                if self.rect.colliderect(block.rect):
                    avgElas = (self.elasticity*block.elasticity)/2
                    if dx > 0: # moving right 
                        self.rect.right = block.rect.left
                        self.speedX = -self.speedX*avgElas# bounce
                        if math.fabs(self.speedY) < self.maxSpeed*1.5: # only lets you get 1.5 times speed
                            self.speedY *= block.friction # friction
                        block.onLeft(self)
                    if dx < 0: # moving left
                        self.rect.left = block.rect.right
                        self.speedX = -self.speedX*avgElas # bounce
                        if math.fabs(self.speedY) < self.maxSpeed*1.5: # only lets you get 1.5 times speed
                            self.speedY *= block.friction  # friction
                        block.onRight(self)
                    if dy > 0: # moving down
                        self.rect.bottom = block.rect.top
                        self.speedY = -self.speedY*avgElas # stop falling, makes it so you don't bounce
                        if math.fabs(self.speedX) < self.maxSpeed*1.5: # only lets you get 1.5 times speed
                            self.speedX *= block.friction # friction
                        block.onTop(self)
                    if dy < 0: # moving up
                        self.rect.top = block.rect.bottom
                        self.speedY = -self.speedY*avgElas # bounce
                        if math.fabs(self.speedX) < self.maxSpeed*1.5: # only lets you get 1.5 times speed
                            self.speedX *= block.friction # friction
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

    # for debugging, prints at start of a frame, so before movement inputs
    def printStuff(self):
        print("x: " + str(self.rect.x) + " y: " + str(self.rect.y) + " speedX: " + str(self.speedX) + " speedY: " + str(self.speedY) + " onGround: " + str(self.ON_GROUND > 0))

    def update(self):
        # maintains movement
        self.move(self.speedX*self.viscosityConst, 0)
        self.move(0, self.speedY* self.viscosityConst)

        if math.fabs(self.speedX) < 0.2: # stop doing stupid calculations
            self.speedX = 0
        if math.fabs(self.speedY) < 0.2:
            self.speedY = 0