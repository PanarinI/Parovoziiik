import pygame

class Tail:
    def __init__(self, hero_width, hero_height, max_wagons, spacing):
        self.wagons = []  # Список вагонов, каждый вагон содержит юнитов
        self.hero_width = hero_width
        self.hero_height = hero_height
        self.max_wagons = max_wagons
        self.spacing = spacing

    def add_wagon(self):
        if len(self.wagons) < self.max_wagons:
            self.wagons.append([])  # Добавляем новый пустой вагон

    def add_unit_to_wagon(self, unit):
        for wagon in self.wagons:
            if len(wagon) < 2:  # Если в вагоне меньше 2 юнитов
                wagon.append(unit)
                return

        # Если все вагоны заполнены, ничего не делаем

    def update(self, hero_rect):
        for i, wagon in enumerate(self.wagons):
            wagon_x = hero_rect.right + (i + 1) * (self.hero_width + self.spacing)
            wagon_y = hero_rect.bottom - self.hero_height
            for j, unit in enumerate(wagon):
                unit['rect'] = pygame.Rect(
                    wagon_x + j * (self.hero_width // 2),
                    wagon_y,
                    self.hero_width // 2,
                    self.hero_height // 2
                )

    def draw(self, screen, hero_rect):
        for i, wagon in enumerate(self.wagons):
            wagon_x = hero_rect.right + (i + 1) * (self.hero_width + self.spacing)
            wagon_y = hero_rect.bottom - self.hero_height

            # Рисуем вагон
            pygame.draw.rect(screen, (150, 150, 150), (wagon_x, wagon_y, self.hero_width, self.hero_height))

            # Рисуем юниты внутри вагона
            for unit in wagon:
                if unit['image'] and unit['rect']:
                    screen.blit(unit['image'], unit['rect'])

