from pygame.locals import *
from platforms import *
from main import *
class Cactus(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.y = y
        self.x = x
        self.image = pygame.image.load('images/cactus_bricks.png')
        self.image = pygame.transform.scale(self.image, (50, 50))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

