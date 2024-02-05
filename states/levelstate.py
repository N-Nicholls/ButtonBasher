from states.gamestate import GameState
from objects.physchar import PhysChar
from objects.liquid import Liquid 
from objects.player import Player
from objects.fallthrough import FallThrough
from objects.conveyor import Conveyor
import pygame

# class to hold a level. Holds blocks and mobs and anything in a game instance
class LevelState(GameState):
    
    def __init__(self, level_file, game, controls):
        super().__init__(game)  
        # groups for rendering
        self.game = game
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.player = pygame.sprite.Group()
        self.fallthrough = pygame.sprite.Group()
        self.liquids = pygame.sprite.Group()
        # self.enemies = pygame.sprite.Group()
        
        self.controls = controls

        # arrays for accessing
        self.blockArr = []
        self.mobArr = []
        self.playerArr = []
        self.fallthroughArr = []
        self.liquidArr = []
        self.parseLevel(level_file, game)

    def parseLevel(self, levelFile, game):
        x = game.offset # places from the center, so offset by half blocksize (effectively x,y = 0)
        y = game.offset
        # World is 1920x1080, each block is 30x30, so 64x36 blocks
        with open(levelFile, 'r') as file:
            lines = file.readlines()
        reading_level = False
        for line in lines:
            line = line.strip()  # Remove any leading/trailing whitespace
            # Check if we've reached the "Main" layer or any other layer in the future
            if line.lower() == "main":
                reading_level = True
                x = game.offset
                y = game.offset
                continue  # Skip to the next iteration
            if reading_level:
                if line:  # Make sure line is not empty
                    for col in line:
                        if col == "B":  # block
                            self.blockArr.append(PhysChar(self.game, x, y, None, None, 0.85, 0, 139, 69, 19))
                        if col == "P": # player
                            self.playerArr.append(Player(self.game, self.controls, x, y))
                        if col == "R": # Redbull
                            self.blockArr.append(PhysChar(self.game, x, y, None, None, 1.05, 0, 255, 0, 0))
                        if col == "S": # Sludge
                            self.blockArr.append(PhysChar(self.game, x, y, None, None, 0.75, 0.2, 0, 255, 0))
                        if col == "I": # Ice
                            self.blockArr.append(PhysChar(self.game, x, y, None, None, 1, 0, 0, 0, 255))
                        if col == "G": # Granite
                            self.blockArr.append(PhysChar(self.game, x, y, None, None, 0.85, 0.3, 100, 100, 100))
                        if col == "J": # JumpPad
                            self.blockArr.append(PhysChar(self.game, x, y, None, None, 0.85, 1, 255, 0, 255))
                        if col == "F": # Fallthrough
                            self.fallthroughArr.append(FallThrough(self.game, x, y))
                        """if col == "<": # conveyor left
                            self.blockArr.append(Conveyor(self.game, x, y, 1, 5, 1)) #1 left, 2 right, 3 up, 4 down
                        if col == ">": # conveyor right
                            self.blockArr.append(Conveyor(self.game, x, y, 2, 5, 1))
                        if col == "^": # conveyor up
                            self.blockArr.append(Conveyor(self.game, x, y, 3, 20, 1))
                        if col == "V": # conveyor down
                            self.blockArr.append(Conveyor(self.game, x, y, 4, 10, 1))"""
                        if col == "W": # water
                            self.liquidArr.append(Liquid(self.game, x, y, 0, 70, 255, 70, 0.98, 0.7))
                        if col == "L": # ladder
                            self.liquidArr.append(Liquid(self.game, x, y, 255, 255, 0, 150, 0.98, 0.6))
                        if col == "C": # concrete
                            self.liquidArr.append(Liquid(self.game, x, y, 255, 255, 255, 150, 0.94, 0.5999))
                        x += game.block_size  # Move to the next block in the row
                    y += game.block_size  # Move to the next row
                    x = game.offset  # Reset x to the start of the next row

        for elements in self.blockArr:
            self.blocks.add(elements)
            self.all_sprites.add(elements)
        for elements in self.playerArr:
            self.player.add(elements)
            self.mobs.add(elements)
            self.all_sprites.add(elements)
        for elements in self.mobArr:
            self.mobs.add(elements)
            self.all_sprites.add(elements)
        for elements in self.fallthroughArr:
            self.fallthrough.add(elements)
            self.blocks.add(elements)
            self.all_sprites.add(elements)
        for elements in self.liquidArr:
            self.liquids.add(elements)
            self.all_sprites.add(elements)

    def handleEvents(self, events): # to be implemented
        pass

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        self.player.update(pressed_keys) # player physics and movement
        self.fallthrough.update() # to be implemented
        # self.blocks.update()
        # self.enemies.update() # to be implemented

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for entity in self.all_sprites:
            screen.blit(entity.surf, entity.rect)





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