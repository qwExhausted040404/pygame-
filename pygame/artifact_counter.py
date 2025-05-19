import pygame
from utils import *

class ArtifactCounter:
    def __init__(self):
        self.collected = 0
        self.total = 6
        self.font = pygame.font.Font(None, 36)
        self.visible = False
        
    def collect(self):
        if self.collected < self.total:
            self.collected += 1
            self.visible = True
    
    def draw(self, screen):
        if self.visible:
            text = f"Артефакты: {self.collected}/{self.total}"
            text1 = self.font.render(text, True, (220, 227, 23))
            screen.blit(text1, (WIDTH-200, HEIGHT-480))