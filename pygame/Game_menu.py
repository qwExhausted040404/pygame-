import pygame
from utils import *

class GameMenu:
    def __init__(self, game):
        self.game = game
        self.active = False
        self.font = pygame.font.Font('font/font_2.ttf', 48)
        self.font_name_game = pygame.font.Font('font/font_1.ttf', 80)
        self.background = pygame.image.load("images/game_menu.jpg").convert()
        self.width, self.height = 1000, 500
        self.background = pygame.transform.scale(self.background, (self.width, self.height))#transform - масштабирует изображение под наши размеры
        
        # Настройки меню
        self.x = (WIDTH - self.width) // 2
        self.y = (HEIGHT - self.height) // 2
        
        # Громкость (0.0 - 1.0)
        self.volume = 0.5

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.active = not self.active
        
        if not self.active:#выходим если меню закрыто
            return
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()#Получает текущие координаты курсора мыши если был клик
            
            # Проверяем клик по кнопкам
            if self.continue_game.collidepoint(mouse_pos):#если нажато на продолжить
                self.active = False
            elif self.quit_game.collidepoint(mouse_pos):#если нажато выйти
                pygame.quit()
                exit()
            elif self.slider_rect.collidepoint(mouse_pos):#Если клик был по ползунку громкости
                # Обновляем громкость
                self.volume = (mouse_pos[0] - self.slider_rect.x) / self.slider_rect.width#переделать в случае чего, вычисляет новую громкость
                pygame.mixer.music.set_volume(self.volume)

    def draw(self, screen):
        if not self.active:#выходим если меню не активно
            return
        
        # Создаем прямоугольники для элементов
        self.continue_game = pygame.Rect(self.x + 358, self.y + 220, 300, 45)
        self.slider_rect = pygame.Rect(self.x + 358, self.y + 300, 300, 20)
        self.quit_game = pygame.Rect(self.x + 358, self.y + 350, 300, 45)
        
        # Фон меню
        screen.blit(self.background, (self.x, self.y))
        
        name_game = self.font_name_game.render('Ловушка времени', True, (220, 227, 23))
        screen.blit(name_game, (self.x + 195, self.y + 30))
        
        # Кнопка "Продолжить"
        pygame.draw.rect(screen, (45, 144, 237), self.continue_game)
        text = self.font.render("Продолжить", True, (220, 227, 23))
        screen.blit(text, (self.continue_game.x + 45, self.continue_game.y-3))
        
        # Ползунок громкости
        pygame.draw.rect(screen, (100, 100, 100), self.slider_rect)
        pygame.draw.rect(screen, (200, 200, 0), (
            self.slider_rect.x, 
            self.slider_rect.y, 
            int(self.slider_rect.width * self.volume), 
            self.slider_rect.height
        ))
        
        # Кнопка "Выйти"
        pygame.draw.rect(screen, (45, 144, 237), self.quit_game)
        text = self.font.render("Выйти", True, (220, 227, 23))
        screen.blit(text, (self.quit_game.x + 100, self.quit_game.y-3))