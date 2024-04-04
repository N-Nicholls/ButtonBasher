class Effect():
    def __init__(self, type, duration):
        self.type = type
        self.duration = duration

    def update(self):
        if self.duration > 0:
            self.duration -= 1