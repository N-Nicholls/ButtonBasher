from objects.physchar import PhysChar
from core.vector import Vector

class Button(PhysChar):
    def __init__(self, game, pos, direction = "up"):
        super().__init__(game, pos, "./sprites/button.png", False, False, 0.92, 0, coverable = (0,0,0,0))
        self.pressed = False
        self.direction = direction

    def update(self):
        super().update()

    def onBottom(self, pc):
        return super().onBottom(pc)
    
    def onLeft(self, pc):
        return super().onLeft(pc)
    
    def onRight(self, pc):
        return super().onRight(pc)
    
    def onTop(self, pc):
        return super().onTop(pc)
    

    def returnSubclass(self):
        return "button"

    def returnMobile(self):
        return True