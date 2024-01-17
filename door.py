import pygame
from platforms import *
from main import *

class Door(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.y = y
        self.x = x
        self.image = pygame.image.load('door1.png')
        self.image = pygame.transform.scale(self.image, (70, 70))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
