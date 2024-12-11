import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Перепрыгни препятствия с хвостом")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Параметры героя
hero_width, hero_height = 40, 60
hero_x = 100
hero_y = HEIGHT - hero_height - 20
hero_speed_y = 0
gravity = 1
jump_strength = -30
is_jumping = False


# Параметры препятствий
obstacle_width, obstacle_height = 40, 80
obstacle_x = WIDTH
obstacle_y = HEIGHT - obstacle_height - 20
obstacle_speed = 5

# Параметры юнитов
units = []  # Список активных юнитов
max_units = 3  # Максимальное количество юнитов на экране
unit_size = 40
unit_spawn_timer = 0  # Таймер появления юнитов
unit_spawn_interval = 100  # Интервал появления юнитов (в кадрах)

# Очки
score = 0

# Хвост героя
interactions_count = 0

tail = []  # Список полосок хвоста
tail_width = hero_width // 2  # Половина ширины героя
tail_color = BLUE

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление прыжком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping:
        hero_speed_y = jump_strength
        is_jumping = True

    # Применение гравитации
    hero_speed_y += gravity
    hero_y += hero_speed_y

    # Ограничение: герой не может упасть ниже пола
    if hero_y > HEIGHT - hero_height - 20:
        hero_y = HEIGHT - hero_height - 20
        hero_speed_y = 0
        is_jumping = False

    # Движение препятствия
    obstacle_x -= obstacle_speed

    # Если препятствие ушло за экран, сбрасываем его положение
    if obstacle_x < -obstacle_width:
        obstacle_x = WIDTH
        score += 1  # Увеличиваем очки

    # Обработка юнитов
    unit_spawn_timer += 1
    if unit_spawn_timer > unit_spawn_interval and len(units) < max_units:
        unit_x = random.randint(WIDTH, WIDTH + 300)
        unit_y = HEIGHT - unit_size - 20
        unit_type = random.choice(["A", "B"])
        units.append({"x": unit_x, "y": unit_y, "type": unit_type})
        unit_spawn_timer = 0

    # Движение юнитов и их сбор
    hero_rect = pygame.Rect(hero_x, hero_y, hero_width, hero_height)
    new_units = []
    for unit in units:
        unit["x"] -= obstacle_speed  # Двигаем юниты влево
        unit_rect = pygame.Rect(unit["x"], unit["y"], unit_size, unit_size)
        if hero_rect.colliderect(unit_rect):
            interactions_count += 1  # Увеличиваем счётчик взаимодействий
            if interactions_count in [1, 3, 5] and len(tail) < 3:  # Проверка на добавление полоски
                tail.append({"x": hero_x - len(tail) * tail_width, "y": hero_y})

            # Обработка типов юнитов
            if unit["type"] == "A":
                jump_strength += 1  # Уменьшаем силу прыжка
            elif unit["type"] == "B":
                score += 2  # Увеличиваем очки

        else:
            if unit["x"] > -unit_size:  # Оставляем юнит, если он не ушёл за экран
                new_units.append(unit)
    units = new_units

    # Движение хвоста
    for i, segment in enumerate(tail):
        segment["x"] = hero_x - (i + 1) * tail_width
        segment["y"] = hero_y

    # Проверка столкновения с препятствием
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
    if hero_rect.colliderect(obstacle_rect):
        print(f"Game Over! Your Score: {score}")
        running = False

    # Рисование
    screen.fill(WHITE)

    # Рисуем хвост
    for segment in tail:
        pygame.draw.rect(screen, tail_color, (segment["x"], segment["y"], tail_width, hero_height))

    pygame.draw.rect(screen, BLUE, (hero_x, hero_y, hero_width, hero_height))  # Герой
    pygame.draw.rect(screen, BLACK, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))  # Препятствие

    # Рисование юнитов
    for unit in units:
        color = RED if unit["type"] == "A" else GREEN
        pygame.draw.rect(screen, color, (unit["x"], unit["y"], unit_size, unit_size))

    # Отображение очков
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))
    # Отображение счётчика взаимодействий
    interaction_text = font.render(f"Interactions: {interactions_count}", True, BLACK)
    screen.blit(interaction_text, (10, 50))  # Отображение чуть ниже очков

    # Обновление экрана
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
