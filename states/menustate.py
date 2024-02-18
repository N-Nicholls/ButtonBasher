import pygame
import pygame_menu
from states import gamestate


class MenuState(gamestate.GameState):
    def __init__(self, game):
            super().__init__(game)
        
    def handleEvents(self):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError

    def draw(self, screen):
        raise NotImplementedError