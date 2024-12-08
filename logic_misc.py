import pygame
import sys
import time

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
BLUE = (0, 0, 255)  # Цвет реки

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


class Rail:
    def __init__(self, rail_length, rail_height, rail_speed, spike_angle, spike_length):
        self.rail_length = rail_length
        self.rail_height = rail_height
        self.rail_speed = rail_speed
        self.spike_angle = spike_angle
        self.spike_length = spike_length
        self.rail_offset_x_1 = 0  # Начальное смещение первого рельса
        self.rail_offset_x_2 = self.rail_length  # Начальное смещение второго рельса (за экраном)
        self.rail_base_y = SCREEN_HEIGHT - 100  # Высота рельса
        self.spike_offset_x_1 = 0  # Начальная позиция шпал
        self.spike_offset_x_2 = self.rail_length  # Начальная позиция для второй группы шпал

    def update(self):
        # Обновление позиции рельсов
        self.rail_offset_x_1 -= self.rail_speed
        self.rail_offset_x_2 -= self.rail_speed

        # Зацикливаем рельсы, когда они выходят за экран
        if self.rail_offset_x_1 + self.rail_length <= 0:
            self.rail_offset_x_1 = self.rail_length  # Перемещаем рельс обратно на правую сторону
        if self.rail_offset_x_2 + self.rail_length <= 0:
            self.rail_offset_x_2 = self.rail_length  # Перемещаем второй рельс обратно

        # Обновление позиции шпал
        self.spike_offset_x_1 -= self.rail_speed
        self.spike_offset_x_2 -= self.rail_speed

        # Зацикливаем шпалы
        if self.spike_offset_x_1 + self.rail_length <= 0:
            self.spike_offset_x_1 = self.rail_length
        if self.spike_offset_x_2 + self.rail_length <= 0:
            self.spike_offset_x_2 = self.rail_length

    def draw(self, screen):
        # Рисуем основной горизонтальный рельс
        pygame.draw.rect(screen, DARK_GRAY,
                         pygame.Rect(self.rail_offset_x_1, self.rail_base_y, self.rail_length, self.rail_height))
        pygame.draw.rect(screen, DARK_GRAY,
                         pygame.Rect(self.rail_offset_x_2, self.rail_base_y, self.rail_length, self.rail_height))

        # Рисуем шпалы
        rail_spike_y = self.rail_base_y + 3  # Шпалы расположены чуть ниже рельса
        for i in range(0, self.rail_length, 60):  # Расставляем шпалы через 60 пикселей
            start_x_1 = i + self.spike_offset_x_1
            end_x_1 = start_x_1 + self.spike_length
            end_y_1 = rail_spike_y + self.spike_angle  # Координата Y для конца шпалы
            pygame.draw.line(screen, DARK_BROWN, (start_x_1, rail_spike_y), (end_x_1, end_y_1),
                             3)  # Рисуем первую группу шпал

            start_x_2 = i + self.spike_offset_x_2
            end_x_2 = start_x_2 + self.spike_length
            end_y_2 = rail_spike_y + self.spike_angle  # Координата Y для конца шпалы
            pygame.draw.line(screen, DARK_BROWN, (start_x_2, rail_spike_y), (end_x_2, end_y_2),
                             3)  # Рисуем вторую группу шпал


# Создание объекта Rail
rail = Rail(800, 5, 5, 120, 10)



# Параметры рек
river_width = 200  # Ширина реки, примерно в два паровозика
river_height = 50  # Высота реки
river_x = 500  # Начальная позиция реки
river_y = SCREEN_HEIGHT - 150  # Река будет на уровне земли
river_visible_1 = False  # Первая река
river_visible_2 = False  # Вторая река

# Главный игровой цикл
start_time = time.time()  # Засекаем время начала игры
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

    # Обновление состояния рельсов и шпал
    rail.update()

    # Проверяем время, чтобы добавить реку
    elapsed_time = time.time() - start_time
    if elapsed_time > 2 and not river_visible_1:
        river_visible_1 = True  # Появление первой реки через 2 секунды
    if elapsed_time > 4 and not river_visible_2:
        river_visible_2 = True  # Появление второй реки через 4 секунды

    # Отрисовка всего
    screen.fill(WHITE)  # Очищаем экран

    # Рисуем рельсы и шпалы
    rail.draw(screen)

    # Рисуем реку
    if river_visible_1:
        pygame.draw.rect(screen, BLUE, pygame.Rect(river_x, river_y, river_width, river_height))  # Первая река
    if river_visible_2:
        pygame.draw.rect(screen, BLUE, pygame.Rect(river_x + 400, river_y, river_width, river_height))  # Вторая река

    # Рисуем поезд
    screen.blit(train_img, (train_x, train_y))  # Рисуем поезд

    # Обновляем экран
    pygame.display.update()
    clock.tick(30)  # Контролируем частоту кадров

pygame.quit()  # Завершаем Pygame
sys.exit()  # Выход из программы
