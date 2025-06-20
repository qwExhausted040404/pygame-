import pygame
from utils import *

class SandPile:
    def __init__(self, x, y, has_artifact=False):
        self.rect = pygame.Rect(x, y, 60, 10)  # Хитбокс кучи
        self.image = pygame.image.load("images/models/sand.png").convert_alpha()
        self.digging = False
        self.progress = 0  # 0-100%
        self.max_progress = 100
        self.dig_time = DIG_TIME  #время копания
        self.current_time = 0
        self.progress_bar = pygame.Rect(x, y - 10, 60, 5)  # Полоска прогресса
        
        self.font = pygame.font.Font(None, MAIN_FONT_SIZE)
        self.show_r = False
        self.digging_sound = pygame.mixer.Sound("music/sand.mp3")
        self.sound_playing = False
        self.digging_sound.set_volume(1)
        
        self.dug = False
        self.has_artifact = has_artifact
        
    def update(self, keys, alex):
        # Проверка на начало/продолжение копания
        if self.dug or (alex and alex.is_dead):  # Если куча уже выкопана или персонаж мертв
            if self.sound_playing:  # Останавливаем звук если он играет
                self.digging_sound.stop()
                self.sound_playing = False
            return
        
        self.show_r = alex.rect.colliderect(pygame.Rect(self.rect))
        was_digging = self.digging
        
        if (self.show_r and keys[pygame.K_f] and self.progress < self.max_progress):
            self.digging = True
            self.current_time += 1
            self.progress = (self.current_time / self.dig_time) * 100
        else:
            self.digging = False
            
        if self.digging and not was_digging:  # Если только начали копать
            self.digging_sound.play(loops=-1)  # Зацикливаем звук
            self.sound_playing = True
        elif not self.digging and was_digging:  # Если только закончили копать
            self.digging_sound.stop()
            self.sound_playing = False
        
        # Если прогресс завершен
        if self.progress >= self.max_progress:
            self.progress = self.max_progress
            self.dug = True
            if self.sound_playing:  # Останавливаем звук если куча выкопана
                self.digging_sound.stop()
                self.sound_playing = False
    
    def draw(self, screen):
        # Отрисовка кучи
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        if self.show_r and self.progress < self.max_progress:
            r_text = self.font.render("F", True, WHITE)
            screen.blit(r_text, (self.rect.x + 20, self.rect.y - 30))
            
        # Отрисовка прогресса (если куча еще не выкопана)
        if self.progress < self.max_progress:
            # Фон полоски
            pygame.draw.rect(screen, (50, 50, 50), self.progress_bar)
            # Заливка прогресса
            progress_width = int(60 * (self.progress / 100))
            progress_fill = pygame.Rect(self.progress_bar.x, self.progress_bar.y, progress_width, 5)
            pygame.draw.rect(screen, (220, 200, 0), progress_fill)