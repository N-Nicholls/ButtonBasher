from objects.enemy import Enemy


class Slime(Enemy):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.speed /= 2
        self.canBreath = False
        self.setSheet("./sprites/slime.png")

    def returnSubclass(self):
        return "slime"