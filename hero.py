import pygame

class Hero:
    def __init__(self, x, y, width, height, jump_strength, gravity, ground_height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed_y = 0
        self.is_jumping = False
        self.jump_strength = jump_strength
        self.gravity = gravity
        self.ground_height = ground_height

    def update(self):
        self.speed_y += self.gravity
        self.rect.y += self.speed_y
        if self.rect.bottom > self.ground_height:
            self.rect.bottom = self.ground_height
            self.speed_y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.speed_y = self.jump_strength
            self.is_jumping = True

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)
