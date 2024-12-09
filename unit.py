import pygame
import random

class Unit:
    def __init__(self, x, y, size, unit_type):
        self.rect = pygame.Rect(x, y, size, size)
        self.type = unit_type
        self.color = (255, 0, 0) if unit_type == "A" else (0, 255, 0)

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    @staticmethod
    def spawn(units, max_units, interval, timer):
        if timer > interval and len(units) < max_units:
            unit_x = random.randint(800, 1100)
            unit_y = 600 - 40 - 20
            unit_type = random.choice(["A", "B"])
            units.append(Unit(unit_x, unit_y, 40, unit_type))
            timer = 0
        return timer
