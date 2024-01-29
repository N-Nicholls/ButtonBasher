import pygame
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class PhysChar(pygame.sprite.Sprite):

    maxSpeed = 10
    speedX = 0
    speedY = 0

    def __init__(self, xpos = 0, ypos = 0, width = 25, height = 25, red = 255, green = 255, blue = 255):
        super(PhysChar, self).__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((0, 255, 255))
        self.rect = self.surf.get_rect(center = (xpos, ypos))

    def move(self, dx, dy):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = block.rect.left
                    self.speedX -= 1
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = block.rect.right
                    self.speedX += 1
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = block.rect.top
                    self.speedY -= 1
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = block.rect.bottom
                    self.speedY += 1

    def update(self): # super function w/ pressed_keys for movement
        self.move(self.speedX, 0)
        self.move(0, self.speedY)

        if self.rect.left < 0: # moving left
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
        
        print(self.speedX, self.speedY)

class Block(PhysChar): # can be collided with, cannot collide itself (won't move)
    def __init__(self, xpos, ypos, width, height, red, green, blue):
        super().__init__(xpos, ypos, width, height, red, green, blue)

class Player(PhysChar):

    def __init__(self):
        super().__init__() 
    
    def update(self, pressed_keys):
        if pressed_keys[K_DOWN] and self.speedY < self.maxSpeed:
            self.speedY += 1
        if pressed_keys[K_UP] and self.speedY > -self.maxSpeed:
            self.speedY -= 1
        if pressed_keys[K_LEFT] and self.speedX > -self.maxSpeed:
            self.speedX -= 1
        if pressed_keys[K_RIGHT] and self.speedX < self.maxSpeed:
            self.speedX += 1
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



SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# basic variables
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True

# sprites
enemies = pygame.sprite.Group()
blocks = pygame.sprite.Group()
player = Player()

block = Block(990, 540, 75, 75, 255, 255, 255)
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
    player.update(pressed_keys)

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
