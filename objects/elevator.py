from objects.physchar import PhysChar
from core.vector import Vector

# IMPORTANT NOTE: THE CODE DOESN'T CHECK FOR ELEVATOR IN ELEVATOR SECTION OF LEVEL. IF U USE A ELEVATOR LAYER, ADD AN ELEVATOR
class Elevator(PhysChar):
    def __init__(self, game, position, speed = 1):
        super().__init__(game, position, "./sprites/error.png", False, False, 0.80, 0)
        self.speedMult = speed
        self.velocity = Vector(0, 0)
        self.path = []
        self.path.append(position)
        self.position = self.path[0]
        self.next = self.path[0]
        self.index = 0
        self.coolDown = 0
        self.isNode = True


    def update(self):
        # print(f"cooldown: {self.coolDown} position: {self.position[0]}, {self.position[1]} target: {self.index - 1} target position: {self.next[0]}, {self.next[1]}")
        if self.isNode == True:
            self.passable = 1
            self.surf.set_alpha(0)
            self.setSheet("./sprites/error.png") # testing purposes
        
        if self.coolDown > 0:
            self.coolDown -= 1
        if self.position == self.next:
            if self.isNode == False:
                self.coolDown += 1
            self.coolDown = self.game.frame_rate/4
            self.next = self.path[self.index]
            if self.index == len(self.path)-1:
                self.index = 0
            else:
                self.index += 1
        if self.coolDown <= 0:
            self.move()

    def addPath(self, pos):
        self.path.append(pos)

    def addBranch(self, other):
        other.isNode = False
        # Assuming you want to offset each new position by a fixed amount
        offset_x = -self.path[0][0] + other.path[0][0]
        offset_y = -self.path[0][1] + other.path[0][1]
        for position in self.path:
            # Calculate the new position with the given offset
            new_position = (position[0] + offset_x, position[1] + offset_y)
            other.path.append(new_position)


    def move(self):
        # self.velocity = (0, 0)
        self.position = (self.rect.centerx, self.rect.centery)
        self.velocity = Vector(self.next[0] - self.position[0], self.next[1] - self.position[1]).normalize() * self.speedMult
        self.moveSingleAxis(self.velocity.x, 0)
        self.moveSingleAxis(0, self.velocity.y)

    # elevator moving checking collision with objects, results in movement of object
    def moveSingleAxis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        for mobile in self.game.state.mobiles:
            if self.rect.colliderect(mobile.rect) and self.passable == 0 and mobile.passable == 0:
                    if dx > 0: # moving right
                        # self.rect.right = mobile.rect.left
                        mobile.rect.left = self.rect.right
                    if dx < 0: # moving left
                        # self.rect.left = mobile.rect.right
                        mobile.rect.right = self.rect.left
                    if dy > 0: # moving down
                        # self.rect.bottom = mobile.rect.top
                        mobile.rect.top = self.rect.bottom
                    if dy < 0: # moving up
                        # self.rect.top = mobile.rect.bottom
                        mobile.rect.bottom = self.rect.top


    def returnSubclass(self):
        return "elevator"
