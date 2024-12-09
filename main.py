import pygame
from hero import Hero
from tail import Tail
from unit import Unit
from obstacle import Obstacle

# Настройки игры
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Поезд с хвостом")
clock = pygame.time.Clock()

# Инициализация Pygame
pygame.init()

# Шрифты
font = pygame.font.Font(None, 36)  # Загрузка шрифта

# Загрузка изображений
unit_a_image = pygame.Surface((40, 40))  # Замените на pygame.image.load("unit_a.png")
unit_a_image.fill((255, 0, 0))
unit_b_image = pygame.Surface((40, 40))  # Замените на pygame.image.load("unit_b.png")
unit_b_image.fill((0, 255, 0))

# Создание объектов
hero = Hero(100, HEIGHT - 80, 40, 60, jump_strength=-30, gravity=1)
tail = Tail(hero_width=40, hero_height=60)
obstacle = Obstacle(WIDTH, HEIGHT - 100, 40, 80, speed=5)
units = []
unit_timer = 0
unit_interval = 100
score = 0
interaction_count = 0

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        hero.jump()

    # Обновление объектов
    hero.update()
    tail.update(hero.rect)
    obstacle.update()

    # Спавн юнитов
    unit_timer += 1
    unit_timer = Unit.spawn(units, max_units=3, interval=unit_interval, timer=unit_timer)

    # Обработка взаимодействий
    for unit in units[:]:
        unit.update(5)
        if hero.rect.colliderect(unit.rect):
            interaction_count += 1
            if interaction_count % 2 == 0:
                tail.add_wagon(unit_a_image if unit.type == "A" else unit_b_image)
            score += 1
            units.remove(unit)

    # Рисование
    screen.fill((255, 255, 255))
    hero.draw(screen)
    tail.draw(screen)
    obstacle.draw(screen)
    for unit in units:
        unit.draw(screen)

    # Отображение очков
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    interaction_text = font.render(f"Interactions: {interaction_count}", True, (0, 0, 0))
    screen.blit(interaction_text, (10, 50))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
