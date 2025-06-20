import pygame
from utils import *

class ArtifactCounter:
    def __init__(self):
        self.collected = 0
        self.total = TOTAL_ARTIFACT
        self.font = pygame.font.Font(None, MAIN_FONT_SIZE)
        self.visible = False
        self.indent_width = 200
        self.indent_height = 480
        
    def collect(self):
        if self.collected < self.total:
            self.collected += 1
            self.visible = True
    
    def draw(self, screen):
        if self.visible:
            text = f"Артефакты: {self.collected}/{self.total}"
            text1 = self.font.render(text, True, DIALOG_COLOR)
            screen.blit(text1, (WIDTH - self.indent_width, HEIGHT - self.indent_height))