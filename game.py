import pygame 
from utils import *
from Alex import Alex 
from enemies import *
from locations import *
from artifact_counter import ArtifactCounter
from Game_menu import *
from savegame import SaveGame

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ловушка времени")
        icon = pygame.image.load('images/models/teleport.png').convert_alpha()
        pygame.display.set_icon(icon)
        
        self.saved_volume = BASE_VOLUME
        
        self.save_system = SaveGame()
        
        self.menu = GameMenu(self)
        self.clock = pygame.time.Clock()

        self.alex = None
        self.enemies = []

        self.artifact_counter = ArtifactCounter()
        self.is_fullscreen = False


        saved_location = self.save_system.load_progress()
        if isinstance(saved_location, Locations1):
            self.setup_location(Locations1)
        elif isinstance(saved_location, Locations2):
            self.setup_location(Locations2)
        elif isinstance(saved_location, Locations3):
            self.setup_location(Locations3)
        elif isinstance(saved_location, Locations4):
            self.setup_location(Locations4)
        elif isinstance(saved_location, Locations5):
            self.setup_location(Locations5)
        elif isinstance(saved_location, Locations6):
            self.setup_location(Locations6)
        elif isinstance(saved_location, Locations7):
            self.setup_location(Locations7)
        else:
            self.setup_location(Locations1)
            
    def setup_location(self, location_class):         

        #сохраняем прогресс
        self.current_location = location_class()
        self.save_system.save_progress(self.current_location)
        
        # Сохраняем текущую громкость перед сменой локации
        if self.current_location and hasattr(self.current_location, 'background_music'):
            self.saved_volume = pygame.mixer.music.get_volume()
        
        self.current_location.setup_music()
        
        # Восстанавливаем громкость для новой локации
        if hasattr(self.current_location, 'background_music'):
            pygame.mixer.music.set_volume(self.saved_volume)
        
    
        if isinstance(self.current_location, Locations1):
            self.alex = None
            self.enemies = []
        elif isinstance(self.current_location, Locations2):
            self.alex = Alex(20, 395)
            self.enemies = []
        elif isinstance(self.current_location, Locations3):
            self.alex = Alex(20, 380)
            self.enemies = [Tigers(900, 200), Tigers(300, 100), Tigers(450, 300),  Tigers(30, 50), Tigers(700, 250)]
        elif isinstance(self.current_location, Locations4):
            self.alex = Alex(20, 380)
            self.enemies = []
        elif isinstance(self.current_location, Locations5):
            self.alex = Alex(20, 350)
            self.enemies = [Zombie(350, 390), Zombie(750, 390)]
        elif isinstance(self.current_location, Locations6):
            self.alex = Alex(20, 350)
            self.enemies = []
        elif isinstance(self.current_location, Locations6):
            self.alex = None
            
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
        
        self.save_system.save_progress(self.current_location)#перед выходом сохраняем текущую локацию
        pygame.quit()

    def update_game(self):
        """Обновление игрового состояния"""
        keys = pygame.key.get_pressed()
        
        if self.alex and self.alex.is_dead:       # Если игрок умер
            self.alex.death_timer -= 1            # Уменьшаем таймер
            if self.alex.death_timer <= 0:        # Если таймер истёк
                # Перезагружаем текущую локацию
                if isinstance(self.current_location, Locations3):
                    self.setup_location(Locations3)
                elif isinstance(self.current_location, Locations4):
                    self.setup_location(Locations4)
                elif isinstance(self.current_location, Locations5):
                    self.setup_location(Locations5)
                elif isinstance(self.current_location, Locations6):
                    self.setup_location(Locations6)
            return  # Пропускаем остальную логику обновления
        
        # Обновление текущей локации
        if isinstance(self.current_location, Locations1):
            self.current_location.update(keys)
            
        elif isinstance(self.current_location, Locations2):
            self.current_location.update(keys, self.alex, self)
            if hasattr(self.current_location, 'platforms'):
                self.alex.platforms = self.current_location.platforms
                
        elif isinstance(self.current_location, Locations3):
            self.current_location.update(keys, self.alex, self)
            self.alex.platforms = self.current_location.platforms
            for enemy in self.enemies[:]: 
                enemy.platforms = self.current_location.platforms
                enemy.update(self.alex)
                for stone in self.alex.stones[:]:
                    if stone.rect.colliderect(enemy.rect):
                        if enemy.take_damage():  # Если здоровье закончилось
                            self.enemies.remove(enemy)
                        self.alex.stones.remove(stone)
                        break
            if len(self.enemies) == 0:
                self.current_location.interactive_obj['enemies_killed'] = True
                
        elif isinstance(self.current_location, Locations4):
            self.current_location.update(keys, self.alex, self)
            if hasattr(self.current_location, 'platforms'):
                self.alex.platforms = self.current_location.platforms
                
        elif isinstance(self.current_location, Locations5):
            self.current_location.update(keys, self.alex, self)
            if hasattr(self.current_location, 'platforms'):
                self.alex.platforms = self.current_location.platforms
                for enemy in self.enemies:
                    enemy.platforms = self.current_location.platforms
                    enemy.update(self.alex)
                    
        elif isinstance(self.current_location, Locations6):
            self.current_location.update(keys, self.alex, self)
            if hasattr(self.current_location, 'platforms'):
                self.alex.platforms = self.current_location.platforms
            self.enemies = self.current_location.robots
            
        elif isinstance(self.current_location, Locations7):
            self.current_location.update(self)
        
        #метание камней на 3-ей локации
        if pygame.mouse.get_pressed()[0] and self.alex and isinstance(self.current_location, Locations3):  # левая кнопка мыши
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.alex.throw_stone(mouse_x, mouse_y, self)
        
        if self.alex:
            self.alex.update(keys, self)

        #стрельба на 6-ой локации
        if pygame.mouse.get_pressed()[0] and self.alex and isinstance(self.current_location, Locations6):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.alex.shoot(mouse_x, mouse_y, self)
        
        # Проверка завершения локации
        if self.current_location.finished:
            if isinstance(self.current_location, Locations1):
                self.setup_location(Locations2)
            elif isinstance(self.current_location, Locations2):
                self.setup_location(Locations3)
            elif isinstance(self.current_location, Locations3):
                self.setup_location(Locations4)
            elif isinstance(self.current_location, Locations4):
                self.setup_location(Locations5)
            elif isinstance(self.current_location, Locations5):
                self.setup_location(Locations6)
            elif isinstance(self.current_location, Locations6):
                self.setup_location(Locations7)
            elif isinstance(self.current_location, Locations7):
                self.menu.active = True
                
    def draw_game(self):
        """Отрисовка всех игровых объектов"""
        self.current_location.draw(self.screen)
        
        if self.alex and not self.alex.is_dead:
            self.alex.draw(self.screen, pygame.key.get_pressed())
            self.alex.draw_health(self.screen)
            pygame.draw.rect(self.screen, RED, self.alex.rect, 1)
            
        if self.enemies != []:
            for enemy in self.enemies:  # Рисуем всех врагов
                enemy.draw(self.screen)
        
        if self.alex and self.alex.is_dead:
            # Создаём полупрозрачную чёрную поверхность
            darkness = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            # Плавное увеличение затемнения (от 0 до 200)
            alpha = min(255, 255 * (1 - self.alex.death_timer / self.alex.death_duration))
            darkness.fill((0, 0, 0, alpha))  # Чёрный с изменяемой прозрачностью
            self.screen.blit(darkness, (0, 0))
            
            # Текст "ПОРАЖЕНИЕ"
            font = pygame.font.Font(FONT_NAME, 72)
            text = font.render("Вы погибли!", True, RED)
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            self.screen.blit(text, text_rect)
        
        self.artifact_counter.draw(self.screen)
        self.menu.draw(self.screen)
    
    def reset_game(self):
        """Сбрасывает игру в начальное состояние"""
        #сбрасываем прогресс
        self.save_system.reset_progress()
        self.setup_location(Locations1)
        
        # Сброс всех параметров игры
        self.saved_volume = BASE_VOLUME
        pygame.mixer.music.set_volume(self.saved_volume)
        
        # Сброс счетчика артефактов
        self.artifact_counter = ArtifactCounter()
        
        # Переход к первой локации
        self.setup_location(Locations1)
        
        # Сброс состояния меню
        self.menu.active = False
        
    