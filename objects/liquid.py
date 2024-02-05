import pygame

# note: liquid modifies your new move speed, but doesn't actively slow you down like frictio
# because then you stop moving after awhile and gravity doesn't work. So you maintain speed inside
class Liquid(pygame.sprite.Sprite):
    """
    viscosity = 1 # lowers speed by a constant amount (scalar)
    buoyantForce = 0 # how much it pushes up
    effectFrames = 1 # how long the multiplier lasts

    def __init__(self, game, xpos, ypos, red = 0, green = 0, blue = 255, alpha = 100, vis = 1, buoy = 0):
        super(Liquid, self).__init__()
        self.surf = pygame.Surface((game.block_size, game.block_size))
        self.surf.fill((red, green, blue))
        self.rect = self.surf.get_rect(center = (xpos, ypos))
        self.surf.set_alpha(alpha)
        self.viscosity = vis
        self.buoyantForce = buoy

    def inside(self, pc):
        pc.viscosityConst = self.viscosity
        pc.buoyantConst = self.buoyantForce
        pc.effectFrames = self.effectFrames
        pc.IN_LIQUID = 1"""