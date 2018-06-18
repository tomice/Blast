import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Mgmt class for bullets fired from ship"""
    def __init__(self, blast_settings, screen, ship):
        """Create bullet obj at ship's current pos"""
        super(Bullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, blast_settings.bullet_width, blast_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)
        self.color = blast_settings.bullet_color
        self.speed_factor = blast_settings.bullet_speed_factor

    def update(self):
        """Move bullet up screen"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet on screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
