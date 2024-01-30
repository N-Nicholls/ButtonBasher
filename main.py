import pygame
import random
import math

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FRAMERATE = 30

# level is a list of strings, each string is a row of blocks
# World is 1920x1080, each block is 30x30, so 64x36 blocks
level = [
        ("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB", # 0
        "B                                                              B", # 1
        "B                                                              B", # 2
        "B                                                              B", # 3
        "B                                  BBBBBB B B BBBBBB           B", # 4
        "B                                       S S R R                B", # 5
        "B                                       S S R R                B", # 6
        "B                                       S S R R                B", # 7
        "B                              BBB      S S R R                B", # 8
        "B                                       S S R R                B", # 9
        "B                                       S S R R                B", # 10
        "B                                       S S R R                B", # 11
        "B                   BBBB                S S R R                B", # 12
        "B                                                              B", # 13
        "B                                                              B", # 14
        "B                                                              B", # 15
        "B                                                              B", # 16
        "B                                P                             B", # 17
        "B                                                              B", # 18
        "B           BBBB                                               B", # 19
        "B                                                              B", # 20
        "B                              BBBBB   BJJJJJJBBB              B", # 21
        "B                                                              B", # 22
        "B                                                              B", # 23
        "B            BBBFFFFBBB                          BBBB          B", # 24
        "B                                                              B", # 25
        "B                                                              B", # 26
        "BBBB BBB                           RRRRRRRRRRR                 B", # 27
        "B                                                              B", # 28
        "B                                                              B", # 29
        "B                                                         BBBBBB", # 30
        "B                  B B                                         B", # 31
        "B                  B B                                         B", # 32
        "B                  B B                                         B", # 33
        "B                                                              B", # 34
        "BBBBBBBBBSSSIIIIIIISSSBBBBBBBBBBBBBBBBBBBBSSSSSBBBBBBBBBBBBBBBBB",), # 35

        ("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                              P                               J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                  GGGGGGGGGGGG                                J",
        "J                                                              J",
        "J                                                              J",
        "J                                      GGGGGGG                 J",
        "J                                                     G        J",
        "J                                                     G        J",
        "J                                                     G        J",
        "J             GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG        J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "J                                                              J",
        "JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ",
        )
        ]
# level constants
BLOCKSIZE = 30
OFFSET = BLOCKSIZE/2


class PhysChar(pygame.sprite.Sprite):

    maxSpeed = 10
    speedX = 0
    speedY = 0
    ON_GROUND = 0 # timer 3 to 0, if 0, then on ground
    ON_GROUND_FRAMES = 3 # since it carrys over a bit, you can do long/small jumps
    friction = 0.95 # constant multiplier, lowers by 5% per frame
    elasticity = 0 # how much it deflects, 0 is no bounce, 1 is perfect bounce. Higher will add energy
    passable = 0
    PASSABLE_FRAMES = 15 # how long you can fall through a fallthrough block, roughly 1/2 sec @ 30 fps
    SPEED_CUTOFF = 0.2

    def __init__(self, xpos = 0, ypos = 0, width = BLOCKSIZE, height = BLOCKSIZE, fric = 0.95, elas = 0, red = 255, green = 255, blue = 255):
        super(PhysChar, self).__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((red, green, blue))
        self.rect = self.surf.get_rect(center = (xpos, ypos))
        self.friction = fric
        self.elasticity = elas

    def move(self, dx, dy):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # Tag controlling if on ground. Every frame lowers by 1, if 0, then on ground
        # total frames allowed depends on ON_GROUND_FRAMES
        if self.ON_GROUND > 0:
            self.ON_GROUND -= 1

        # collision w/ blocks and walls
        for block in blocks:
            if block.passable <= 0:
                if self.rect.colliderect(block.rect):
                    avgElas = (self.elasticity*block.elasticity)/2
                    if dx > 0: # moving right 
                        self.rect.right = block.rect.left
                        self.speedX = -self.speedX*avgElas# bounce
                        if math.fabs(self.speedY) < self.maxSpeed*1.5: # only lets you get 1.5 times speed
                            self.speedY *= block.friction # friction
                    if dx < 0: # moving left
                        self.rect.left = block.rect.right
                        self.speedX = -self.speedX*avgElas # bounce
                        if math.fabs(self.speedY) < self.maxSpeed*1.5: # only lets you get 1.5 times speed
                            self.speedY *= block.friction # friction
                    if dy > 0: # moving down
                        self.rect.bottom = block.rect.top
                        self.speedY = -self.speedY*avgElas # stop falling, makes it so you don't bounce
                        if math.fabs(self.speedX) < self.maxSpeed*1.5: # only lets you get 1.5 times speed
                            self.speedX *= block.friction # friction
                        self.ON_GROUND = self.ON_GROUND_FRAMES # reset on ground timer
                    if dy < 0: # moving up
                        self.rect.top = block.rect.bottom
                        self.speedY = -self.speedY*avgElas # bounce
                        if math.fabs(self.speedX) < self.maxSpeed*1.5: # only lets you get 1.5 times speed
                            self.speedX *= block.friction # friction
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
        self.move(self.speedX, 0)
        self.move(0, self.speedY)

        if math.fabs(self.speedX) < self.SPEED_CUTOFF: # stop doing stupid calculations
            self.speedX = 0
        if math.fabs(self.speedY) < self.SPEED_CUTOFF:
            self.speedY = 0
        
class Block(PhysChar): # can be collided with, cannot collide itself (won't move)
    def __init__(self, xpos, ypos, width = BLOCKSIZE, height = BLOCKSIZE, fric = 0.95, elas = 0, red = 150, green = 75, blue = 0):
        super().__init__(xpos, ypos, width, height, fric, elas, red, green, blue)

class FallThrough(Block): # if you're on it and press down, you fall through
    def __init__(self, xpos, ypos, width = BLOCKSIZE, height = BLOCKSIZE/2, fric = 0.95, elas = 0, red = 0, green = 100, blue = 0):
        super().__init__(xpos, ypos - height/2-1, width, height, fric, elas, red, green, blue)

    def update(self, pressed_keys, pc): # This makes ALL fallthrough blocks fallthrough, not just the one you're on
        if pressed_keys[K_DOWN] and pc.ON_GROUND > 0: # will need a diff passable flag for enemies + mulitplayer
            self.passable = self.PASSABLE_FRAMES
        else:
            if self.passable != 0:
                self.passable -= 1

class Player(PhysChar):
    GRAVITY = 0.6

    def __init__(self, xpos, ypos, width = BLOCKSIZE, height = BLOCKSIZE, fric = 0.95, elas = 1, red = 0, green = 255, blue = 255):
        super().__init__(xpos, ypos, width, height, fric, elas, red, green, blue) 
    
    def update(self, pressed_keys):
        # movement
        self.printStuff()
        if pressed_keys[K_DOWN] and self.speedY < self.maxSpeed:
            self.speedY += 1
        if pressed_keys[K_UP] and self.speedY > -self.maxSpeed and self.ON_GROUND > 0:
            self.speedY -= 10
        if pressed_keys[K_LEFT] and self.speedX > -self.maxSpeed:
            self.speedX -= 1
        if pressed_keys[K_RIGHT] and self.speedX < self.maxSpeed:
            self.speedX += 1

        self.speedY += self.GRAVITY # gravity
        super().update()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# main
# initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
blocks = pygame.sprite.Group()
fallThrough = pygame.sprite.Group()

Mobs = []
BlockArr = []

x = OFFSET # places from the center, so offset by half blocksize (effectively x,y = 0)
y = OFFSET
for row in level[1]:
        for col in row:
            if col == "B": #block
                BlockArr.append(Block(x, y))
            if col == "P": # player
                Mobs.append(Player(x, y))
            if col == "R": # Redbull
                BlockArr.append(Block(x, y, BLOCKSIZE, BLOCKSIZE, 1.05, 0, 255, 0, 0))
            if col == "S": # Sludge
                BlockArr.append(Block(x, y, BLOCKSIZE, BLOCKSIZE, 0.85, 0, 0, 255, 0))
            if col == "I": # Ice
                BlockArr.append(Block(x, y, BLOCKSIZE, BLOCKSIZE, 1, 0, 0, 0, 255))
            if col == "F": # Fallthrough
                BlockArr.append(FallThrough(x, y))
                fallThrough.add(BlockArr[-1]) # -1 indicates last elem
            if col == "J": # JumpPad
                BlockArr.append(Block(x, y, BLOCKSIZE, BLOCKSIZE, 0.95, 1.7, 255, 0, 255))
            if col == "G": # Granite
                BlockArr.append(Block(x, y, BLOCKSIZE, BLOCKSIZE, 0.93, 0.3, 100, 100, 100))
            x += BLOCKSIZE # 60x60 is size of block
        y += BLOCKSIZE
        x = OFFSET

# can't do this in each obj, cuz it can't find the element inside the scope of the obj
# the plus side is that we can use these arrays for calling the objects in the main loop
for elements in BlockArr:
    blocks.add(elements)
    all_sprites.add(elements)
for elements in Mobs:
    all_sprites.add(elements)

# events and timers
ADDENEMY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDENEMY, 250) # Temp removed 

clock = pygame.time.Clock()

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)


    pressed_keys = pygame.key.get_pressed()
    fallThrough.update(pressed_keys, Mobs[0]) # fallthrough update
    Mobs[0].update(pressed_keys) # player physics update
    enemies.update()

    # Fill the screen with black
    screen.fill((0, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf,entity.rect)

    if pygame.sprite.spritecollideany(Mobs[0], enemies):
        Mobs[0].kill()
        running = False

    # Update the display
    pygame.display.flip()
    clock.tick(FRAMERATE) # framerate, 30 fps