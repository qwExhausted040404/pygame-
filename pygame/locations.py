import pygame
from utils import WIDTH, HEIGHT

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Locations:
    def __init__(self):
        self.background = None
        self.font = pygame.font.Font(None, 36)
        self.finished = False
        self.background_music = None
        self.music_volume = 0.5
        self.music_playing = False
        
    def update(self, keys):
        pass
    
    def draw(self, screen):
        screen.blit(self.background, (0, 0))
    
 
class Locations1(Locations):
    def __init__(self):
        super().__init__()
        self.current_dialog = 0
        self.background_music = "music/1-2_Locations_music.mp3"
        self.background = pygame.image.load("images/locations/house.jpg").convert()
        self.dialogs = [
            "Алекс: Еще одно заброшенное здание... Как же я люблю этот момент — первый взгляд на забытое место.",
            "Алекс: Что скрывают эти стены? Может, здесь остались вещи прошлых хозяев... Или что-то более необычное.",
            "Алекс: Этот дом явно видел лучше дни. Окна разбиты, двери сорваны... Но в этом есть своя мрачная красота.",
            "Алекс: Чем старше здание, тем больше у него историй. А это... Похоже, здесь творилось что-то недоброе.",
            "Алекс: Почему люди бросают такие места? Страх? Проклятие? Или просто время не пощадило их?",
            "Алекс: Ладно, хватит раздумий. Пора зайти внутрь и узнать правду."
        ]
        self.space_pressed = False
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)
        
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
            if len(dialog) > 70:
                split_pos = dialog.rfind(' ', 0, 70)
                text = self.font.render(self.dialogs[self.current_dialog][:split_pos], True, (220, 227, 23))
                screen.blit(text, (20, HEIGHT - 120))
                text1 = self.font.render(self.dialogs[self.current_dialog][split_pos:], True, (220, 227, 23))
                screen.blit(text1, (300, HEIGHT - 70))
            else:
                text = self.font.render(self.dialogs[self.current_dialog][:70], True, (220, 227, 23))
                screen.blit(text, (20, HEIGHT - 120))
                text1 = self.font.render(self.dialogs[self.current_dialog][70:], True, (220, 227, 23))
                screen.blit(text1, (300, HEIGHT - 70))
                
                
class Locations2(Locations):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("images/locations/location_2.jpg").convert()
        self.show_message = True
        self.message_start_time = pygame.time.get_ticks()#содержит в себе время перехода на вторую локацию
        self.message_duration = 3000 
        self.message_text = "Что... Почему дверь заперлась? Как мне выбраться? Что это там за вещичка"
        self.message1_start_time = 0
        self.interactive_obj = {
            'rect': pygame.Rect(WIDTH - 100, HEIGHT - 100, 100, 100),  # Зона взаимодействия
            'image': pygame.image.load("images/artefact_1.png").convert_alpha(),
            'show_e': False,
            'collected': False,
            'message': "Вы нашли древний артефакт!",
            'message1': "Найдите 6 артефактов, иначе будете заперты НАВСЕГДА!!!",
            'message_shown': False,
            'message_shown1': False,
            'message_duration': 3000  # 3 секунды
        }
        
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
            text = self.font.render(self.message_text, True, (220, 227, 23))
            screen.blit(text, (WIDTH - 950, HEIGHT - 40))
            
        if not self.interactive_obj['collected']:
            screen.blit(self.interactive_obj['image'], self.interactive_obj['rect'])
            if self.interactive_obj['show_e']:
                font = pygame.font.Font(None, 36)
                e_text = font.render("E", True, (255, 255, 255))
                screen.blit(e_text, (self.interactive_obj['rect'].x + 40, self.interactive_obj['rect'].y - 30))
                
        if self.interactive_obj['message_shown']:
            text = self.font.render(self.interactive_obj['message'], True, (220, 227, 23))
            screen.blit(text, (WIDTH - 700, HEIGHT//2))
        
        if self.interactive_obj['message_shown1']:
            text1 = self.font.render(self.interactive_obj['message1'], True, (220, 227, 23))
            screen.blit(text1, (WIDTH - 900, HEIGHT//2))
            

class Locations3(Locations):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("images/locations/location_3.jpg").convert()
        self.background_music = "music/3_Locations_music.mp3"
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)
        
    def update(self, keys):
        pass
    
    def draw(self, screen):
        super().draw(screen)