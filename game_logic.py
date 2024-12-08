import pygame
import sys
import math  # Добавляем импорт модуля math для работы с тригонометрическими функциями

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)  # Цвет рельсов
DARK_BROWN = (101, 67, 33)  # Темно-коричневый цвет шпал
DARK_GRAY = (64, 64, 64)  # Темно-серый цвет рельсов
CARAMEL = (153, 101, 21)  # Темно-карамельный (RGB)

# Инициализация Pygame
pygame.init()

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Паровозик Пиара")

# Часы для контроля частоты кадров
clock = pygame.time.Clock()

# Переменные игры
train_width = 100  # Ширина поезда
train_height = 50  # Высота поезда (добавляем эту переменную)
train_img = pygame.Surface((train_width, train_height))  # Временное изображение поезда
train_img.fill(BLACK)
train_x = 100
train_y = SCREEN_HEIGHT - 150
ground_y = SCREEN_HEIGHT - 150
is_jumping = False
velocity_y = 0
jump_height = -15  # Высота прыжка
gravity = 0.6  # Гравитация

# Рельсы
rail_length = SCREEN_WIDTH  # Длина рельса
rail_speed = 5  # Скорость движения рельсов
rail_height = 5  # Толщина основного рельса
rail_base_y = train_y + train_height  # Высота рельса (он будет на уровне поезда)
rails = [pygame.Rect(0, train_y + train_height, SCREEN_WIDTH, rail_height)]  # Рельсы непосредственно под поездом
rail_length = SCREEN_WIDTH  # Длина рельс
rail_speed = 5  # Скорость движения рельсов

# Размер шпал (длина каждой шпалки)
spike_angle = 120  # Угол наклона шпалы
spike_length = 10  # Длина каждой шпалы

# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Корректно закрываем Pygame
            sys.exit()  # Полностью выходим из программы

    # Управление прыжком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping:  # Прыжок, если не в воздухе
        is_jumping = True
        velocity_y = jump_height  # Начало прыжка

    # Применение гравитации
    if is_jumping:
        train_y += velocity_y  # Двигаем поезд по вертикали
        velocity_y += gravity  # Плавное ускорение падения
        if train_y >= ground_y:
            train_y = ground_y  # Останавливаем поезд на земле
            is_jumping = False  # Поезд больше не в прыжке
            velocity_y = 0  # Останавливаем вертикальную скорость

    # Двигаем рельсы
    for rail in rails:
        rail.x -= rail_speed  # Рельсы двигаются влево
        if rail.x + rail.width < 0:  # Если рельсы вышли за экран
            rail.x = SCREEN_WIDTH  # Ставим рельсы обратно справа

    # Отрисовка всего
    screen.fill(WHITE)  # Очищаем экран

    # Рисуем основной горизонтальный рельс (не двигается с поездом)
    pygame.draw.rect(screen, DARK_GRAY, pygame.Rect(0, rail_base_y, rail_length, rail_height))

    # Смещение шпал по оси X (для того, чтобы они не выпирали над рельсом)
    spike_offset_x = 10  # Смещение шпал по оси x, регулируй по желанию

    # Рисуем поперечные бруски (шпалы)
    rail_spike_y = rail_base_y + 3  # Шпалы расположены чуть ниже рельса

    for i in range(0, rail_length, 60):  # Расставляем шпалы через 60 пикселей
        # Начальная точка шпалы
        start_x = i - rail_speed + spike_offset_x
        start_y = rail_spike_y  # Высота начала шпалы (по оси Y)

        # Конечная точка шпалы
        end_x = start_x + spike_length * math.cos(math.radians(spike_angle))  # Длина по оси X
        end_y = start_y + spike_length * math.sin(math.radians(spike_angle))  # Длина по оси Y

        # Рисуем шпалу с заданной длиной (spike_length) и углом наклона (spike_angle)
        pygame.draw.line(screen, DARK_BROWN, (start_x, start_y), (end_x, end_y), 3)  # Косая черточка (шпалка)

    # Рисуем поезд
    screen.blit(train_img, (train_x, train_y))  # Рисуем поезд

    # Обновляем экран
    pygame.display.update()
    clock.tick(30)  # Контролируем частоту кадров

pygame.quit()  # Завершаем Pygame
sys.exit()  # Выход из программы
