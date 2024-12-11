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
    global hero, tail, units, gaps, gap_timer, gap_interval, score, interaction_count, unit_timer, unit_interval, current_phase, distance, obstacle_speed, gap_width
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
    current_phase = 1  # Текущая фаза игры
    distance = 0  # Пройденная дистанция
    obstacle_speed = 5  # Базовая скорость движения
    gap_width = 100  # Ширина пропасти

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

    # Логика фаз игры
    if current_phase == 1:  # Фаза 1: Сбор пассажиров
        if len(tail.wagons) == 3 and all(len(wagon) == 2 for wagon in tail.wagons):
            current_phase = 2  # Переход к фазе 2





    elif current_phase == 2:  # Фаза 2: Замена профессионалов

        all_replaced = True  # Флаг для проверки, заменены ли все профессионалы

        for wagon in tail.wagons:

            for unit in wagon:

                if unit['type'] == 'A':  # Если есть профессионал

                    # Удаляем профессионала

                    wagon.remove(unit)

                    # Добавляем тупореза вместо него

                    new_unit = {"type": "B", "image": pygame.Surface((40, 40)), "rect": None}

                    new_unit['image'].fill((0, 255, 0))  # Задаём цвет тупореза

                    tail.add_unit_to_wagon(new_unit)

                    all_replaced = False  # Указываем, что профессионалы ещё есть

                    break  # Останавливаем цикл для текущего вагона

        # Если все профессионалы заменены, и все вагоны заполнены

        if all_replaced and all(len(wagon) == 2 for wagon in tail.wagons):

            current_phase = 3  # Переход к фазе 3



        else:
            for wagon in tail.wagons:
                for unit in wagon:
                    if unit['type'] == 'A':  # Найден профессионал
                        wagon.remove(unit)  # Удаляем профессионала
                        tail.add_unit_to_wagon({"type": "B", "image": unit['image'], "rect": None})
                        break

    elif current_phase == 3:  # Фаза 3: Ускорение
        obstacle_speed += 0.01  # Постепенно увеличиваем скорость
        if random.random() < 0.1:  # Иногда увеличиваем ширину пропасти
            gap_width += random.randint(5, 10)

    # Обновление объектов
    hero.update()
    tail.update(hero.rect)

    # Обновление пропастей
    gap_timer += 1
    if gap_timer > gap_interval:
        gap_timer = 0
        gap_interval = random.randint(80, 130)
        gap_x = WIDTH
        gaps.append({"x": gap_x, "width": gap_width})

    for gap in gaps[:]:
        gap["x"] -= obstacle_speed
        if gap["x"] + gap["width"] < 0:
            gaps.remove(gap)
        if gap["x"] < hero.rect.x < gap["x"] + gap["width"] and hero.rect.bottom >= HEIGHT - GROUND_HEIGHT:
            print(f"Game Over! Your Score: {score}, Distance: {distance} meters")
            reset_game()

    # Спавн юнитов
    unit_timer += 1
    if unit_timer > unit_interval:
        Unit.spawn(units, max_units=20, spawn_x_range=(800, 1100), ground_y=600, unit_size=40)
        unit_timer = 0
        unit_interval = random.randint(80, 120)

    # Обработка взаимодействий с юнитами
    for unit in units[:]:
        unit.update(obstacle_speed)
        unit.draw(screen)
        if hero.rect.colliderect(unit.rect):
            interaction_count += 1

            # Если юнит молчаливый, определить его тип (рандомно)
            if unit.type == "A":
                hero.jump_strength += 3
                print("Вы добавили профессионала!")
            elif unit.type == "silent":
                unit.type = random.choice(["A", "B"])
                if unit.type == "A":
                    unit.image.fill((255, 0, 0))  # Профессионал
                    print("Вы добавили профессионала!")
                    hero.jump_strength += 3
                elif unit.type == "B":
                    unit.image.fill((0, 255, 0))  # Тупорез
                    print("Вы добавили тупореза!")
                    score += 2

            # Логика добавления в вагон
            if interaction_count in [1, 3, 5]:
                tail.add_wagon()

            unit_image = unit.get_image()
            tail.add_unit_to_wagon({
                'type': unit.type,
                'image': unit_image,
                'rect': None
            })

            score += 1
            units.remove(unit)

    # Рисование
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 200, 0), (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
    for gap in gaps:
        pygame.draw.rect(screen, (255, 255, 255), (gap["x"], HEIGHT - GROUND_HEIGHT, gap["width"], GROUND_HEIGHT))
    hero.draw(screen)
    tail.draw(screen, hero.rect)
    for unit in units:
        unit.draw(screen)

    # Отображение очков и дистанции
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    distance_text = font.render(f"Distance: {distance} m", True, (0, 0, 0))
    phase_text = font.render(f"Фаза: {current_phase}", True, (0, 0, 0))  # Фаза игры
    screen.blit(score_text, (10, 10))
    screen.blit(distance_text, (10, 50))
    jump_strength_text = font.render(f"Jump Strength: {hero.jump_strength}", True, (0, 0, 0))
    screen.blit(jump_strength_text, (10, 130))
    screen.blit(phase_text, (10, 90))

    pygame.display.flip()
    distance += 1
    clock.tick(30)

pygame.quit()
