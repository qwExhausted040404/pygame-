import pygame

class Enemy():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0
        self.health = 100
        self.rect = pygame.Rect(x, y, 32, 32)
        
    
    def update(self, keys): 
        
        pass
    
    def draw(self, screen, keys):
        
        pass
    
    
    
class Tigers(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.walk_left = [
            pygame.image.load("images/models/tiger(1).png").convert_alpha(),
            pygame.image.load("images/models/tiger(2).png").convert_alpha(),
            pygame.image.load("images/models/tiger(1).png").convert_alpha(),
            pygame.image.load("images/models/tiger(2).png").convert_alpha()
        ]
        
        self.walk_right = [
            pygame.image.load("images/models/tiger(3).png").convert_alpha(),
            pygame.image.load("images/models/tiger(4).png").convert_alpha(),
            pygame.image.load("images/models/tiger(3).png").convert_alpha(),
            pygame.image.load("images/models/tiger(4).png").convert_alpha()
        ]
        
        self.x = x
        self.y = y
        
        self.hitbox_width = 40
        self.hitbox_height = 51
        self.hitbox_x = 3
        self.hitbox_y = 10
        self.direction = 'left'
        
        self.rect = pygame.Rect(
            self.x + self.hitbox_x,
            self.y + self.hitbox_y,
            self.hitbox_width,
            self.hitbox_height
        )
        
        self.speed = 8
        self.count_anim = 0
        self.anim_speed = 0.15  # Скорость анимации (чем меньше, тем медленнее)
        self.current_frame = 0  # Текущий кадр (дробный для плавности)
    
    def update(self):
        # Плавное обновление анимации
        self.current_frame += self.anim_speed
        if self.current_frame >= len(self.walk_left):
            self.current_frame = 0
        
        self.count_anim = int(self.current_frame)  # Округляем до целого
        
        # Движение
        self.x -= self.speed
        self.rect.x = self.x + self.hitbox_x
    
    def draw(self, screen):
        screen.blit(self.walk_left[self.count_anim], (self.x, self.y))