import pygame 
from utils import WIDTH, HEIGHT
from Alex import Alex 
from enemies import Tigers
from locations import *
from artifact_counter import ArtifactCounter
from Game_menu import *

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ловушка времени")
        icon = pygame.image.load('images/teleport.png').convert_alpha()
        pygame.display.set_icon(icon)
        
        self.menu = GameMenu(self)
        self.clock = pygame.time.Clock()
        self.current_location = None
        self.alex = None
        self.enemies = []
        self.setup_location(Locations1)
        self.artifact_counter = ArtifactCounter()
        
    def setup_location(self, location_class):
        self.current_location = location_class()
        if isinstance(self.current_location, Locations1):
            self.alex = None
            self.enemies = []
        elif isinstance(self.current_location, Locations2):
            self.alex = Alex(100, 400)
            self.enemies = []
        elif isinstance(self.current_location, Locations3):
            self.alex = Alex(100, 400)
            self.enemies = []

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.menu.handle_event(event)
            
            if not self.menu.active:
                self.update_game()
                
            self.draw_game()
            
            pygame.display.update()
            self.clock.tick(60)
        
        pygame.quit()

    def update_game(self):
        """Обновление игрового состояния"""
        keys = pygame.key.get_pressed()
        
        # Обновление текущей локации
        if isinstance(self.current_location, Locations1):
            self.current_location.update(keys)
        elif isinstance(self.current_location, Locations2):
            self.current_location.update(keys, self.alex, self)
        elif isinstance(self.current_location, Locations3):
            self.current_location.update(keys)
        
        # Обновление персонажа
        if self.alex:
            self.alex.update(keys)
        
        # Проверка завершения локации
        if self.current_location.finished:
            if isinstance(self.current_location, Locations1):
                self.setup_location(Locations2)
            elif isinstance(self.current_location, Locations2):
                self.setup_location(Locations3)
                
    def draw_game(self):
        """Отрисовка всех игровых объектов"""
        self.current_location.draw(self.screen)
        
        if self.alex:
            self.alex.draw(self.screen, pygame.key.get_pressed())

        self.artifact_counter.draw(self.screen)
        self.menu.draw(self.screen)
        
        
def main():
    game = GameManager()
    game.run()

if __name__ == "__main__":
    main()