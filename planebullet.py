import pygame

class Planebullet:
    def __init__(self, plane_rect):
        self.image = pygame.image.load("images/planes_bullet1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = plane_rect.x
        self.rect.y = plane_rect.y

    def update(self):
        self.rect.y -= 6  # Move the bullet upwards

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def off_screen(self, height):
        return self.rect.bottom < 0
