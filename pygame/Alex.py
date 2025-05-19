import pygame
from utils import WIDTH, HEIGHT

class Alex:
    def __init__(self, x, y):
        # Загрузка анимаций
        self.walk_left = [
            pygame.image.load("images/models/left(1).png").convert_alpha(),
            pygame.image.load("images/models/left(2).png").convert_alpha(),
            pygame.image.load("images/models/left(3).png").convert_alpha(),
            pygame.image.load("images/models/left(4).png").convert_alpha()
        ]
        
        self.walk_right = [
            pygame.image.load("images/models/right(1).png").convert_alpha(),
            pygame.image.load("images/models/right(2).png").convert_alpha(),
            pygame.image.load("images/models/right(3).png").convert_alpha(),
            pygame.image.load("images/models/right(4).png").convert_alpha()
        ]
        self.hitbox_width = 40
        self.hitbox_height = 51
        self.hitbox_x = 3
        self.hitbox_y = 10
        
        self.x = x
        self.y = y
        
        self.rect = pygame.Rect(
            self.x + self.hitbox_x,
            self.y + self.hitbox_y,
            self.hitbox_width,
            self.hitbox_height
        )
        
        # Параметры персонажа
        self.speed = 5.5
        self.count_anim = 0
        self.left_or_right = 'right'
        
        # Параметры прыжка
        self.gravity = 1.2
        self.initial_speed = 16
        self.is_jump = False
        self.jump_speed = 0
        self.on_the_ground = True
    
    def update(self, keys):
        # Обработка анимации
        if self.count_anim == 3:
            self.count_anim = 0
        else:
            self.count_anim += 1
        
        # Обработка направления персонажа
        if keys[pygame.K_a]:
            self.left_or_right = 'left'
        elif keys[pygame.K_d]:
            self.left_or_right = 'right'
        
        # Обработка движения
        if keys[pygame.K_a] and self.x > 2:
            self.x -= self.speed
        elif keys[pygame.K_d] and self.x < WIDTH - 45:
            self.x += self.speed
        
        # Обработка прыжка
        if not self.is_jump and keys[pygame.K_w] and self.on_the_ground:
            self.is_jump = True
            self.on_the_ground = False
            self.jump_speed = -self.initial_speed
        if self.is_jump:
            self.y += self.jump_speed
            self.jump_speed += self.gravity
            if self.y >= HEIGHT - 100:
                self.y = HEIGHT - 100
                self.is_jump = False
                self.on_the_ground = True
                self.jump_speed = 0
    
        #изменение хитбокса
        self.rect.x = self.x + self.hitbox_x
        self.rect.y = self.y + self.hitbox_y
        
    def draw(self, screen, keys):
        
        if keys[pygame.K_a]:
            screen.blit(self.walk_left[self.count_anim], (self.x, self.y))
        elif keys[pygame.K_d]:
            screen.blit(self.walk_right[self.count_anim], (self.x, self.y))
        else:
            if self.left_or_right == 'left':
                screen.blit(self.walk_left[0], (self.x, self.y))
            elif self.left_or_right == 'right':
                screen.blit(self.walk_right[0], (self.x, self.y))