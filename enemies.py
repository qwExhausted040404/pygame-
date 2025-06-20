import pygame
import random
from utils import *

class Enemy():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0
        self.health = 100
        self.rect = pygame.Rect(x, y, 32, 32)
        self.animation_count = 0
        self.animation_speed = 0
    
    def update(self, keys): 
        pass
    
    def draw(self):
        pass
    
    def animation(self):
        self.animation_count += self.animation_speed
        if self.animation_count >= len(self.walk_left):
            self.animation_count = 0
            
    def check_platform_collisions(self):
        """Базовая проверка коллизий с платформами"""
        self.on_ground = False
        
        for platform in self.platforms:
            if not self.rect.colliderect(platform.rect):
                continue

            overlap_x = min(self.rect.right - platform.rect.left, 
                          platform.rect.right - self.rect.left)
            overlap_y = min(self.rect.bottom - platform.rect.top, 
                          platform.rect.bottom - self.rect.top)
            
            if overlap_x < overlap_y:  # Боковое столкновение
                if self.rect.centerx < platform.rect.centerx:
                    self.rect.right = platform.rect.left
                else:
                    self.rect.left = platform.rect.right
                self.x = self.rect.x
            else:  # Вертикальное столкновение
                if self.rect.centery < platform.rect.centery:  # На платформе
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.y = self.rect.y
                else:  # Удар головой
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
                    self.y = self.rect.y
                    
    def draw_health_bar(self, screen):
        """Отрисовка health bar"""
        health_width = (self.health / self.max_health) * self.health_bar_width
        health_x = self.x + 10 + (self.rect.width - self.health_bar_width) / 2
        health_y = self.y - 10
        
        # Фон (красный)
        pygame.draw.rect(screen, (255, 0, 0), 
                        (health_x, health_y, 
                        self.health_bar_width, self.health_bar_height))
        # Текущее здоровье (зелёный)
        pygame.draw.rect(screen, (0, 255, 0), 
                        (health_x, health_y, 
                        health_width, self.health_bar_height))
    
    
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
        
        self.hitbox_width = HITBOX_WIDTH_TIGER
        self.hitbox_height = HITBOX_HEIGHT_TIGER
        self.hitbox_x = HITBOX_X_TIGER
        self.hitbox_y = HITBOX_Y_TIGER
        
        self.direction = random.choice(['left', 'right'])  # Случайное начальное направление
        
        self.rect = pygame.Rect(
            self.x + self.hitbox_x,
            self.y + self.hitbox_y,
            self.hitbox_width,
            self.hitbox_height
        )
        
        # Параметры движения
        self.speed = SPEED_TIGER
        self.count_anim = 0
        self.animation_speed = ANIMATIONS_SPEED
        
        # Параметры прыжка
        self.gravity = TIGER_GRAVITY
        self.velocity_y = 0
        self.velocity_x = 0  # Горизонтальная скорость при прыжке
        self.jump_power = 0
        self.on_ground = False
        self.is_jumping = False
        
        # Параметры атаки
        self.detection_radius = TIGER_DETECTION_RADIUS
        self.attack_cooldown = 0
        self.attack_cooldown_max = TIGER_COOLDOWN
        self.attack_damage = 1
        
        # Здоровье
        self.max_health = TIGER_MAX_HEALTH
        self.health = self.max_health
        self.health_bar_width = 40
        self.health_bar_height = 5
        
        # Платформы
        self.platforms = []
        
    def update(self, alex):
        # Обновление анимации
        
        self.animation()

        # Гравитация
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        
        # Движение по горизонтали
        if self.is_jumping:
            new_x = self.x + self.velocity_x
            # Проверяем, чтобы не выйти за границы экрана
            if 0 <= new_x <= WIDTH - self.rect.width:
                self.x = new_x
            else:
                # Если достигли границы, останавливаем горизонтальное движение
                self.velocity_x = 0
                
        else:
            # Патрулирование
            if self.direction == 'left':
                self.x -= self.speed
            else:
                self.x += self.speed
            
            # Проверка границ экрана
            if self.x < 0:
                self.x = 0
                self.direction = 'right'
            elif self.x > WIDTH - self.rect.width:
                self.x = WIDTH - self.rect.width
                self.direction = 'left'
        
        # Проверка коллизий с платформами
        self.check_platform_collisions()
        
        # Обновление хитбокса
        self.rect.x = self.x + self.hitbox_x
        self.rect.y = self.y + self.hitbox_y
        
        # Логика прыжка на игрока
        if not self.is_jumping and self.on_ground and self.attack_cooldown <= 0:
            #Формула: sqrt((x2 - x1)^2 + (y2 - y1)^2)
            distance_to_player = ((self.rect.centerx - alex.rect.centerx)**2 + 
                                (self.rect.centery - alex.rect.centery)**2)**0.5
            
            if distance_to_player < self.detection_radius:
                self.jump_to_target(alex.rect.centerx, alex.rect.top, distance_to_player)
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # Проверка столкновения с игроком
        if self.rect.colliderect(alex.rect) and self.is_jumping:
            alex.take_damage()
            self.is_jumping = False
            self.attack_cooldown = self.attack_cooldown_max
            
    def jump_to_target(self, target_x, target_y, distance):
        if self.is_jumping or self.attack_cooldown > 0:  # Уже в прыжке или перезарядка
            return
       
        dx = target_x - self.rect.centerx
        dy = (target_y - 40) - self.rect.centery
        
        # Устанавливаем скорость прыжка
        speed = TIGER_SPEED_JUMP # Общая скорость прыжка
        
        # Рассчитываем новую целевую позицию, чтобы не вылететь за границы
        new_target_x = min(WIDTH - self.rect.width, target_x)
        dx = new_target_x - self.rect.centerx
        
        self.velocity_x = (dx / distance) * speed
        self.velocity_y = (dy / distance) * speed
        
        self.is_jumping = True
        self.on_ground = False
        if dx > 0:
            self.direction = 'right'
        else:
            self.direction = 'left'

        # Активируем перезарядку сразу после прыжка
        self.attack_cooldown = self.attack_cooldown_max
        
    def check_platform_collisions(self):
        self.on_ground = False
        
        for platform in self.platforms:
            if not self.rect.colliderect(platform.rect):
                continue
            
            # Определяем направление столкновения
            overlap_x = min(self.rect.right - platform.rect.left, 
                          platform.rect.right - self.rect.left)
            overlap_y = min(self.rect.bottom - platform.rect.top, 
                          platform.rect.bottom - self.rect.top)
            
            if overlap_x < overlap_y:  # Боковое столкновение
                if self.rect.centerx < platform.rect.centerx:
                    self.rect.right = platform.rect.left
                    self.x = self.rect.x - self.hitbox_x
                    self.velocity_x = 0  # Останавливаем горизонтальное движение
                else:
                    self.rect.left = platform.rect.right
                    self.x = self.rect.x - self.hitbox_x
                    self.velocity_x = 0  # Останавливаем горизонтальное движение
            else:  # Вертикальное столкновение
                if self.velocity_y > 0:  # Падаем вниз (на платформу)
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.is_jumping = False
                    self.y = self.rect.y - self.hitbox_y
                else:  # Движемся вверх (удар головой)
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
                    self.y = self.rect.y - self.hitbox_y

    def take_damage(self):
        """Обработка получения урона"""
        self.health -= 1
        return self.health <= 0  # Возвращает True, если здоровье закончилось
        
    def draw(self, screen):
        # Отрисовка тигра
        if self.direction == 'left':
            screen.blit(self.walk_left[int(self.animation_count)], (self.x, self.y))
        else:
            screen.blit(self.walk_right[int(self.animation_count)], (self.x, self.y))
            
        # Отрисовка здоровья
        self.draw_health_bar(screen)

class Crossbow(Enemy):
    def __init__(self, x, y, direction):
        super().__init__(x, y)
        self.image_right = pygame.image.load("images/models/crossbow_right.png").convert_alpha()
        self.image_left = pygame.image.load("images/models/crossbow_left.png").convert_alpha()
        self.direction = direction  # "left" или "right"
        self.rect = pygame.Rect(x, y, 40, 30)
        self.cooldown = 0
        self.cooldown_max = 0  # Задержка между выстрелами (в кадрах)
        self.arrows = []  # Список активных стрел
        self.min_cooldown = 110
        self.min_cooldown = 300
        
    def update(self, alex):        
        if self.cooldown <= 0:
            self.shoot()
            self.cooldown = random.randint(self.min_cooldown, self.min_cooldown)
        else:
            self.cooldown -= 1

        # Обновляем стрелы
        for arrow in self.arrows[:]:
            arrow.update()
            if arrow.rect.x < 0 or arrow.rect.x > WIDTH:
                self.arrows.remove(arrow)
            elif arrow.rect.colliderect(alex.rect):
                alex.take_damage()
                if arrow in self.arrows:
                    self.arrows.remove(arrow)

    def shoot(self):
        if self.direction == "left":
            arrow = Arrow(self.rect.x, self.rect.centery, "left")
        else:
            arrow = Arrow(self.rect.right, self.rect.centery, "right")
        self.arrows.append(arrow)

    def draw(self, screen):
        # Отрисовка арбалета
        if self.direction == 'right':
            screen.blit(self.image_right, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.image_left, (self.rect.x, self.rect.y))
        # Отрисовка стрел
        for arrow in self.arrows:
            arrow.draw(screen)


class Arrow:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y+20, 30, 5)
        if direction == "right":
            self.speed = SPEED_ARROW
        else:
            self.speed = -(SPEED_ARROW)
        self.direction = direction
        self.image = pygame.image.load("images/models/shells/arrow_right.png").convert_alpha()
        if direction == "left":
            self.image = pygame.image.load("images/models/shells/arrow_left.png").convert_alpha()

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y-12))
        
class Zombie(Enemy):
    def __init__(self, x, y):
        
        self.walk_right = [
            pygame.image.load("images/models/zombie(1).png").convert_alpha(),
            pygame.image.load("images/models/zombie(2).png").convert_alpha(),
            pygame.image.load("images/models/zombie(3).png").convert_alpha(),
            pygame.image.load("images/models/zombie(4).png").convert_alpha(),
            pygame.image.load("images/models/zombie(5).png").convert_alpha(),
            pygame.image.load("images/models/zombie(6).png").convert_alpha(),
            pygame.image.load("images/models/zombie(7).png").convert_alpha()
        ]
        
        self.walk_left = [
            pygame.image.load("images/models/zombie(8).png").convert_alpha(),
            pygame.image.load("images/models/zombie(9).png").convert_alpha(),
            pygame.image.load("images/models/zombie(10).png").convert_alpha(),
            pygame.image.load("images/models/zombie(11).png").convert_alpha(),
            pygame.image.load("images/models/zombie(12).png").convert_alpha(),
            pygame.image.load("images/models/zombie(13).png").convert_alpha(),
            pygame.image.load("images/models/zombie(14).png").convert_alpha()
        ]
        
        self.x = x
        self.y = y
        self.speed = SPEED_ZOMBIE
        self.direction = random.choice([LEFT, RIGHT])  # -1 - влево, 1 - вправо
        self.animation_count = 0
        self.rect = pygame.Rect(x, y, 40, 60)
        self.damage_cooldown = 0
        self.animation_speed = ANIMATIONS_SPEED 
        
    def update(self, alex):
        # Обновление анимации
        self.animation()
        # Движение зомби
        self.x += self.speed * self.direction
        self.rect.x = self.x
        
        # Разворот у краев экрана
        if self.x < 0 or self.x > WIDTH - 40:
            self.direction *= -1
        
        # Проверка столкновения с игроком
        if self.rect.colliderect(alex.rect) and self.damage_cooldown <= 0:
            alex.take_damage()
            self.damage_cooldown = DAMAGE_COOLDOWN_ZOMBIE  # Задержка 1 секунда (60 кадров)
        
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1


    def draw(self, screen):
        if self.direction < 0:  # Движение влево
            screen.blit(self.walk_left[int(self.animation_count)], (self.x, self.y))
        else:  # Движение вправо
            screen.blit(self.walk_right[int(self.animation_count)], (self.x, self.y))

class Ghost:
    def __init__(self, y):
        #случайные параметры
        self.speed = random.uniform(3.0, 7.0)
        self.direction = random.choice([LEFT, RIGHT])  # -1 - слева направо, 1 - справа налево
        
        #Загружаем соответствующее изображение
        if self.direction > 0:
            self.image = pygame.image.load("images/models/ghost_right.png").convert_alpha()
            self.x = GHOST_APPEARANCE_LEFT_X  # Появление слева
        else:
            self.image = pygame.image.load("images/models/ghost_left.png").convert_alpha()
            self.x = WIDTH  # Появление справа
            
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.active = True

        
        
    def update(self):
        # Движение призрака
        self.x += self.speed * self.direction
        self.rect.x = self.x
        
        # Проверка выхода за границы
        if (self.direction > 0 and self.x > WIDTH) or (self.direction < 0 and self.x < -60):
            self.active = False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
                   
class Robot(Enemy):
    def __init__(self, x, y, is_main_platform=False):
        super().__init__(x, y)
        # Загрузка анимаций
        self.stay_right = pygame.image.load("images/models/robot(7).png").convert_alpha()
        self.stay_left = pygame.image.load("images/models/robot(15).png").convert_alpha()
        self.walk_right = [
            pygame.image.load("images/models/robot(1).png").convert_alpha(),
            pygame.image.load("images/models/robot(2).png").convert_alpha(),
            pygame.image.load("images/models/robot(3).png").convert_alpha(),
            pygame.image.load("images/models/robot(4).png").convert_alpha(),
            pygame.image.load("images/models/robot(5).png").convert_alpha(),
            pygame.image.load("images/models/robot(6).png").convert_alpha(),
            pygame.image.load("images/models/robot(7).png").convert_alpha(),
            pygame.image.load("images/models/robot(8).png").convert_alpha()
        ]
        self.walk_left = [
            pygame.image.load("images/models/robot(9).png").convert_alpha(),
            pygame.image.load("images/models/robot(10).png").convert_alpha(),
            pygame.image.load("images/models/robot(11).png").convert_alpha(),
            pygame.image.load("images/models/robot(12).png").convert_alpha(),
            pygame.image.load("images/models/robot(13).png").convert_alpha(),
            pygame.image.load("images/models/robot(14).png").convert_alpha(),
            pygame.image.load("images/models/robot(15).png").convert_alpha(),
            pygame.image.load("images/models/robot(16).png").convert_alpha()
        ]
        self.shoot_image = pygame.image.load("images/models/shells/robot-bullet.png").convert_alpha()
        
        self.x = x
        self.y = y
        self.speed = SPEED_ROBOT
        self.direction = random.choice([LEFT, RIGHT])  # -1 - влево, 1 - вправо
        self.animation_count = 0
        self.animation_speed = ANIMATIONS_SPEED
        self.rect = pygame.Rect(x, y, 40, 60)
        self.health = ROBOT_HEALTH   # Количество попаданий для уничтожения
        self.max_health = ROBOT_HEALTH 
        self.shoot_cooldown = 0
        self.shoot_delay = ROBOT_SHOOT_DELAY  # Задержка между выстрелами (в кадрах)
        self.bullets = []
        self.platforms = []
        self.health_bar_width = 40
        self.health_bar_height = 5
        
        self.on_ground = False
        self.velocity_y = 0
        self.gravity = 0.8
        
        self.is_main_platform = is_main_platform
        self.shoot_timer = 0
        
        # Новые свойства для эффекта телепортации
        self.is_spawning = True
        self.spawn_timer = ROBOT_SPAWN_TIMER  # 2 секунды
        self.alpha = 0
        self.current_image = self.stay_right
        
    def update(self, alex):
        # Логика появления
        if self.is_spawning:
            self.spawn_timer -= 1
            self.alpha = ALPHA  - (self.spawn_timer * 2) # Плавное появление
            
            # Завершение появления
            if self.spawn_timer <= 0:
                self.is_spawning = False
                self.alpha = ALPHA
            return  # Не обновляем логику, пока появляется
        
        # Обновление анимации
        if self.is_main_platform:
            self.animation()

            self.x += self.speed * self.direction
            self.rect.x = self.x
            
            # Проверка краев экрана
            if self.direction > 0 and self.rect.right > WIDTH:
                self.x = WIDTH - self.rect.width
                self.direction *= -1
            elif self.direction < 0 and self.rect.left < 0:
                self.x = 0
                self.direction *= -1
                
        # Гравитация
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        self.rect.y = self.y
        
        # Проверка коллизий с платформами
        self.check_platform_collisions()
        
        # Стрельба
        if self.shoot_cooldown <= 0 and self.on_ground:
            self.shoot(alex)
            self.shoot_cooldown = self.shoot_delay
        elif self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # Обновление пуль
        for bullet in self.bullets[:]:
            if bullet.update(self.platforms):
                self.bullets.remove(bullet)
            elif bullet.rect.colliderect(alex.rect):
                alex.take_damage()
                self.bullets.remove(bullet)

    def check_platform_collisions(self):
        """Проверка коллизий с платформами"""
        self.on_ground = False
        
        for platform in self.platforms:
            if not self.rect.colliderect(platform.rect):
                continue

            overlap_x = min(self.rect.right - platform.rect.left, 
                           platform.rect.right - self.rect.left)
            overlap_y = min(self.rect.bottom - platform.rect.top, 
                           platform.rect.bottom - self.rect.top)
            
            if overlap_x < overlap_y:  # Боковое столкновение
                if self.rect.centerx < platform.rect.centerx:
                    self.rect.right = platform.rect.left
                else:
                    self.rect.left = platform.rect.right
                self.x = self.rect.x
            else:  # Вертикальное столкновение
                if self.rect.centery < platform.rect.centery:  # Сверху (на платформе)
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.y = self.rect.y
                else:  # Снизу (удар головой)
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
                    self.y = self.rect.y
                    
    def shoot(self, alex):
        bullet = RobotBullet(self.rect.centerx, self.rect.centery, 
                           alex.rect.centerx, alex.rect.centery, self.direction)
        self.bullets.append(bullet)
        
    
    def take_damage(self):
        self.health -= 1
        return self.health <= 0
    
    def draw(self, screen):
        # Выбираем изображение для отрисовки
        if self.is_spawning:
            if self.direction > 0:
                self.current_image = self.stay_right
            else:
                self.current_image = self.stay_left
            
        elif self.is_main_platform:
            if self.shoot_cooldown > self.shoot_delay - 10:  # Анимация выстрела
                self.current_image = self.shoot_image
                
            else:
                if self.direction < 0:
                    self.current_image = self.walk_left[int(self.animation_count)]
                else:
                    self.current_image = self.walk_right[int(self.animation_count)]
        else:
            if self.x < WIDTH/2:
                self.current_image = self.stay_right
                self.direction = 1
            else:
                self.current_image = self.stay_left
                self.direction = -1
        
        # Применяем прозрачность при появлении
        if self.is_spawning:
            temp_image = self.current_image.copy()
            temp_image.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(temp_image, (self.x, self.y))
        else:
            screen.blit(self.current_image, (self.x, self.y))
        
        # Рисуем пули
        for bullet in self.bullets:
            bullet.draw(screen)
            
        # Рисуем здоровье
        self.draw_health_bar(screen)

class RobotBullet:
    def __init__(self, x, y, target_x, target_y, direction):
        self.image = pygame.image.load("images/models/shells/robot-bullet.png").convert_alpha()
        
        # Определяем начальную позицию в зависимости от направления
        if direction > 0:  # Если робот смотрит вправо
            self.x = x + 48  # Смещение от центра робота вправо
            self.y = y + 10  # Небольшое смещение по Y
        else:  # Если робот смотрит влево
            self.x = x - 33  # Смещение от центра робота влево
            self.y = y + 10
        
        self.rect = pygame.Rect(self.x, self.y, 10, 5)
        self.speed = SPEED_ROBOT_BULLET
        self.direction = direction
        
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

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                return True  # Пуля должна исчезнуть
        return False
    
    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))
        
        
