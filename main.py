import pygame
import random
from hero import Hero
from tail import Tail
from unit import Unit

# Настройки игры
WIDTH, HEIGHT = 800, 600
GROUND_HEIGHT = 20  # Высота земли
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Поезд с хвостом")
clock = pygame.time.Clock()

# Инициализация Pygame
pygame.init()

# Шрифты
font = pygame.font.Font(None, 36)

# Функция для сброса игры
def reset_game():
    global hero, tail, units, gaps, gap_timer, gap_interval, score, interaction_count, unit_timer, unit_interval
    hero = Hero(100, HEIGHT - 80 - GROUND_HEIGHT, 40, 60, jump_strength=-24, gravity=1, ground_height=HEIGHT - GROUND_HEIGHT)
    tail = Tail(hero_width=40, hero_height=60, max_wagons=3, spacing=10)
    units = []
    gaps = []
    gap_timer = 0
    gap_interval = random.randint(10, 150)
    score = 0
    interaction_count = 0
    unit_timer = 0
    unit_interval = random.randint(80, 120)

# Начальная инициализация объектов игры
reset_game()

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

    # Обновление пропастей
    gap_timer += 1
    if gap_timer > gap_interval:
        gap_timer = 0  # Сброс таймера
        gap_interval = random.randint(80, 130)  # Новый случайный интервал для появления пропастей

        # Создание новой пропасти
        gap_x = WIDTH  # Пропасть появляется справа, за пределами экрана
        gap_width = random.randint(50, 140)  # Случайная ширина пропасти
        gaps.append({"x": gap_x, "width": gap_width})

    # Обновление всех пропастей
    for gap in gaps[:]:
        gap["x"] -= 5  # Движение пропастей влево
        if gap["x"] + gap["width"] < 0:  # Удаление пропасти, если она ушла за экран
            gaps.remove(gap)

        # Проверка падения героя в пропасть
        if gap["x"] < hero.rect.x < gap["x"] + gap["width"] and hero.rect.bottom >= HEIGHT - GROUND_HEIGHT:
            print(f"Game Over! Your Score: {score}")
            reset_game()

    # Спавн юнитов
    unit_timer += 1
    if unit_timer > unit_interval:
        Unit.spawn(units, max_units=20, spawn_x_range=(800, 1100), ground_y=600, unit_size=40)
        unit_timer = 0
        unit_interval = random.randint(80, 120)  # Новый случайный интервал для следующего юнита

    # Обработка взаимодействий с юнитами
    for unit in units[:]:
        unit.update(5)
        unit.draw(screen)  # Отображение юнита и его текста
        if hero.rect.colliderect(unit.rect):
            interaction_count += 1

            # Проверка типа юнита
            if unit.type == "A":  # Красный юнит
                hero.jump_strength += 3  # Уменьшение высоты прыжка
            elif unit.type == "B":  # Зелёный юнит
                score += 2  # Дополнительные очки

            # Добавление вагона при нечётных взаимодействиях
            if interaction_count in [1, 3, 5]:
                tail.add_wagon()
            # Добавление юнита в вагон
            unit_image = unit.get_image()  # Получаем объект pygame.Surface
            tail.add_unit_to_wagon(unit_image)

            score += 1  # Увеличиваем общий счёт
            units.remove(unit)

    # Рисование
    screen.fill((255, 255, 255))

    # Отрисовка земли
    pygame.draw.rect(screen, (0, 200, 0), (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

    # Отрисовка пропастей
    for gap in gaps:
        pygame.draw.rect(screen, (255, 255, 255), (gap["x"], HEIGHT - GROUND_HEIGHT, gap["width"], GROUND_HEIGHT))

    # Отрисовка героя и хвоста
    hero.draw(screen)
    tail.draw(screen, hero.rect)

    # Отрисовка юнитов
    for unit in units:
        unit.draw(screen)

    # Отображение очков
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    interaction_text = font.render(f"Interactions: {interaction_count}", True, (0, 0, 0))
    screen.blit(interaction_text, (10, 50))

    pygame.display.flip()
    clock.tick(30)
print(self.wagons)

pygame.quit()
