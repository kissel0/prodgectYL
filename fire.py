from platforms import *

class Fire(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.y = y
        self.x = x
        self.image = pygame.image.load('images/fire1.png')
        self.image = pygame.transform.scale(self.image, (50, 50))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
