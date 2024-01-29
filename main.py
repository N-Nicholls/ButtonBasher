# Import the pygame module
import pygame
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Consts
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

ACCEL = 1
MAXVX = 50
MAXVY = 50
FRICTION = 0.1
GRAVITY = .5

class PhysChar(pygame.sprite.Sprite):

    velocityX = 0
    velocityY = 0
    velocityXMax = MAXVX
    velocityYMax = MAXVY

    def __init__(self):
        super(PhysChar, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((0, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self): # super function w/ pressed_keys for movement

        # 1st Law of Motion
        self.rect.move_ip(self.velocityX, self.velocityY)
        # Gravity, as if you're always holding down
        if self.velocityY < self.velocityYMax:
            self.velocityY += GRAVITY
        # Friction
        if(self.velocityX > 0):
            self.velocityX -= FRICTION
        if(self.velocityX < 0):
            self.velocityX += FRICTION
        if(self.velocityY > 0):
            self.velocityY -= FRICTION
        if(self.velocityY < 0):
            self.velocityY += FRICTION

        # Keep char on the screen
        # If the player is bumping into an edge, will slow movement in that direction twofold
        # This will be a problem later when there are things to bump into that aren't walls.
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocityX += 2*ACCEL
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.velocityX -= 2*ACCEL
        if self.rect.top <= 0:
            self.velocityY += 2*ACCEL
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.velocityY -= 2*ACCEL
            self.rect.bottom = SCREEN_HEIGHT

    def handle_collision(self, group): # can be called in classes where necessary, with whatever group is necessary
        collided_objects = pygame.sprite.spritecollide(self, group, False)
        for obj in collided_objects:
            # Collision response logic here
            # Example: stop movement on collision
            if self.velocityX > 0:  # Moving right
                self.rect.right = obj.rect.left
            elif self.velocityX < 0:  # Moving left
                self.rect.left = obj.rect.right
            if self.velocityY > 0:  # Moving down
                self.rect.bottom = obj.rect.top
            elif self.velocityY < 0:  # Moving up
                self.rect.top = obj.rect.bottom
            self.velocityX = 0
            self.velocityY = 0


class Block(PhysChar): # can be collided with, cannot collide itself (won't move)
    def __init__(self, X, Y):
        super().__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((165, 42, 42))
        self.rect = self.surf.get_rect(center = (X, Y))

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(PhysChar):

    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((25, 25)) # overrides the parent's surf
        self.surf.fill((0, 255, 255))
        self.rect = self.surf.get_rect()
    
    def update(self, pressed_keys, blocks):
        # if you're moving and not at max speed, increase speed
        # note: no checks for capability of movement (collision)
        # might be a problem at higher speeds
        if pressed_keys[K_DOWN] and self.velocityY < self.velocityYMax: 
            print(self.velocityY)
            self.velocityY += ACCEL
        if pressed_keys[K_UP] and self.velocityY > -self.velocityYMax:
            print(self.velocityY)
            self.velocityY -= ACCEL
        if pressed_keys[K_LEFT] and self.velocityX > -self.velocityXMax:
            print(self.velocityX)
            self.velocityX -= ACCEL
        if pressed_keys[K_RIGHT] and self.velocityX < self.velocityXMax:
            print(self.velocityX)
            self.velocityX += ACCEL
        super().update()
        self.handle_collision(blocks)

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


# basic variables
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True
enemies = pygame.sprite.Group()
blocks = pygame.sprite.Group()
player = Player()

block = Block(990, 540)
blocks.add(block)

# events and timers
ADDENEMY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDENEMY, 250) # Temp removed 

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(block)


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
    player.update(pressed_keys, blocks)

    enemies.update()

    # Fill the screen with black
    screen.fill((0, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf,entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    # Update the display
    pygame.display.flip()
    clock.tick(30) # framerate, 30 fps
