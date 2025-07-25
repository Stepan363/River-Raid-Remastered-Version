import pygame
import settings


class Turretclass:
    def __init__(self, turret_rect):
        self.image = pygame.image.load("images/turret.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = turret_rect.x
        self.rect.y = turret_rect.y
        self.direction = 'null'

    def update(self):
        # yet to type
        self.rect.y += settings.game_speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def off_screen(self, height):
        return self.rect.y > 1080   