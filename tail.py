import pygame

class Tail:
    def __init__(self, hero_width, hero_height):
        self.wagons = []  # Список вагонов
        self.wagon_width = hero_width // 2
        self.hero_height = hero_height
        self.spacing = 10  # Расстояние между вагонами

    def add_wagon(self, unit_image):
        """Добавляет новый вагон с изображением юнита"""
        wagon = {"image": unit_image, "x": 0, "y": 0}
        self.wagons.append(wagon)

    def update(self, hero_rect):
        """Обновляет позиции вагонов"""
        for i, wagon in enumerate(self.wagons):
            wagon["x"] = hero_rect.x - (i + 1) * (self.wagon_width + self.spacing)
            wagon["y"] = hero_rect.y

    def draw(self, screen):
        """Рисует все вагоны"""
        for wagon in self.wagons:
            screen.blit(wagon["image"], (wagon["x"], wagon["y"]))
