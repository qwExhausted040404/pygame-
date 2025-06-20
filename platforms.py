import pygame 
from utils import *
class Platform:
    def __init__(self, x, y, width, height, image_path=None):
        self.rect = pygame.Rect(x, y, width, height)
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = None
    
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, GREY, self.rect)
