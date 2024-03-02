import pygame
import math
from core.vector import Vector
from core.spritesheet import SpriteSheet
import random

class PhysChar(pygame.sprite.Sprite):
    def __init__(self, game, pos = (0,0), sheetPath = "./sprites/error.png", randHor = False, randVert = False, fric = 0.95, elas = 1, coverable = False):
        super(PhysChar, self).__init__()
        self.game = game
        self.sheet = SpriteSheet(sheetPath)
        # rendering
        self.width = game.block_size 
        self.height = game.block_size
        self.surf = self.sheet.image_at(0, self.width, self.height)
        self.rect = self.surf.get_rect(center=pos)
        if randHor:
            choice1 = random.randint(0, 1)
            if choice1 == 0:
                self.surf = pygame.transform.flip(self.surf, True, False)
                self.rect.y -1
        if randVert:
            choice2 = random.randint(0, 1)
            if choice2 == 0:
                self.surf = pygame.transform.flip(self.surf, False, True)
            
        # physics/collision
        self.velocity = Vector(0, 0)
        self.friction = fric
        self.elasticity = elas
        self.passable = 0
        self.on_ground = 0
        self.in_liquid = False
        self.drowning = False # used to be in_liquid, but now in_liquid doesn't dictate drowning so this does
        self.on_left = 0
        self.on_right = 0
        self.on_roof = 0
        self.gravity = Vector(0, 0.6)

        # effects
        self.maxSpeed = 10
        self.breath = 10 * self.game.frame_rate # ten seconds
        self.canBreath = False

        # slime effects
        self.coverable = coverable
        self.temp_fric = None
        self.temp_elas = None
        self.covered_top = None
        self.top_coolDown = 0

        # player jump functions
        self.jumps = 1
        self.jumpAmt = 1
        self.jumpCooldown = 10


    def update(self):
        if self.canBreath:
            if self.drowning:
                if self.breath <= 0:
                    self.die(10)
                else:
                    self.breath -= 1
            else:
                if self.breath >= 10 * self.game.frame_rate:
                    self.breath = 10 * self.game.frame_rate
                else:
                    self.breath += 1
            # print(self.breath)


        # effects
        self.velocity += self.gravity
        if self.on_ground > 0:
            self.on_ground -= 1
        self.in_liquid = False
        self.drowning = False
        if self.on_left > 0:
            self.on_left -= 1
        if self.on_right > 0:
            self.on_right -= 1
        if self.on_roof > 0:
            self.on_roof -= 1
        
        if self.jumpCooldown > 0:
            self.jumpCooldown -= 1

        if self.on_roof and self.on_ground > 0:
            self.die(10)
        if self.on_left and self.on_right > 0:
            self.die(10)

        # optimises calculations
        if math.fabs(self.velocity.x) < 0.02:
            self.velocity.x = 0
        if math.fabs(self.velocity.y) < 0.02:
            self.velocity.y = 0

        # maintains movement
        self.move(self.velocity.x, self.velocity.y)

    # collision stuff per direction individually
    def move(self, dx, dy):
        self.moveSingleAxis(dx, 0)
        self.moveSingleAxis(0, dy)

    # calls gibbed, exists as check to make sure thing calling isn't a gib itself
    def gibbed(self, pos, intensity):
        if self.returnSubclass() == "gib":
            return
        else:   
            for _ in range(intensity):
                self.game.state.gibbed(pos)
                
    def setSheet(self, path, frame = 0):
        self.sheet = SpriteSheet(path)
        self.surf = self.sheet.image_at(frame, self.width, self.height)

    def moveSingleAxis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        for block in self.game.state.blocks:
            if self.rect.colliderect(block.rect) and block.returnSubclass() == "spike":
                block.onTop(self)
            if self.rect.colliderect(block.rect) and block.passable == 0: 
                    if dx > 0: # moving right
                        self.rect.right = block.rect.left
                        block.onLeft(self)
                    if dx < 0: # moving left
                        self.rect.left = block.rect.right
                        block.onRight(self)
                    if dy > 0: # moving down
                        self.rect.bottom = block.rect.top
                        if block.returnSubclass() == "elevator": # if elevator, then move with it
                            if block.velocity.y <= 0:
                                self.move(block.velocity.x, block.velocity.y)
                        block.onTop(self)
                    if dy < 0: # moving up
                        self.rect.top = block.rect.bottom
                        block.onBottom(self)
        for liquid in self.game.state.liquids:
            if self.rect.colliderect(liquid.rect):
                liquid.inside(self)
        if self.returnSubclass() == "enemy": # enemy collision, could later have diff collision stuff than just death
            for player in self.game.state.player:
                if self.rect.colliderect(player.rect):
                    self.game.state.sword((self.rect.x, self.rect.y), self.direction)
                    player.die(10)
        for mobile in self.game.state.mobiles:
            if self.rect.colliderect(mobile.rect) and mobile.passable == 0 and self.rect != mobile.rect and self.returnSubclass() != "gib":
                    if dx > 0: # moving right
                        self.rect.right = mobile.rect.left
                        mobile.onLeft(self)
                    if dx < 0: # moving left
                        self.rect.left = mobile.rect.right
                        mobile.onRight(self)
                    if dy > 0: # moving down
                        self.rect.bottom = mobile.rect.top
                        mobile.onTop(self)
                    if dy < 0: # moving up
                        self.rect.top = mobile.rect.bottom
                        mobile.onBottom(self)


    def onTop(self, pc):
        pc.on_ground = 3
        pc.jumps = pc.jumpAmt
        pc.jump_mult = self.elasticity + pc.elasticity
        pc.velocity = Vector(pc.velocity.x, -pc.velocity.y*self.elasticity)*self.friction
        pass
    def onBottom(self, pc):
        pc.on_roof = 1
        pc.velocity = Vector(pc.velocity.x, -pc.velocity.y*self.elasticity)*self.friction
        pass
    def onLeft(self, pc):
        pc.on_right = 1
        pc.velocity = Vector(-pc.velocity.x*self.elasticity, pc.velocity.y)*self.friction
        if pc.returnSubclass() == "enemy" or "slime":
            pc.direction *= -1
        pass
    def onRight(self, pc):
        pc.on_left = 1
        pc.velocity = Vector(-pc.velocity.x*self.elasticity, pc.velocity.y)*self.friction
        if pc.returnSubclass() == "enemy" or "slime":
            pc.direction *= -1

    def die(self, intensity = 0, path = None):
        self.gibbed((self.rect.x, self.rect.y), intensity)
        self.game.state.addBody(self.rect.center, path)
        self.kill()

    def disableControls(self):
        pass

    def returnSubclass(self):
        return "physchar"
    
    def returnMobile(self):
        return False
    
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



    """def update(self):  
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
"""