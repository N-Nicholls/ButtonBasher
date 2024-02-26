from states.gamestate import GameState
from objects.physchar import PhysChar
from objects.liquid import Liquid 
from objects.player import Player
from objects.fallthrough import FallThrough
from objects.conveyor import Conveyor
from objects.elevator import Elevator
from objects.enemy import Enemy
from objects.button import Button
from objects.spike import Spike
from effects.gib import Gib
from effects.sword import Sword

import pygame
import random

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
        self.enemies = pygame.sprite.Group() # called for pathfinding and movement
        self.mobiles = pygame.sprite.Group() # for generic moving block collision, like elevators, shouldn't be called to move
        self.buttons = pygame.sprite.Group()
        self.gibs = pygame.sprite.Group()
        self.conveyor = pygame.sprite.Group() # just to update the sprite, probably not efficient
        
        self.controls = controls
        self.parseLevel(level_file, game)

        # events and timers
        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 1000) # add enemy every second, in ms

    def parseLevel(self, levelFile, game):
        currentLayer = None
        # arrays for accessing
        blockArr = []
        fallthroughArr = []
        liquidArr = []
        elevArr = []
        convArr = []

        # spawn points
        self.playerArr = []
        self.enemyArr = []
        self.buttonArr = []
        x = game.offset
        y = game.offset
        self.COOLDOWN = 0

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
                            blockArr.append(PhysChar(self.game, (x, y), "./sprites/brick.png", True, False, 0.85, 0, ))
                        if col == "P": # player
                            self.playerArr.append((x, y))
                        if col == "R": # Redbull
                            blockArr.append(PhysChar(self.game, (x, y), "./sprites/redbull.png", True, False, 1.05, 0))
                        if col == "S": # Sludge
                            blockArr.append(PhysChar(self.game, (x, y), "./sprites/sludge.png", True, False, 0.75, 0.2, ))
                        if col == "I": # Ice
                            blockArr.append(PhysChar(self.game, (x, y), "./sprites/ice.png", True, False, 1, 0, ))
                        if col == "G": # Granite
                            blockArr.append(PhysChar(self.game, (x, y), "./sprites/granite.png", True, True, 0.85, 0.3))
                        if col == "J": # JumpPad
                            blockArr.append(PhysChar(self.game, (x, y), "./sprites/jump.png", False, True, 0.85, 1, ))
                        if col == "F": # Fallthrough
                            fallthroughArr.append(FallThrough(self.game, (x, y)))
                        if col == "<": # conveyor left
                            convArr.append(Conveyor(self.game, (x, y), "left", 1))
                        if col == ">": # conveyor right
                            convArr.append(Conveyor(self.game, (x, y), "right", 1))
                        if col == "^": # conveyor up
                            convArr.append(Conveyor(self.game, (x, y), "up", 20))
                        if col == "V": # conveyor down
                            convArr.append(Conveyor(self.game, (x, y), "down", 10))
                        if col == "W": # water
                            liquidArr.append(Liquid(self.game, (x, y), "./sprites/error.png", False, False, 70, 0.98, 0.7))
                        if col == "L": # ladder
                            liquidArr.append(Liquid(self.game, (x, y), "./sprites/ladder.png", False, False, 150, 0.94, 0.6))
                        if col == "C": # concrete
                            liquidArr.append(Liquid(self.game, (x, y), "./sprites/error.png", False, False, 150, 0.94, 0.5999))
                        if col == "@": # button
                            self.buttonArr.append((x, y))
                        if col == "E":
                            self.enemyArr.append((x, y))
                        if col == "7":
                            blockArr.append(Spike(self.game, (x,y)))
                    elif currentLayer == "elevator":
                        if col.isdigit():
                            temp[int(col)] = (x, y)
                    elif currentLayer == "enemy":
                        pass
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
        for elements in convArr:
            self.blocks.add(elements)
            self.conveyor.add(elements)
            self.all_sprites.add(elements)
        

    def spawnEnemy(self):
        choice = random.choice(self.enemyArr)
        temp = Enemy(self.game, choice)
        self.enemies.add(temp)
        self.mobiles.add(temp)
        self.all_sprites.add(temp)

    def spawnButton(self):
        choice = random.choice(self.buttonArr) # chooses random button to spawn button
        temp = Button(self.game, choice)
        self.mobiles.add(temp)
        self.buttons.add(temp)
        self.all_sprites.add(temp)
    
    def spawnPlayer(self):
        choice = random.choice(self.playerArr)
        temp = Player(self.game, self.controls, choice)
        self.player.add(temp)
        self.mobiles.add(temp)
        self.all_sprites.add(temp)

    def gibbed(self, pos, intensity):
        for _ in range(intensity):
            temp = Gib(self.game, (pos))
            self.gibs.add(temp)
            self.all_sprites.add(temp)

    def sword(self, pos, direction):
        temp = Sword(self.game, pos, direction)
        self.gibs.add(temp)
        self.all_sprites.add(temp)

    def handleEvents(self, events): 
        pressed_keys = pygame.key.get_pressed()
        for event in events:
            if pressed_keys[self.game.controls['enemy']] and self.COOLDOWN == 0:
                self.spawnEnemy()
                self.COOLDOWN = 3
            if pressed_keys[self.game.controls['button']] and self.COOLDOWN == 0:
                self.spawnButton()
                self.COOLDOWN = 3
            if pressed_keys[self.game.controls['player']] and self.COOLDOWN == 0:
                self.spawnPlayer()
                self.COOLDOWN = 3
            if event.type == self.ADDENEMY:
                # self.spawnEnemy()
                pass

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        self.gibs.update() # gib stuff
        self.player.update(pressed_keys) # player physics and movement
        self.elevator.update() # timer for elevators
        self.fallthrough.update() # timer for fallthrough blocks
        self.enemies.update() # enemy movement and collision
        self.buttons.update()
        self.conveyor.update()
        if self.COOLDOWN > 0:
            self.COOLDOWN -= 1

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for entity in self.all_sprites:
            screen.blit(entity.surf, entity.rect)





