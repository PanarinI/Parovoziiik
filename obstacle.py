import pygame

class Obstacle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:  # Сброс за экраном
            self.rect.x = 800

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
