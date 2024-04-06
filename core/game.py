from states.levelstate import LevelState
import pygame
import json

# game main class, handles main loop and changing of states
class Game():

    def __init__(self):
        
        # File path for the JSON file
        file_path = './core/config.json'

        # Reading the data back from the JSON file
        with open(file_path, 'r') as json_file:
            config_data_loaded = json.load(json_file)

        # Accessing the configuration data
        self.screen_width = config_data_loaded["screen"]["width"]
        self.screen_height = config_data_loaded["screen"]["height"]
        self.frame_rate = config_data_loaded["frameRate"]
        # self.default = {'right': pygame.K_l, 'left': pygame.K_QUOTE, 'up': pygame.K_p, 'down': pygame.K_SEMICOLON, 'escape': pygame.K_ESCAPE, 'enemy': pygame.K_1, 'button': pygame.K_2, 'player': pygame.K_3}
        self.controls = self.load_controls(config_data_loaded["controls"]) # needs to convert json strings to PYGAME consts

        self.block_size = self.screen_width/64 # maintains the ratio of 64x36 blocks for 16:9 resolution
        self.offset = self.block_size/2

        print(f'Screen Width: {self.screen_width}, Screen Height: {self.screen_height}, Frame Rate: {self.frame_rate}')

        # important initialize stuff
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.running = True

        # eventually should be main menu state
        self.state = LevelState("./levels/level3.txt", self, self.controls) # should be more comprehensive later

    def load_controls(self, controls_config):
        controls = {'right': pygame.K_l, 'left': pygame.K_QUOTE, 'up': pygame.K_p, 'down': pygame.K_SEMICOLON, 'escape': pygame.K_ESCAPE, 'enemy': pygame.K_1, 'button': pygame.K_2, 'player': pygame.K_3, 'slime': pygame.K_4}
        for action, key_name in controls_config.items():
            if isinstance(key_name, str):
                if hasattr(pygame, key_name):
                    controls[action] = getattr(pygame, key_name)
                else:
                    if action in self.controls:
                        # controls[action] = self.default[action]
                        print(f"Key specification for '{action}' not found, replacing with default '{self.controls[action]}'")
                    else:
                        print(f"Warning: Key specification for '{action}' is invalid and no default is provided")
            else:
                if action in self.controls:
                    # controls[action] = self.default[action]
                    print(f"Key specification for '{action}' was not a string or not found, replacing with default '{self.controls[action]}'")
                else:
                    print(f"Warning: Key specification for '{action}' is not a string and no default is provided. Found {type(key_name).__name__} instead.")
        return controls

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
        
            self.state.draw(self.screen)
            self.state.handleEvents(events)
            self.state.update()

            pygame.display.flip()
            self.clock.tick(self.frame_rate)

    def changeState(self, state):
        self.state = state

    def quit(self):
        pygame.quit()