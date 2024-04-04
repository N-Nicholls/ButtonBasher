from objects.enemy import Enemy
from effects.effect import Effect

class Slime(Enemy):
    def __init__(self, game, pos, type = "sludge"):
        super().__init__(game, pos)
        self.speed /= 2
        self.canBreath = False
        self.type = type
        match type:
            case "sludge":
                self.level = 0
                self.effects.append(Effect("sludge", 50))
            case "fire":
                self.level = 1
                self.effects.append(Effect("fire", 50))
            case "jump":
                self.level = 2
                self.effects.append(Effect("jump", 50))
            case "ice":
                self.level = 3
                self.effects.append(Effect("ice", 50))
            case "redbull":
                self.level = 4
                self.effects.append(Effect("redbull", 50))
        self.setSheet("./sprites/slime.png")
    
    def update(self):
        self.effects[0].duration = 50
        # print(f"{self.effects[0].type} {self.effects[0].duration}")
        super().update()

    def returnSubclass(self):
        return "slime"