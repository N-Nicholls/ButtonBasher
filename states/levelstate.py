from states.gamestate import GameState
from objects.physchar import PhysChar
from objects.liquid import Liquid 
from objects.player import Player
from objects.fallthrough import FallThrough
from objects.conveyor import Conveyor
from objects.elevator import Elevator
from objects.enemy import Enemy
from pygame.locals import K_DOWN, K_UP, K_LEFT, K_RIGHT, K_ESCAPE
import pygame

# class to hold a level. Holds blocks and mobs and anything in a game instance
class LevelState(GameState):
    
    def __init__(self, level_file, game, controls):
        super().__init__(game)  
        # groups for rendering
        self.game = game
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.player = pygame.sprite.Group()
        self.fallthrough = pygame.sprite.Group()
        self.liquids = pygame.sprite.Group()
        self.elevator = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.mobiles = pygame.sprite.Group() # for generic moving block collision, like elevators
        
        self.controls = controls
        self.parseLevel(level_file, game)

        # events and timers
        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 1000) # add enemy every second, in ms

    def parseLevel(self, levelFile, game):
        currentLayer = None
        # arrays for accessing
        blockArr = []
        playerArr = []
        fallthroughArr = []
        liquidArr = []
        elevArr = []
        enemyArr = []
        x = game.offset
        y = game.offset

        # World is 1920x1080, each block is 30x30, so 64x36 blocks
        temp = [None, None, None, None, None, None, None, None, None, None] # for elevators
        with open(levelFile, 'r') as file:
            lines = file.readlines()
        for line in lines:
            line = line.strip()
            words = line.split()
            
            if not words:
                continue # Skip empty lines

            if words[0].lower() in ["main", "elevator", "enemy"]:
                currentLayer = words[0].lower()
                x, y = game.offset, game.offset
                continue
            elif words[0].lower() == "end":
                break

            if currentLayer:
                for col in line:
                    if currentLayer == "main":
                        if col == "B":  # block
                            blockArr.append(PhysChar(self.game, x, y, None, None, 0.85, 0, 139, 69, 19))
                        if col == "P": # player
                            playerArr.append(Player(self.game, self.controls, x, y))
                        if col == "R": # Redbull
                            blockArr.append(PhysChar(self.game, x, y, None, None, 1.05, 0, 255, 0, 0))
                        if col == "S": # Sludge
                            blockArr.append(PhysChar(self.game, x, y, None, None, 0.75, 0.2, 0, 255, 0))
                        if col == "I": # Ice
                            blockArr.append(PhysChar(self.game, x, y, None, None, 1, 0, 0, 0, 255))
                        if col == "G": # Granite
                            blockArr.append(PhysChar(self.game, x, y, None, None, 0.85, 0.3, 100, 100, 100))
                        if col == "J": # JumpPad
                            blockArr.append(PhysChar(self.game, x, y, None, None, 0.85, 1, 255, 0, 255))
                        if col == "F": # Fallthrough
                            fallthroughArr.append(FallThrough(self.game, x, y))
                        if col == "<": # conveyor left
                            blockArr.append(Conveyor(self.game, x, y, "left", 1))
                        if col == ">": # conveyor right
                            blockArr.append(Conveyor(self.game, x, y, "right", 1))
                        if col == "^": # conveyor up
                            blockArr.append(Conveyor(self.game, x, y, "up", 20))
                        if col == "V": # conveyor down
                            blockArr.append(Conveyor(self.game, x, y, "down", 10))
                        if col == "W": # water
                            liquidArr.append(Liquid(self.game, x, y, 0, 70, 255, 70, 0.98, 0.7))
                        if col == "L": # ladder
                            liquidArr.append(Liquid(self.game, x, y, 255, 255, 0, 150, 0.98, 0.6))
                        if col == "C": # concrete
                            liquidArr.append(Liquid(self.game, x, y, 255, 255, 255, 150, 0.94, 0.5999))
                    elif currentLayer == "elevator":
                        if col.isdigit():
                            temp[int(col)] = (x, y)
                    elif currentLayer == "enemy":
                        if col == "E":
                            enemyArr.append(Enemy(self.game, (x, y)))
                    x += game.block_size  # Move to the next block in the row
                y += game.block_size  # Move to the next row
                x = game.offset  # Reset x to the start of the next row
            for i in range(0, 10):
                if temp[i] and temp[i+1]:
                    elevArr.append(Elevator(self.game, temp[i], temp[i+1], 1))
                    temp[i] = None
                    temp[i+1] = None

        for elements in blockArr:
            self.blocks.add(elements)
            self.all_sprites.add(elements)
        for elements in playerArr:
            self.player.add(elements)
            self.mobiles.add(elements)
            self.all_sprites.add(elements)
        for elements in fallthroughArr:
            self.fallthrough.add(elements)
            self.blocks.add(elements)
            self.all_sprites.add(elements)
        for elements in liquidArr:
            self.liquids.add(elements)
            self.all_sprites.add(elements)
        for elements in elevArr:
            self.elevator.add(elements)
            self.blocks.add(elements)
            self.all_sprites.add(elements)
        for elements in enemyArr:
            self.enemies.add(elements)
            self.mobiles.add(elements)
            self.all_sprites.add(elements)

    def spawnEnemy(self, x, y):
        pass



    def handleEvents(self, events): # to be implemented
        pressed_keys = pygame.key.get_pressed()
        for event in events:
            if pressed_keys[K_ESCAPE]:
                    self.running = False
            elif event.type == self.ADDENEMY:
                '''new_enemy = Enemy()
                self.enemies.add(new_enemy)
                self.all_sprites.add(new_enemy)'''

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        self.player.update(pressed_keys) # player physics and movement
        self.elevator.update() # timer for elevators
        self.fallthrough.update() # timer for fallthrough blocks
        self.enemies.update() # enemy movement and collision

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for entity in self.all_sprites:
            screen.blit(entity.surf, entity.rect)





