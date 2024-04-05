class Effect():
    def __init__(self, type, duration):
        self.type = type
        self.duration = duration

    def update(self):
        # print(self.duration)
        if self.duration > 0:
            self.duration -= 1