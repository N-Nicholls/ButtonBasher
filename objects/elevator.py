from objects.physchar import PhysChar
from core.vector import Vector

class Elevator(PhysChar):
    def __init__(self, game, path):
        super().__init__(game, path[0][0], path[0][1], game.block_size, game.block_size, 0.95, 0, 100, 100, 100)
        self.path = path
        self.path_index = 0  # Keep track of the current index in the path
        self.position = path[self.path_index]
        self.next = path[(self.path_index + 1) % len(path)]  # Use modulo for looping

    def update(self):
        if self.position != self.next:
            self.move(self.next)
            # Check if the elevator has reached its next position
            if Vector(self.rect.x, self.rect.y) == Vector(self.next[0], self.next[1]):
                self.position = self.next
                # Update path_index to move to the next position in the path, loop if at the end
                self.path_index = (self.path_index + 1) % len(self.path)
                self.next = self.path[self.path_index]

    def move(self, pos):
        # Assuming Vector is a class that supports vector arithmetic
        direction = Vector(pos[0], pos[1]) - Vector(self.rect.x, self.rect.y)
        direction = direction.normalize()  # Normalize direction for consistent speed
        self.move_single_axis(direction.x, 0)
        self.move_single_axis(0, direction.y)

    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy






"""class Elevator(PhysChar):
    def __init__(self, game, path):
        super().__init__(game, path[0][0], path[0][1], game.block_size, game.block_size, 0.95, 0, 100, 100, 100)
        self.position = path[0]
        self.path = path
        self.next = path[1]

    def update(self):
        if self.position != self.next:
            self.move(self.next)

    def move(self, pos):
        direction = Vector(pos[0], pos[1]) - Vector(self.rect.x, self.rect.y)
        self.rect.x += direction.x
        self.rect.y += direction.y"""
