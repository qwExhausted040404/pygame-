import pygame

#разрешение
WIDTH, HEIGHT = 1000, 500

# Настройки текста
FONT_NAME = 'font/font_1.ttf'
MAIN_FONT_SIZE = 36
LARGE_FONT_SIZE = 48

#цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (100, 100, 100)
DIALOG_COLOR = (220, 227, 23)
COLOR_BUTTONS = (45, 144, 237)

# Направления
LEFT = -1
RIGHT = 1

# параметры игровых объектов
DIG_TIME = 500

#параметры стрелы
SPEED_ARROW = 7

#параметры зомби
SPEED_ZOMBIE = 3.2
DAMAGE_COOLDOWN_ZOMBIE = 60

#параметры робота
SPEED_ROBOT = 1.5
ROBOT_HEALTH = 12
SPEED_ROBOT_BULLET = 3.5
ROBOT_SHOOT_DELAY = 200
ROBOT_SPAWN_TIMER = 120

#движущаяся платформа
SPEED_PLATFORM = 2

#параметры тигра
TIGER_GRAVITY = 0.8
TIGER_DETECTION_RADIUS = 450
TIGER_COOLDOWN = 180
TIGER_MAX_HEALTH = 4
TIGER_SPEED_JUMP = 26
SPEED_TIGER = 2.7

#параметры призрака
GHOST_APPEARANCE_LEFT_X = -60
MIN_GHOST_SPEED = 3.0
MAX_GHOST_SPEED = 7.0

#скорость анимации
ANIMATIONS_SPEED = 0.15

#громкость
BASE_VOLUME = 0.5

#хитбокс алекса
HITBOX_WIDTH_ALEX = 30
HITBOX_HEIGHT_ALEX = 45
HITBOX_X_ALEX = 8
HITBOX_Y_ALEX = 5

#скорость Алекса
SPEED_ALEX = 5.5

#жизни алекса
MAX_HEALTH_ALEX = 3

#параметры оружия алекса
THROW_COOLDOWN = 30
SHOOT_COOLDOWN = 14
SPEED_STONE = 18
LIFETIME_STONE = 120
SPEED_BULLET = 15
STONE_GRAVITY = 0.2

#хитбокс тигра
HITBOX_WIDTH_TIGER = 40
HITBOX_HEIGHT_TIGER = 20
HITBOX_X_TIGER = 3
HITBOX_Y_TIGER = 5

#параметры прыжка алекса
ALEX_GRAVITY = 1.2
ALEX_INITIAL_SPEED = 18

#длительность смерти
ALEX_DEATH_DURATION = 420

#кол-во артефактов, которые надо собрать
TOTAL_ARTIFACT = 5

#затемнение
ALPHA = 255

#нужное время выживания на 5-ой локации
LEVEL_TIMER = 180 * 60