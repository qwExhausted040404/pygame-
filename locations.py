import pygame
import random
from utils import WIDTH, HEIGHT
from platforms import *
from enemies import *
from item_other import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Locations:
    def __init__(self):
        self.background = None
        self.font = pygame.font.Font(None, MAIN_FONT_SIZE)
        self.finished = False
        self.background_music = None
        self.music_volume = BASE_VOLUME
        self.music_playing = False
        self.interactive_obj = {}
        self.platforms = []
        self.dialogs = []
        
    def update(self, keys, alex=None, game_manager=None):
        pass
    
    def draw(self, screen):
        screen.blit(self.background, (0, 0))
    
    def setup_music(self):
        if self.background_music:
            pygame.mixer.music.load(self.background_music)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
    
    def draw_platforms(self, screen):
        for i, platform in enumerate(self.platforms):
            if i != 0:
                platform.draw(screen)
                
                
class Locations1(Locations):
    def __init__(self):
        super().__init__()
        self.current_dialog = 0
        self.background_music = "music/1-2_Locations_music.mp3"
        self.background = pygame.image.load("images/locations/location_1.jpg").convert()
        self.dialogs = [
            "Алекс: Еще одно заброшенное здание... Как же я люблю этот момент — первый взгляд на забытое место.",
            "Алекс: Что скрывают эти стены? Может, здесь остались вещи прошлых хозяев... Или что-то более необычное.",
            "Алекс: Этот дом явно видел лучше дни. Окна разбиты, двери сорваны... Но в этом есть своя мрачная красота.",
            "Алекс: Чем старше здание, тем больше у него историй. А это... Похоже, здесь творилось что-то недоброе.",
            "Алекс: Почему люди бросают такие места? Страх? Проклятие? Или просто время не пощадило их?",
            "Алекс: Ладно, хватит раздумий. Пора зайти внутрь и узнать правду."
        ]
        self.space_pressed = False
        
        self.max_symbol_in_str = 70
        
    def setup_music(self):
         super().setup_music()
        
    def update(self, keys):
        if keys[pygame.K_SPACE] and not self.space_pressed:
            self.space_pressed = True
            self.current_dialog += 1
            if self.current_dialog >= len(self.dialogs):
                self.finished = True
        elif not keys[pygame.K_SPACE]:
            self.space_pressed = False
    
    def draw(self, screen):
        super().draw(screen)  
        if self.current_dialog < len(self.dialogs):
            dialog = self.dialogs[self.current_dialog]
            if len(dialog) > self.max_symbol_in_str:
                split_pos = dialog.rfind(' ', 0, self.max_symbol_in_str)
                text = self.font.render(self.dialogs[self.current_dialog][:split_pos], True, DIALOG_COLOR)
                screen.blit(text, (20, HEIGHT - 120))
                text1 = self.font.render(self.dialogs[self.current_dialog][split_pos:], True, DIALOG_COLOR)
                screen.blit(text1, (300, HEIGHT - 70))
            else:
                text = self.font.render(self.dialogs[self.current_dialog][:self.max_symbol_in_str], True, DIALOG_COLOR)
                screen.blit(text, (20, HEIGHT - 120))
                text1 = self.font.render(self.dialogs[self.current_dialog][self.max_symbol_in_str:], True, DIALOG_COLOR)
                screen.blit(text1, (300, HEIGHT - 70))
                
                
class Locations2(Locations):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("images/locations/location_2.jpg").convert()
        self.background_music = "music/2_Locations_music.mp3"
        self.show_message = True
        self.message_start_time = pygame.time.get_ticks()#содержит в себе время перехода на вторую локацию
        self.message_duration = 3000 
        self.message_text = "Что... Почему дверь заперлась? Как мне выбраться? Что это там за вещичка"
        self.message1_start_time = 0
        self.interactive_obj = {
            'rect': pygame.Rect(WIDTH - 100, HEIGHT - 100, 100, 100),  # Зона взаимодействия
            'image': pygame.image.load("images/models/artefacts/artefact_1.png").convert_alpha(),
            'show_e': False,
            'collected': False,
            'message': "Вы нашли древний артефакт!",
            'message1': "Найдите 6 артефактов, иначе будете заперты НАВСЕГДА!!!",
            'message_shown': False,
            'message_shown1': False,
            'message_duration': self.message_duration  # 3 секунды
        }
        self.platforms = [Platform(0, HEIGHT - 50, WIDTH, 50)]
    
    def setup_music(self):
         super().setup_music()
         
    def update(self, keys, alex, game_manager):
        current_time = pygame.time.get_ticks()#это время от начала запуска программы 
        if current_time - self.message_start_time >= self.message_duration:#тут мы смотрим разницу между временем запуска игры и временем перехода на вторую локацию
            self.show_message = False
            
        if not self.interactive_obj['collected']:
            self.interactive_obj['show_e'] = alex.rect.colliderect(self.interactive_obj['rect'])
            if self.interactive_obj['show_e'] and keys[pygame.K_e]:
                self.interactive_obj['collected'] = True
                self.interactive_obj['message_shown'] = True
                self.message_start_time = pygame.time.get_ticks()
                game_manager.artifact_counter.collect()
                
        else:
            if self.interactive_obj['message_shown'] and current_time - self.message_start_time > self.interactive_obj['message_duration']:
                self.interactive_obj['message_shown'] = False
                self.interactive_obj['message_shown1'] = True
                self.message1_start_time = pygame.time.get_ticks()
                
        if self.interactive_obj['message_shown1'] and current_time - self.message1_start_time > self.interactive_obj['message_duration']:
            self.interactive_obj['message_shown1'] = False
            self.finished = True
            
    def draw(self, screen):
        super().draw(screen)
        if self.show_message:
            text = self.font.render(self.message_text, True, DIALOG_COLOR)
            screen.blit(text, (WIDTH - 950, HEIGHT - 40))
            
        if not self.interactive_obj['collected']:
            screen.blit(self.interactive_obj['image'], self.interactive_obj['rect'])
            if self.interactive_obj['show_e']:
                font = pygame.font.Font(None, MAIN_FONT_SIZE)
                e_text = font.render("E", True, WHITE)
                screen.blit(e_text, (self.interactive_obj['rect'].x + 40, self.interactive_obj['rect'].y - 30))
                
        if self.interactive_obj['message_shown']:
            text = self.font.render(self.interactive_obj['message'], True, DIALOG_COLOR)
            screen.blit(text, (WIDTH - 700, HEIGHT//2))
        
        if self.interactive_obj['message_shown1']:
            text1 = self.font.render(self.interactive_obj['message1'], True, DIALOG_COLOR)
            screen.blit(text1, (WIDTH - 900, HEIGHT//2))
            

class Locations3(Locations):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("images/locations/location_3.jpg").convert()
        self.background_music = "music/3_Locations_music.mp3"
        self.interactive_obj = {
            'rect': pygame.Rect(WIDTH - 105, HEIGHT - 445, 100, 50),  # Зона взаимодействия
            'image': pygame.image.load("images/models/artefacts/artefact_2.png").convert_alpha(),
            'show_e': False,
            'collected': False,
            'enemies_killed': False
        }
        self.platforms = [
            Platform(-100, HEIGHT - 90, WIDTH + 200, 30),  # Основная земля
            Platform(400, 300, 150, 20, "images/models/platforms/forest_platform.png"),
            Platform(700, 250, 200, 20, "images/models/platforms/forest_platform.png"),
            Platform(150, 250, 150, 20, "images/models/platforms/forest_platform.png"),
            Platform(20, 150, 110, 20, "images/models/platforms/forest_platform.png"),
            Platform(220, 100, 150, 20, "images/models/platforms/forest_platform.png"),
            Platform(850, 100, 125, 20, "images/models/platforms/forest_platform.png"),
            Platform(530, 103, 170, 20, "images/models/platforms/forest_platform.png")
        ]
    
    def setup_music(self):
         super().setup_music()
         
    def update(self, keys, alex, game_manager):
        alex.platforms = self.platforms
        
        if not self.interactive_obj['collected']:
            self.interactive_obj['show_e'] = alex.rect.colliderect(self.interactive_obj['rect'])
            if self.interactive_obj['show_e'] and self.interactive_obj['enemies_killed'] and  keys[pygame.K_e]:
                self.interactive_obj['collected'] = True
                self.interactive_obj['message_shown'] = True
                self.message_start_time = pygame.time.get_ticks()
                self.finished = True
                game_manager.artifact_counter.collect()
            
    def draw(self, screen):
        super().draw(screen)
        #отрисовка платформ, кроме первой
        self.draw_platforms(screen)
        
        #
        if not self.interactive_obj['collected'] and not self.interactive_obj['enemies_killed']:
            screen.blit(self.interactive_obj['image'], self.interactive_obj['rect'])
            if self.interactive_obj['show_e']:
                font = pygame.font.Font(None, 55)
                e_text = font.render("X", True, RED)
                screen.blit(e_text, (self.interactive_obj['rect'].x + 10, self.interactive_obj['rect'].y))
                
        elif not self.interactive_obj['collected'] and self.interactive_obj['enemies_killed']:
            screen.blit(self.interactive_obj['image'], self.interactive_obj['rect'])
            if self.interactive_obj['show_e']:
                font = pygame.font.Font(None, MAIN_FONT_SIZE)
                e_text = font.render("E", True, WHITE)
                screen.blit(e_text, (self.interactive_obj['rect'].x + 40, self.interactive_obj['rect'].y - 10))
            
        
class Locations4(Locations):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("images/locations/location_4.jpg").convert()
        self.background_music = "music/4_Locations_music.mp3"
        
        self.platforms = [
            Platform(0, HEIGHT - 90, WIDTH, 10),  # Основная земля
            Platform(450, 350, 150, 20, "images/models/platforms/sand_platform.png"),
            Platform(700, 257, 200, 20, "images/models/platforms/sand_platform.png"),
            Platform(150, 250, 180, 20, "images/models/platforms/sand_platform.png"),
            Platform(220, 140, 150, 20, "images/models/platforms/sand_platform.png"),
            Platform(850, 107, 125, 20, "images/models/platforms/sand_platform.png"),
            Platform(530, 103, 50, 20, "images/models/platforms/sand_platform.png")
        ]
        self.moving_platform = self.platforms[-1]  # Сохраняем ссылку на движущуюся платформу
        self.moving_direction = RIGHT  # 1 - вправо, -1 - влево
        self.moving_speed = SPEED_PLATFORM
        self.right_border_platform = 700
        self.left_border_platform = 400
        
        self.sand_piles = [
            SandPile(500, HEIGHT - 185),
            SandPile(200, HEIGHT - 120),
            SandPile(770, HEIGHT - 274),
            SandPile(265, HEIGHT - 395),
            SandPile(875, HEIGHT - 425) 
        ]
        artifact_pile = random.choice(self.sand_piles[-2:])
        artifact_pile.has_artifact = True
        
        self.crossbows = [
        Crossbow(-28, HEIGHT - 410, "right"),
        Crossbow(-28, HEIGHT - 230, "right"),
        Crossbow(WIDTH - 46, HEIGHT - 320, "left"),
        Crossbow(WIDTH - 46, HEIGHT - 140, "left")
        ]
        
        self.artifact = {
            'rect': pygame.Rect(0, 0, 50, 50),
            'image': pygame.image.load("images/models/artefacts/artefact_3.png").convert_alpha(),
            'show_e': False,
            'collected': False,
            'active': False
        }
    
    def setup_music(self):
         super().setup_music()
               
    def update(self, keys, alex, game_manager):
        self.prev_platform_x = self.moving_platform.rect.x
        self.moving_platform.rect.x += self.moving_direction * self.moving_speed
        # Меняем направление, если платформа достигла границ
        if (self.moving_platform.rect.x > self.right_border_platform) or (self.moving_platform.rect.x < self.left_border_platform):
            self.moving_direction *= -1
            
        alex.platforms = self.platforms
        for crossbow in self.crossbows:
            crossbow.update(alex)
        
        for pile in self.sand_piles[:]:  # Делаем копию списка для безопасного удаления
            pile.update(keys, alex)
            if pile.dug:
                # Если это куча с артефактом - активируем артефакт
                if hasattr(pile, 'has_artifact') and pile.has_artifact:
                    self.artifact['rect'].x = pile.rect.x
                    self.artifact['rect'].y = pile.rect.y - 5
                    self.artifact['active'] = True
                self.sand_piles.remove(pile)
        
        if self.artifact['active'] and not self.artifact['collected']:
            self.artifact['show_e'] = alex.rect.colliderect(self.artifact['rect'])
            if self.artifact['show_e'] and keys[pygame.K_e]:
                self.artifact['collected'] = True
                game_manager.artifact_counter.collect()
                self.finished = True
            
    def draw(self, screen):
        super().draw(screen)
        self.draw_platforms(screen)
                    
        for crossbow in self.crossbows:
            crossbow.draw(screen)

        for pile in self.sand_piles:
            pile.draw(screen)
            
        if self.artifact['active'] and not self.artifact['collected']:
            screen.blit(self.artifact['image'], self.artifact['rect'])
            if self.artifact['show_e']:
                font = pygame.font.Font(None, MAIN_FONT_SIZE)
                e_text = font.render("E", True, WHITE)
                screen.blit(e_text, (self.artifact['rect'].x + 20, self.artifact['rect'].y - 30))
                
                
class Locations5(Locations):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("images/locations/location_5.png").convert()
        self.background_music = "music/5_Locations_music.mp3"
        
        self.artifact = {
            'rect': pygame.Rect(500, 298, 50, 50),
            'image': pygame.image.load("images/models/artefacts/artefact_4.png").convert_alpha(),
            'show_e': False,
            'collected': False,
            'active': False
        }
        
        self.platforms = [
            Platform(0, HEIGHT - 40, WIDTH, 10),  # Основная земля
            Platform(450, 350, 150, 20, "images/models/platforms/stone_platform.png"),
            Platform(700, 257, 200, 20, "images/models/platforms/stone_platform.png"),
            Platform(150, 250, 180, 20, "images/models/platforms/stone_platform.png"),
            Platform(220, 140, 150, 20, "images/models/platforms/stone_platform.png"),
            Platform(850, 107, 125, 20, "images/models/platforms/stone_platform.png"),
            Platform(530, 103, 50, 20, "images/models/platforms/stone_platform.png")
        ]
        
        self.ghost_heights = [90, 220, 310]
        # Список активных призраков
        self.ghosts = []
        # Таймеры для респауна каждого призрака
        self.ghost_timers = [0, 0, 0]
            
        self.level_timer = LEVEL_TIMER
        self.font = pygame.font.Font(FONT_NAME, LARGE_FONT_SIZE)
        
        for i in range(3):
            self.spawn_ghost(i)
    
    def setup_music(self):
         super().setup_music()
         
    def spawn_ghost(self, index):
        """Создает нового призрака на заданной высоте"""
        if self.level_timer <= 0:
            return  # Не спавним новых если время вышло
            
        y = self.ghost_heights[index]
        self.ghosts.append(Ghost(y))
        # Устанавливаем случайный таймер до следующего появления (1-4 секунды)
        if index == 0:
            self.ghost_timers[index] = random.randint(120, 190)
        else:
            self.ghost_timers[index] = random.randint(200, 350)
            
    def update(self, keys, alex, game_manager):
        alex.platforms = self.platforms
        
        # Обновление таймера уровня
        if self.level_timer > 0:
            self.level_timer -= 1
        else:
            self.artifact['active'] = True
            
        if self.artifact['active'] and not self.artifact['collected']:
            self.artifact['show_e'] = alex.rect.colliderect(self.artifact['rect'])
            if self.artifact['show_e'] and keys[pygame.K_e]:
                self.artifact['collected'] = True
                game_manager.artifact_counter.collect()
                self.finished = True
            
        # Обновление призраков
        for ghost in self.ghosts[:]:
            ghost.update()
            if ghost.rect.colliderect(alex.rect):
                alex.take_damage()
                self.ghosts.remove(ghost)
            elif not ghost.active:
                self.ghosts.remove(ghost)
                
        # Обновление таймеров респауна
        for i in range(3):
            if self.ghost_timers[i] > 0:
                self.ghost_timers[i] -= 1
            else:
                self.spawn_ghost(i)
        
        if self.artifact['active'] and not self.artifact['collected']:
            self.artifact['show_e'] = alex.rect.colliderect(self.artifact['rect'])
            if self.artifact['show_e'] and keys[pygame.K_e]:
                self.artifact['collected'] = True
                game_manager.artifact_counter.collect()
                self.finished = True
                
    def draw(self, screen):
        super().draw(screen)
        self.draw_platforms(screen)
        
        for ghost in self.ghosts:
            ghost.draw(screen)
            
        minutes = self.level_timer // (60 * 60)
        seconds = (self.level_timer % (60 * 60)) // 60
        timer_text = f"{minutes:02}:{seconds:02}"
        text_surface = self.font.render(timer_text, True, WHITE)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 20))
        
        if self.artifact['active'] and not self.artifact['collected']:
            screen.blit(self.artifact['image'], self.artifact['rect'])
            if self.artifact['show_e']:
                font = pygame.font.Font(None, MAIN_FONT_SIZE)
                e_text = font.render("E", True, WHITE)
                screen.blit(e_text, (self.artifact['rect'].x + 20, self.artifact['rect'].y - 30))


class Locations6(Locations):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("images/locations/location_6.jpg").convert()
        self.background_music = "music/6_Locations_music.mp3"
        
        self.artifact = {
            'rect': pygame.Rect(495, 315, 50, 50),
            'image': pygame.image.load("images/models/artefacts/artefact_5.png").convert_alpha(),
            'show_e': False,
            'collected': False,
            'active': False
        }
        
        self.platforms = [
            Platform(0, HEIGHT - 28, WIDTH, 30, "images/models/platforms/fire_platform(1).png"),  # Основная земля
            Platform(370, 370, 280, 20, "images/models/platforms/fire_platform(1).png"),
            Platform(700, 257, 200, 20, "images/models/platforms/fire_platform(2).png"),
            Platform(120, 270, 180, 20, "images/models/platforms/fire_platform(1).png"),
            Platform(-100, 140, 260, 20, "images/models/platforms/fire_platform(2).png"),
            Platform(840, 140, 260, 20, "images/models/platforms/fire_platform(1).png"),
            Platform(570, 305, 50, 20, "images/models/platforms/fire_platform(2).png")
        ]
        
        # Изначальные роботы
        self.robots = [
            Robot(104, 85, False),# На верхней платформе
            Robot(835, 85, False),# На верхней платформе 
            Robot(800, 430, True),# На основной платформе
            Robot(600, 430, True)
        ]
        
        for robot in self.robots:
            robot.platforms = self.platforms
            robot.is_spawning = False  # Изначальные роботы уже появились
        
        self.robots_killed = 0
        self.max_robots = 16
        self.not_spawn_robots = 13
        self.font = pygame.font.Font(FONT_NAME, MAIN_FONT_SIZE)
        
        self.moving_platform = self.platforms[-1]
        self.moving_direction = 1
        self.moving_speed = SPEED_PLATFORM
        self.max_border_platform = 305
        self.min_border_platform = 70
        self.spawn_main_platform = 420
        self.spawn_upper_platforms = -80
        
    def setup_music(self):
         super().setup_music()
         
    def spawn_robot(self, x, y, is_main_platform):
        """Создает нового робота с эффектом телепортации"""
        robot = Robot(x, y, is_main_platform)
        robot.platforms = self.platforms
        robot.is_spawning = True
        robot.spawn_timer = 120
        if x < WIDTH // 2:
            robot.direction = 1  # Вправо
        else:
            robot.direction = -1  # Влево
        robot.alpha = 0
        self.robots.append(robot)
        return robot
        
    def update(self, keys, alex, game_manager):
        # Движение платформы
        self.moving_platform.rect.y += self.moving_direction * self.moving_speed
        if self.moving_platform.rect.y < self.min_border_platform or self.moving_platform.rect.y > self.max_border_platform:
            self.moving_direction *= -1
            
        alex.platforms = self.platforms
        
        for robot in self.robots[:]:
            robot.update(alex)
            
            for bullet in alex.bullets[:]:
                if bullet.rect.colliderect(robot.rect):
                    if robot.take_damage():
                        # Определяем платформу робота
                        on_main_platform = False
                        for platform in self.platforms:
                            if pygame.Rect(robot.rect.x, robot.rect.bottom, robot.rect.width, 1).colliderect(platform.rect):
                                on_main_platform = (platform == self.platforms[0])
                                break
                        
                        self.robots.remove(robot)
                        self.robots_killed += 1
                        
                        if self.robots_killed < self.not_spawn_robots:
                            if on_main_platform:
                                # Спавн нового робота на основной платформе
                                x = random.randint(50, WIDTH - 50)
                                y = self.spawn_main_platform
                                new_robot = self.spawn_robot(x, y, True)
                                new_robot.direction = random.choice([LEFT, RIGHT])
                            else:
                                # Спавн на других платформах
                                x = robot.rect.x
                                y = self.spawn_upper_platforms
                                self.spawn_robot(x, y, False)
                    
                    alex.bullets.remove(bullet)
                    break
        
        # Активация артефакта после убийства всех роботов
        if self.robots_killed == self.max_robots and not self.artifact['active']:
            self.artifact['active'] = True
            
        if self.artifact['active'] and not self.artifact['collected']:
            self.artifact['show_e'] = alex.rect.colliderect(self.artifact['rect'])
            if self.artifact['show_e'] and keys[pygame.K_e]:
                self.artifact['collected'] = True
                game_manager.artifact_counter.collect()
                self.finished = True
    
    def draw(self, screen):
        super().draw(screen)
        self.draw_platforms(screen)
            
        # Рисуем роботов
        for robot in self.robots:
            robot.draw(screen)
            
        # Счетчик
        counter_text = f"{self.robots_killed}/{self.max_robots}"
        text_surface = self.font.render(counter_text, True, WHITE)
        screen.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, 20))
        
        # Артефакт
        if self.artifact['active'] and not self.artifact['collected']:
            screen.blit(self.artifact['image'], self.artifact['rect'])
            if self.artifact['show_e']:
                font = pygame.font.Font(None, MAIN_FONT_SIZE)
                e_text = font.render("E", True, WHITE)
                screen.blit(e_text, (self.artifact['rect'].x + 20, self.artifact['rect'].y - 30))
                
class Locations7(Locations):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("images/locations/location_2.jpg").convert()

        self.dialogs = [
            "Алекс: Наконец то я собрал все артефакты и дверь открылась!",
            "Алекс: Это было захватывающее и опасное путешествие",
            "Алекс: Пожалуй, пора заканчивать исследовать эти ужасные здания",
            "Алекс: Мало ли что ждёт меня в других местах ",
            "Алекс: Ну все, пора выбираться",
        ]
        self.current_dialog = 0
        self.dialog_start_time = pygame.time.get_ticks()
        self.dialog_duration = 3000  # 3 секунды на каждый диалог
        
        self.darkness_alpha = 0
        self.darkness_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.darkening = False
        self.darkening_start_time = 0
        self.darkening_duration = 8000  # 8 секунд затемнения
        self.game_complete = False
    
    def setup_music(self):
         super().setup_music()
         
    def update(self, game_manager):
        current_time = pygame.time.get_ticks()
        
        # Если игра уже завершена, ничего не делаем
        if self.game_complete:
            return
            
        # Если идет затемнение
        if self.darkening:
            elapsed = current_time - self.darkening_start_time
            self.darkness_alpha = (elapsed / self.darkening_duration) * 255
            
            # Если затемнение завершено
            if elapsed >= self.darkening_duration:
                self.game_complete = True
                # Вместо выхода открываем меню
                self.finished = True
                if game_manager:
                    game_manager.menu.active = True
            return
            
            
        # Прокрутка диалогов
        if current_time - self.dialog_start_time >= self.dialog_duration:
            self.current_dialog += 1
            self.dialog_start_time = current_time
            
            # Если диалоги закончились, начинаем затемнение
            if self.current_dialog >= len(self.dialogs):
                self.darkening = True
                self.darkening_start_time = current_time
                
    def draw(self, screen):
        super().draw(screen)
        
        # Отрисовка текущего диалога
        if not self.darkening and self.current_dialog < len(self.dialogs):
            font = pygame.font.Font(FONT_NAME, 30)
            text = font.render(self.dialogs[self.current_dialog], True, DIALOG_COLOR)
            screen.blit(text, (65, HEIGHT - 70))
            
        # Отрисовка затемнения
        if self.darkening:
            self.darkness_surface.fill((0, 0, 0, self.darkness_alpha))
            screen.blit(self.darkness_surface, (0, 0))

        
        
        