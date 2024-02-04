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