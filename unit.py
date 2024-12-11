import pygame
import random

COLOR_MAP = {"A": (255, 0, 0), "B": (0, 255, 0)}

class Unit:
    def __init__(self, x, y, size, unit_type):
        self.rect = pygame.Rect(x, y, size, size)
        self.type = unit_type
        self.color = (255, 0, 0) if unit_type == "A" else (0, 255, 0)
        # Установка изображения
        self.image = pygame.Surface((size, size))
        self.image.fill(self.color)  # Красный для A, зелёный для B

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_image(self):
        return self.image

    def is_off_screen(self, screen_width):
        return self.rect.right < 0

    @staticmethod
    def spawn(units, max_units, spawn_x_range, ground_y, unit_size):
        if len(units) < max_units:
            unit_x = random.randint(*spawn_x_range)  # Диапазон появления юнитов
            unit_y = ground_y - unit_size  # Позиция юнита на земле
            unit_type = random.choice(["A", "B"])  # Тип юнита
            units.append(Unit(unit_x, unit_y, unit_size, unit_type))  # Добавление юнита

