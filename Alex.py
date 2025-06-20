import pygame
from utils import *
from locations import *


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
        
        self.hitbox_width = HITBOX_WIDTH_ALEX
        self.hitbox_height = HITBOX_HEIGHT_ALEX
        self.hitbox_x = HITBOX_X_ALEX
        self.hitbox_y = HITBOX_Y_ALEX
        
        self.x = x
        self.y = y
        
        self.rect = pygame.Rect(
            self.x + self.hitbox_x,
            self.y + self.hitbox_y,
            self.hitbox_width,
            self.hitbox_height
        )
        
        self.hit_sound = pygame.mixer.Sound("music/hit.mp3")
        self.max_health = MAX_HEALTH_ALEX
        self.health = self.max_health
        self.health_images = [
            pygame.image.load("images/HP_3.png").convert_alpha(),
            pygame.image.load("images/HP_2.png").convert_alpha(),
            pygame.image.load("images/HP_1.png").convert_alpha()
        ]
        
        # Параметры персонажа
        self.speed = SPEED_ALEX
        self.count_anim = 0
        self.left_or_right = 'right'
        
        # Параметры прыжка
        self.gravity = ALEX_GRAVITY
        self.initial_speed = ALEX_INITIAL_SPEED
        self.is_jump = False
        self.jump_speed = 0
        self.on_the_ground = True

        self.platforms = []  # Сюда будем передавать платформы из локации
        self.velocity_y = 0  # Вертикальная скорость (для плавного падения)
        
        self.is_dead = False # Флаг смерти (True когда игрок умер)
        self.death_timer = 0 # Таймер для анимации смерти
        self.death_duration = ALEX_DEATH_DURATION # Длительность смерти в кадрах (3 сек при 60 FPS)
        
        self.bullets = []
        self.shoot_cooldown = 0
        self.shoot_sound = pygame.mixer.Sound("music/shot.mp3")
        
        self.stones = []  # список активных камней
        self.throw_cooldown = 0  # перезарядка броска
        
    def update(self, keys, game_manager):
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
        if keys[pygame.K_w] and self.on_the_ground:
            self.velocity_y = -self.initial_speed
            self.is_jump = True
            self.on_the_ground = False
        
        if self.throw_cooldown > 0:
            self.throw_cooldown -= 1
            
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1    
        
        for bullet in self.bullets[:]:
            if not bullet.update(self.platforms) or not bullet.is_alive():
                self.bullets.remove(bullet)
        
        if isinstance(game_manager.current_location, Locations3):
            for stone in self.stones[:]:
                stone.update(self.platforms)
                if not stone.is_alive():
                    self.stones.remove(stone)
                
        # Применяем гравитацию
        self.apply_gravity()
        
        # Проверяем коллизии с платформами
        self.check_collisions()
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

        for stone in self.stones:
            stone.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)
            
    def throw_stone(self, target_x, target_y, game_manager):
        if not isinstance(game_manager.current_location, Locations3):
            return
        
        if self.throw_cooldown <= 0:
            start_x = self.x + self.hitbox_x + self.hitbox_width // 2
            start_y = self.y + self.hitbox_y
            self.stones.append(Stone(start_x, start_y, target_x, target_y))
            self.throw_cooldown = THROW_COOLDOWN  # небольшая задержка между бросками
    
    def shoot(self, target_x, target_y, game_manager):
        if self.shoot_cooldown <= 0:
            self.shoot_sound.play()
            start_x = self.x + self.hitbox_x + self.hitbox_width // 2
            start_y = self.y + self.hitbox_y + 10
            self.bullets.append(Bullet(start_x, start_y, target_x, target_y))
            self.shoot_cooldown = SHOOT_COOLDOWN  # небольшая задержка между выстрелами
            
    def take_damage(self):
        self.hit_sound.play()
        if self.health > 1:
            self.health -= 1
        elif self.health == 1:
            self.health -= 1
            self.dead()
                
    def dead(self):
        self.is_dead = True # Активируем состояние смерти
        self.death_timer = self.death_duration
    
    def reset(self, x, y):
        self.x = x                    # Возвращаем начальную позицию X
        self.y = y                    # Возвращаем начальную позицию Y
        self.health = self.max_health # Полное восстановление HP
        self.is_dead = False          # Сбрасываем флаг смерти
        self.death_timer = 0          # Обнуляем таймер
        self.velocity_y = 0
        
    def draw_health(self, screen):
        if 1 <= self.health <= 3:
            screen.blit(self.health_images[3 - self.health], (10, 10))
            
    def apply_gravity(self):
        self.velocity_y += self.gravity  # Ускоряем падение
        self.y += self.velocity_y
    
    def check_collisions(self):
        self.on_the_ground = False  # Предполагаем, что персонаж в воздухе
        # Обновляем хитбокс
        self.rect.x = self.x + self.hitbox_x
        self.rect.y = self.y + self.hitbox_y
        
        for platform in self.platforms:
            if not self.rect.colliderect(platform.rect):
                continue
                
            # Определяем направление столкновения
            overlap_x = min(self.rect.right - platform.rect.left, platform.rect.right - self.rect.left)
            overlap_y = min(self.rect.bottom - platform.rect.top, platform.rect.bottom - self.rect.top)
            
            # Боковое столкновение (горизонтальное)
            if overlap_x < overlap_y:
                if self.rect.centerx < platform.rect.centerx:  # Слева
                    self.rect.right = platform.rect.left
                else:  # Справа
                    self.rect.left = platform.rect.right
                self.x = self.rect.x - self.hitbox_x  # Синхронизируем X
                
            # Вертикальное столкновение (сверху/снизу)
            else:
                if self.rect.centery < platform.rect.centery:  # Сверху
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_the_ground = True
                    self.is_jump = False
                else:  # Снизу
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
                self.y = self.rect.y - self.hitbox_y  # Синхронизируем Y

class Stone:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("images/models/shells/stone.png").convert_alpha()
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        
        #скорость
        self.speed = SPEED_STONE
        
        # Рассчитываем направление к цели
        dx = target_x - x
        dy = target_y + 50 - y
        distance = (dx**2 + dy**2)**0.5 
        
        # Нормализуем и умножаем на скорость
        self.velocity_x = (dx / distance) * self.speed
        self.velocity_y = (dy / distance) * self.speed
        
        # Гравитация
        self.gravity = STONE_GRAVITY
        self.lifetime = LIFETIME_STONE  # время жизни в кадрах (2 сек)
    
    def update(self, platforms):
        self.x += self.velocity_x
        self.velocity_y += self.gravity  # применяем гравитацию
        self.y += self.velocity_y
        self.lifetime -= 1

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.lifetime = 0  # камень исчезает при попадании в платформу
                break
            
    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))
    
    def is_alive(self):
        return self.lifetime > 0 and self.y < HEIGHT  # исчезает при выходе за экран или по времени
    

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("images/models/shells/bullet.png").convert_alpha()
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.speed = SPEED_BULLET
        
        # Рассчитываем направление
        dx = target_x - x
        dy = target_y - y
        distance = (dx**2 + dy**2)**0.5
        
        self.velocity_x = (dx / distance) * self.speed
        self.velocity_y = (dy / distance) * self.speed
    
    def update(self, platforms):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Проверяем столкновение с платформами
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                return False  # пуля уничтожается
        return True  # пуля продолжает полёт
    
    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))
    
    def is_alive(self):
        # Пуля исчезает при выходе за границы экрана
        return (0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT)