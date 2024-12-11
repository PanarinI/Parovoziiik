import pygame
import random

TEXTS_PRO = ["Где бюджет проекта?", "Какие метрики эффективности?", "Почему столько тупорезов?"]
TEXTS_DUMB = ["Больше пиара!", "А зачем нам показатели?", "Всё идёт по плану!"]
COLOR_MAP = {"A": (255, 0, 0), "B": (0, 255, 0), "silent": (200, 200, 200)}

class Unit:
    def __init__(self, x, y, size, unit_type):
        self.rect = pygame.Rect(x, y, size, size)
        self.type = unit_type  # "A" - профессионал, "B" - тупорез, "silent" - молчаливый
        self.color = COLOR_MAP[self.type]

        # Установка изображения
        self.image = pygame.Surface((size, size))
        self.image.fill(self.color)

        # Текстовое облачко
        self.text = None
        if self.type == "A":  # Профессионал
            self.text = random.choice(TEXTS_PRO)
        elif self.type == "B":  # Тупорез
            self.text = random.choice(TEXTS_DUMB)
        # "silent" не имеет текста

        # Таймер для текста (3 секунды)
        self.text_timer = pygame.time.get_ticks() + 3000

    def update(self, speed):
        """Обновление позиции юнита."""
        self.rect.x -= speed

    def draw(self, screen):
        """Отрисовка юнита и его текста (если есть)."""
        screen.blit(self.image, self.rect)
        if self.text and pygame.time.get_ticks() < self.text_timer:
            # Рисуем облачко текста
            text_surface = pygame.font.Font(None, 20).render(self.text, True, (0, 0, 0))
            pygame.draw.ellipse(screen, (255, 255, 255), (self.rect.x - 10, self.rect.y - 40, 120, 30))
            screen.blit(text_surface, (self.rect.x, self.rect.y - 35))

    def get_image(self):
        """Возвращает изображение юнита."""
        return self.image

    def is_off_screen(self, screen_width):
        """Проверяет, ушёл ли юнит за экран."""
        return self.rect.right < 0

    @staticmethod
    def spawn(units, max_units, spawn_x_range, ground_y, unit_size):
        """Создаёт новых юнитов на экране."""
        if len(units) < max_units:
            unit_x = random.randint(*spawn_x_range)
            unit_y = ground_y - unit_size
            # Вероятности появления типов
            unit_type = random.choices(
                ["A", "B", "silent"],  # Профессионал, тупорез, молчаливый
                weights=[0.3, 0.5, 0.2],  # Вероятности 30%, 50%, 20%
                k=1
            )[0]
            units.append(Unit(unit_x, unit_y, unit_size, unit_type))
