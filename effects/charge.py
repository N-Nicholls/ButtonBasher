from objects.physchar import PhysChar
from core.vector import Vector
import random
import math

class Charge(PhysChar):
    def __init__(self, game, object,):
        # spawns them in a halfcircle around the objects
        max_diffX = min(15, 30 + game.block_size) 
        diffX = random.randint(-max_diffX, max_diffX)
        diffY = math.sqrt(15**2 - diffX**2)
        self.object = object
        self.game = game
        self.max_dist = 60
        super().__init__(game, (object.rect.center) , "./sprites/charge-sheet.png", False, False, 0, 0, )
        self.rect.x = object.rect.x +diffX*2
        self.rect.y = object.rect.y -diffY*2
        self.surf = self.sheet.image_at(1, 11, 11, 2, None, 0)
        self.gravity = Vector(0, 0)
        self.passable = 1

        # anim stuff
        self.timeMax = random.randint(60, 90)
        self.frame = random.randint(0, self.timeMax)
        self.killed = False

    def update(self):

        if self.killed == True:
            if self.frame > 11:
                self.kill()
            self.surf = self.sheet.image_at(self.frame, 11, 11, 2, None, 0)
            self.frame += 1
            return        

        if self.frame <= self.timeMax/2:
            self.surf = self.sheet.image_at(1, 11, 11, 2, None, 0)
        else:
            self.surf = self.sheet.image_at(2, 11, 11, 2, None, 0)
        self.frame+= 1
        if self.frame > self.timeMax:
            self.frame = 1

        # Calculate the vector from the charge to the object
        direction_vector = Vector(self.rect.x - self.object.rect.x, self.rect.y - self.object.rect.y)
        distance = abs(direction_vector)  # Calculate the distance to the object
        
        # If the distance is greater than the maximum allowed distance
        if distance > self.max_dist:
            # Normalize the direction vector
            if distance > 0:  # Ensure we don't divide by zero
                direction = direction_vector * (1 / distance)
            else:
                direction = Vector(0, 0)  # Handle the case where distance is zero
            
            # Calculate the new position to maintain the maximum distance
            new_position = Vector(self.object.rect.x, self.object.rect.y) + (direction * self.max_dist)
            
            # Update the charge's position
            self.rect.x = new_position.x
            self.rect.y = new_position.y

        # attraction
        self.velocity -= (Vector(self.rect.x, self.rect.y) - Vector(self.object.rect.x, self.object.rect.y))*0.005

        # repulsive force to charges
        for charge in self.object.charges: 
            if abs((Vector(self.rect.x, self.rect.y) - Vector(charge.rect.x, charge.rect.y))) < self.max_dist:
                self.velocity += (Vector(self.rect.x, self.rect.y) - Vector(charge.rect.x, charge.rect.y))*0.005

        super().update()

    def returnSubclass(self):
        return "charge"