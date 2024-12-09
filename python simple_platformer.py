import pygame

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Простой Платформер")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Параметры игрока
player_width, player_height = 40, 60
player_x = WIDTH // 2
player_y = HEIGHT - 200
player_speed = 5
player_jump_speed = -15
player_color = BLUE

# Гравитация
gravity = 1
player_velocity_y = 0
is_jumping = False

# Платформа
platform_x = 300
platform_y = HEIGHT - 100
platform_width = 200
platform_height = 20

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_SPACE] and not is_jumping:
        player_velocity_y = player_jump_speed
        is_jumping = True

    # Применяем гравитацию
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Проверка столкновения с платформой
    if (
        player_y + player_height >= platform_y
        and platform_x <= player_x <= platform_x + platform_width
    ):
        player_y = platform_y - player_height
        player_velocity_y = 0
        is_jumping = False

    # Ограничение экрана
    if player_x < 0:
        player_x = 0
    if player_x > WIDTH - player_width:
        player_x = WIDTH - player_width

    # Если игрок упал за пределы экрана
    if player_y > HEIGHT:
        print("Game Over!")
        running = False

    # Рисование
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (platform_x, platform_y, platform_width, platform_height))  # Платформа
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_width, player_height))  # Игрок

    # Обновление экрана
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
