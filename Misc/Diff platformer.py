import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = -7
ASTEROID_SPEED = 3

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Экран
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# Загрузка изображений
player_image = pygame.image.load("player_ship.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 50))
asteroid_image = pygame.image.load("asteroid.png").convert_alpha()
asteroid_image = pygame.transform.scale(asteroid_image, (50, 50))
bullet_image = pygame.image.load("bullet.png").convert_alpha()
bullet_image = pygame.transform.scale(bullet_image, (10, 30))

# Игрок
class Player:
    def __init__(self):
        self.image = player_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.speed = PLAYER_SPEED

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Пуля
class Bullet:
    def __init__(self, x, y):
        self.image = bullet_image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += BULLET_SPEED
        return self.rect.bottom > 0  #
