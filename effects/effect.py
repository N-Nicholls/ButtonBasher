class Effect():
    def __init__(self, type, duration):
        self.type = type
        self.duration = duration
        self.friction = .85
        self.elasticity = 0
        match type:
            case "sludge":
                self.friction = 0.75
                self.elasticity = 0
            case "fire":
                self.friction = 0.85
                self.elasticity = 0
            case "jump":
                self.friction = 0.85
                self.elasticity = 1 
            case "ice":
                self.friction = 1
                self.elasticity = 0
            case "redbull":
                self.friction = 1.05
                self.elasticity = 0

    def update(self):
        # print(self.duration)
        if self.duration > 0:
            self.duration -= 1
        else:
            print("deleted self")
            del self