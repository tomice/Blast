import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Parent ship class for Blast."""
    def __init__(self, blast_settings, screen):
        """Init ship and starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.blast_settings = blast_settings
        self.image = pygame.image.load('../images/player.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.vertical = float(self.rect.centery)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's pos based on the movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.blast_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.blast_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.vertical -= self.blast_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.vertical += self.blast_settings.ship_speed_factor
        self.rect.centerx = self.center
        self.rect.centery = self.vertical
    
    def blitme(self):
        """Draw ship at current location."""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Center ship on screen"""
        self.center = self.screen_rect.centerx
        # FIXME: Arbitrary "magic number" to get ship to bottom
        self.vertical = self.screen_rect.bottom - 25
