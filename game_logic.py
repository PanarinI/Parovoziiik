import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Паровозик Пиара")

# Часы для контроля частоты кадров
clock = pygame.time.Clock()

# Переменные игры
train_img = pygame.Surface((100, 50))  # Временное изображение поезда
train_img.fill(BLACK)
train_x = 100
train_y = SCREEN_HEIGHT - 150
ground_y = SCREEN_HEIGHT - 150
is_jumping = False
velocity_y = 0
jump_height = -15  # Высота прыжка
gravity = 0.6  # Гравитация

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

    # Отрисовка всего
    screen.fill(WHITE)  # Очищаем экран
    screen.blit(train_img, (train_x, train_y))  # Рисуем поезд

    pygame.display.update()  # Обновляем экран
    clock.tick(30)  # Контролируем частоту кадров

pygame.quit()  # Завершаем Pygame
sys.exit()  # Выход из программы
