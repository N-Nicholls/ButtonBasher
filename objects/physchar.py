import pygame
import math
from core.vector import Vector
from core.spritesheet import SpriteSheet
from effects.effect import Effect
import random

class PhysChar(pygame.sprite.Sprite):
    def __init__(self, game, pos = (0,0), sheetPath = "./sprites/error.png", randHor = False, randVert = False, fric = 0.95, elas = 1, coverable = (0,0,0,0)):
        super(PhysChar, self).__init__()
        self.game = game
        
        # rendering
        self.sheet = SpriteSheet(sheetPath)
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

        # slime cover
        self.coverable = coverable # top, bottom, left, right
        self.cover_top = None
        self.cover_bottom = None
        self.cover_left = None
        self.cover_right = None
            
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
        self.effects = []

        # player jump functions
        self.jumps = 1
        self.jumpAmt = 1
        self.jumpCooldown = 10

    def static_update(self):
        # effects and block covering updates
        for effect in self.effects:
            effect.update()
        for cover in [self.cover_top, self.cover_bottom, self.cover_left, self.cover_right]:
            if cover is not None:
                if cover.duration <= 0:
                    cover = None
                else:
                    cover.update()

    def update(self):
        # breathing updates
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

        # non-slime effects
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
        
        # player jump updates
        if self.jumpCooldown > 0:
            self.jumpCooldown -= 1

        # get squished
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
        if pc.returnSubclass() == "slime" and self.coverable[0] == 1:               
            if self.cover_top is not None and self.cover_top.type == pc.type:
                self.cover_top.duration = 50
                self.game.state.coverAdd(self, "top", pc.type)
            else:
                self.cover_top = Effect(pc.type, 50) 
                self.game.state.coverAdd(self, "top", pc.type)
        pass
    def onBottom(self, pc):
        pc.on_roof = 1
        pc.velocity = Vector(pc.velocity.x, -pc.velocity.y*self.elasticity)*self.friction
        if pc.returnSubclass() == "slime" and self.coverable[1] == 1:
            if self.cover_bottom is not None and self.cover_bottom.type == pc.type:
                self.cover_bottom.duration = 50
                self.game.state.coverAdd(self, "bottom", pc.type) 
            else:
                self.cover_bottom = Effect(pc.type, 50)
                self.game.state.coverAdd(self, "bottom", pc.type) 
        pass
    def onLeft(self, pc):
        pc.on_right = 1
        pc.velocity = Vector(-pc.velocity.x*self.elasticity, pc.velocity.y)*self.friction
        if pc.returnSubclass() == "slime" and self.coverable[2] == 1:
            if self.cover_left is not None and self.cover_left.type == pc.type:
                self.cover_left.duration = 50
                self.game.state.coverAdd(self, "left", pc.type)
            else:
                self.cover_left = Effect(pc.type, 50)
                self.game.state.coverAdd(self, "left", pc.type) 
        if pc.returnSubclass() == "enemy" or pc.returnSubclass() == "slime":
            pc.direction *= -1
        pass
    def onRight(self, pc):
        pc.on_left = 1
        pc.velocity = Vector(-pc.velocity.x*self.elasticity, pc.velocity.y)*self.friction
        if pc.returnSubclass() == "slime" and self.coverable[3] == 1:
            if self.cover_right is not None and self.cover_right.type == pc.type:
                self.cover_right.duration = 50
                self.game.state.coverAdd(self, "right", pc.type)
            else:
                self.cover_right = Effect(pc.type, 50) 
                self.game.state.coverAdd(self, "right", pc.type)
        if pc.returnSubclass() == "enemy" or pc.returnSubclass() == "slime":
            pc.direction *= -1

    def die(self, intensity = 0, path = None):
        self.gibbed((self.rect.x, self.rect.y), intensity)
        self.kill()

    # calls gibbed, exists as check to make sure thing calling isn't a gib itself
    def gibbed(self, pos, intensity):
        if self.returnSubclass() == "gib":
            return
        else:   
            for _ in range(intensity):
                self.game.state.gibbed(pos)

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