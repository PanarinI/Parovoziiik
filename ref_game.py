import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Перепрыгни препятствия")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Параметры героя
hero_width, hero_height = 40, 60
hero_x = 100
hero_y = HEIGHT - hero_height - 20
hero_speed_y = 0  # Вертикальная скорость
gravity = 1  # Гравитация
jump_strength = -15  # Сила прыжка
is_jumping = False  # Флаг, чтобы не прыгать бесконечно

# Параметры препятствий
obstacle_width, obstacle_height = 40, 40
obstacle_x = WIDTH
obstacle_y = HEIGHT - obstacle_height - 20
obstacle_speed = 5

# Очки
score = 0

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

    # Проверка столкновения
    hero_rect = pygame.Rect(hero_x, hero_y, hero_width, hero_height)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
    if hero_rect.colliderect(obstacle_rect):
        print(f"Game Over! Your Score: {score}")
        running = False

    # Рисование
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (hero_x, hero_y, hero_width, hero_height))  # Герой
    pygame.draw.rect(screen, RED, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))  # Препятствие

    # Отображение очков
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
