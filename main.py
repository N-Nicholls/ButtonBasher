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


class PhysChar(pygame.sprite.Sprite):
    maxSpeed = 10
    speedX = 0
    speedY = 0
    ON_GROUND = 0 # timer 3 to 0, if 0, then on ground
    ON_GROUND_FRAMES = 3 # since it carrys over a bit, you can do long/small jumps
    friction = 0.95 # constant multiplier, lowers by 5% per frame
    elasticity = 0 # how much it deflects, 0 is no bounce, 1 is perfect bounce. Higher will add energy
    PASSABLE = 0
    PASSABLE_FRAMES = 15 # how long you can fall through a fallthrough block, roughly 1/2 sec @ 30 fps
    JUMP_MULT = 1
    GRAVITY = 0
    ON_CONVEYORX = 0
    ON_CONVEYORY = 0

    effects = [ 
        ON_GROUND, JUMP_MULT, GRAVITY, ON_CONVEYORX, ON_CONVEYORY,
    ]

    def __init__(self, game, xpos = 0, ypos = 0, width = None, height = None, fric = 0.95, elas = 0, red = 255, green = 255, blue = 255):
        super(PhysChar, self).__init__()
        self.game = game
        width = width if width is not None else Game.blockSize # because wiidth height params can't see Game class
        height = height if height is not None else Game.blockSize

        self.surf = pygame.Surface((width, height))
        self.surf.fill((red, green, blue))
        self.rect = self.surf.get_rect(center = (xpos, ypos))
        self.friction = fric
        self.elasticity = elas

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
        self.ON_CONVEYORX = 0
        self.ON_CONVEYORY = 0

        # collision w/ blocks and walls
        for block in self.game.state.blocks:
            if block.PASSABLE <= 0:
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
                            self.speedY *= block.friction # friction
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

        if math.fabs(self.speedX) < 0.2: # stop doing stupid calculations
            self.speedX = 0
        if math.fabs(self.speedY) < 0.2:
            self.speedY = 0
        
class Block(PhysChar): # can be collided with, cannot collide itself (won't move)
    def __init__(self, game, xpos, ypos, width=None, height=None, fric = 0.95, elas = 0, red = 150, green = 75, blue = 0):
        width = width if width is not None else Game.blockSize # because wiidth height params can't see Game class
        height = height if height is not None else Game.blockSize
        super().__init__(game, xpos, ypos, width, height, fric, elas, red, green, blue)

# basically a trapdoor that makes it passable if the obj on it presses down
class FallThrough(Block): # if you're on it and press down, you fall through
    def __init__(self, game, xpos, ypos, width=None, height=None, fric = 0.95, elas = 0, red = 0, green = 100, blue = 0):
        width = width if width is not None else Game.blockSize # because wiidth height params can't see Game class
        height = height if height is not None else Game.blockSize
        super().__init__(game, xpos, ypos - height/4-1, width, height/2, fric, elas, red, green, blue)

    def onTop(self, pc):
        pc.ON_GROUND = pc.ON_GROUND_FRAMES
        pc.JUMP_MULT = 1 + self.elasticity
        if pc.controls[K_DOWN] and pc.ON_GROUND > 0:
            self.PASSABLE = self.PASSABLE_FRAMES
        else:
            if self.PASSABLE != 0:
                self.PASSABLE -= 1

    def update(self):
        self.PASSABLE -= 1

# Jump Pad applies constant speed for as long as you're on it, works for game ig
class Conveyor(Block): #1-left, 2-right, 3-up, 4-down
    direction = 0
    speed = 0
    def __init__(self, game, xpos, ypos, direct = 0, speedCon = 5):
        self.direction = direct
        self.speed = speedCon
        self.game = game
        super().__init__(game, xpos, ypos, Game.blockSize, Game.blockSize, fric = 0.92, elas = 0, red = 100, green = 100, blue = 0)

    def onTop(self, pc):
        pc.ON_GROUND = pc.ON_GROUND_FRAMES
        pc.JUMP_MULT = 1 + self.elasticity
        match self.direction:
            case 1:
                if math.fabs(pc.speedX) < pc.maxSpeed*1.5: # I feel like theres a better way to do these if
                    pc.ON_CONVEYORX += -self.speed # prevents gaining too much speed
            case 2:
                if math.fabs(pc.speedX) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORX += self.speed 
            case 3:
                if math.fabs(pc.speedY) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORY += -self.speed
            case 4:
                if math.fabs(pc.speedY) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORY += self.speed
            case _:
                pass

    def onLeft(self, pc): #doesn't work, as well as right
        match self.direction:
            case 1:
                if math.fabs(pc.speedX) < pc.maxSpeed*1.5: 
                    pc.ON_CONVEYORX += -self.speed 
            case 2:
                if math.fabs(pc.speedX) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORX += self.speed 
            case 3:
                if math.fabs(pc.speedY) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORY += -self.speed
            case 4:
                if math.fabs(pc.speedY) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORY += self.speed
            case _:
                pass
    def onRight(self, pc):
        match self.direction:
            case 1:
                if math.fabs(pc.speedX) < pc.maxSpeed*1.5: 
                    pc.ON_CONVEYORX += -self.speed 
            case 2:
                if math.fabs(pc.speedX) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORX += self.speed 
            case 3:
                if math.fabs(pc.speedY) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORY += -self.speed
            case 4:
                if math.fabs(pc.speedY) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORY += self.speed
            case _:
                pass
    def onBottom(self, pc): # For Mr. Dixon, PhD
        match self.direction:
            case 1:
                if math.fabs(pc.speedX) < pc.maxSpeed*1.5: 
                    pc.ON_CONVEYORX += -self.speed 
            case 2:
                if math.fabs(pc.speedX) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORX += self.speed 
            case 3:
                if math.fabs(pc.speedY) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORY += -self.speed
            case 4:
                if math.fabs(pc.speedY) < pc.maxSpeed*1.5:
                    pc.ON_CONVEYORY += self.speed
            case _:
                pass

# phys obj that can be controlled
class Player(PhysChar):
    controls = []

    def __init__(self, game, xpos, ypos, width=None, height=None, fric = 0.95, elas = 1, red = 0, green = 255, blue = 255):
        width = width if width is not None else Game.blockSize # because wiidth height params can't see Game class
        height = height if height is not None else Game.blockSize
        super().__init__(game, xpos, ypos, width, height, fric, elas, red, green, blue) 
        self.GRAVITY = 0.6
    
    def update(self, pressed_keys):
        # movement
        self.printStuff()
        self.controls = pressed_keys # this might be very stupid, but it means obj can see what the user is pressing
        if self.controls[K_DOWN] and self.speedY < self.maxSpeed:
            self.speedY += 1
        if self.controls[K_UP] and self.speedY > -self.maxSpeed and self.ON_GROUND > 0:
            self.speedY -= math.fabs(10 * self.JUMP_MULT)
        if self.controls[K_LEFT] and self.speedX > -self.maxSpeed:
            self.speedX -= 1
        if self.controls[K_RIGHT] and self.speedX < self.maxSpeed:
            self.speedX += 1

        self.speedX += self.ON_CONVEYORX
        self.speedY += self.GRAVITY + self.ON_CONVEYORY # gravity
        super().update()

'''class Enemy(pygame.sprite.Sprite):
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
            self.kill()'''

# game main class, handles main loop and changig of states
class Game():

    screenWidth = 1920
    screenHeight = 1080
    frameRate = 30
    blockSize = screenWidth/64
    offset = blockSize/2

    def __init__(self, width = 1920, height = 1080, framerate = 30):
        # define level constants, most of this can't be changed yet
        if width / height != 16/9:
            print("Warning: Nonstandard aspect ratio")
            screenWidth = 1920
            screenHeight = 1080
        else:
            screenWidth = width
            screenHeight = height
        if framerate != 30:
            print("Warning: Framerate not 30fps! This can't be changed yet")
            frameRate = 30
        frameRate = framerate
        blockSize = screenWidth/64
        offset = blockSize/2

        # important initialize stuff
        pygame.init()
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        self.running = True

        # eventually should be main menu state
        self.state = levelState("level.txt", self) # should be more comprehensive later

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.state.handle_events(events)
            self.state.update()
            self.state.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(Game.frameRate)

    def changeState(self, state):
        self.state = state

    def quit(self):
        pygame.quit()

# default gamestate class, maybe add more later
class GameState():
    def __init__(self, game):
        self.game = game
    
    def handleEvents(self):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError

    def draw(self, screen):
        raise NotImplementedError

# class to hold a level. Holds blocks and mobs and anything in a game instance
class levelState(GameState):
    
    def __init__(self, levelFile, game):
        super().__init__(game)  
        # groups for rendering
        self.game = game
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()

        # arrays for accessing
        self.Mobs = []
        self.BlockArr = []
        self.parseLevel(levelFile)

    def parseLevel(self, levelFile):
        x = Game.offset # places from the center, so offset by half blocksize (effectively x,y = 0)
        y = Game.offset
        # World is 1920x1080, each block is 30x30, so 64x36 blocks
        with open(levelFile, 'r') as file:
            lines = file.readlines()
        reading_level = False
        for line in lines:
            line = line.strip()  # Remove any leading/trailing whitespace
            # Check if we've reached the "Main" layer or any other layer in the future
            if line.lower() == "main":
                reading_level = True
                x = Game.offset
                y = Game.offset
                continue  # Skip to the next iteration
            if reading_level:
                if line:  # Make sure line is not empty
                    for col in line:
                        if col == "B":  # block
                            self.BlockArr.append(Block(self.game, x, y))
                        if col == "B": #block
                            self.BlockArr.append(Block(self.game, x, y))
                        if col == "P": # player
                            self.Mobs.append(Player(self.game, x, y))
                        if col == "R": # Redbull
                            self.BlockArr.append(Block(self.game, x, y, Game.blockSize, Game.blockSize, 1.05, 0, 255, 0, 0))
                        if col == "S": # Sludge
                            self.BlockArr.append(Block(self.game, x, y, Game.blockSize, Game.blockSize, 0.85, 0, 0, 255, 0))
                        if col == "I": # Ice
                            self.BlockArr.append(Block(self.game, x, y, Game.blockSize, Game.blockSize, 1, 0, 0, 0, 255))
                        if col == "F": # Fallthrough
                            self.BlockArr.append(FallThrough(self.game, x, y))
                        if col == "J": # JumpPad
                            self.BlockArr.append(Block(self.game, x, y, Game.blockSize, Game.blockSize, 0.95, 1.7, 255, 0, 255))
                        if col == "G": # Granite
                            self.BlockArr.append(Block(self.game, x, y, Game.blockSize, Game.blockSize, 0.93, 0.3, 100, 100, 100))
                        if col == "<": # conveyor left
                            self.BlockArr.append(Conveyor(self.game, x, y, 1, 5)) #1 left, 2 right, 3 up, 4 down
                        if col == ">": # conveyor right
                            self.BlockArr.append(Conveyor(self.game, x, y, 2, 5))
                        if col == "^": # conveyor up
                            self.BlockArr.append(Conveyor(self.game, x, y, 3, 20))
                        if col == "V": #c onveyor down
                            self.BlockArr.append(Conveyor(self.game, x, y, 4, 10))
                        x += Game.blockSize  # Move to the next block in the row
                    y += Game.blockSize  # Move to the next row
                    x = Game.offset  # Reset x to the start of the next row

        # Add Blocks and Mobs to their respective groups after loading the level
        # can't do this in each obj, cuz it can't find the element inside the scope of the obj
        # the plus side is that we can use these arrays for calling the objects in the main loop
        for elements in self.BlockArr:
            self.blocks.add(elements)
            self.all_sprites.add(elements)
        for elements in self.Mobs:
            self.all_sprites.add(elements)

    def handle_events(self, events): # to be implemented
        pass

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        self.Mobs[0].update(pressed_keys) # player physics update
        # self.enemies.update() # to be implemented

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for entity in self.all_sprites:
            screen.blit(entity.surf, entity.rect)


if __name__ == "__main__":
    buttonBasher = Game()
    buttonBasher.run()
    buttonBasher.quit()



'''
# events and timers
ADDENEMY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDENEMY, 250) # Temp removed 

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

    if pygame.sprite.spritecollideany(Mobs[0], enemies):
        Mobs[0].kill()
        running = False
'''