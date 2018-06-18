import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class for an enemy"""
    def __init__(self, ai_settings, screen):
        """Init an enemy and starting pos"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('../images/enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def blitme(self):
        """Blit enemy to screen"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Check left and right edges"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Update enemies speed and direction"""
        self.x += (self.ai_settings.enemy_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
