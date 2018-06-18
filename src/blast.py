import sys
import pygame
import game_functions as gf
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from enemy import Alien

def run_game():
    """Main game loop"""
    # NOTE: Pre init to reduce audio lag and oddities
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    enemies = Group()
    gf.create_fleet(ai_settings, screen, ship, enemies)
    menuMusic = pygame.mixer.Sound('../audio/menuMusic.ogg')
    menuMusic.play()
    
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, 
            enemies, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, enemies,
            bullets, play_button)
        if stats.game_active:
            menuMusic.stop()
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, enemies, bullets)
            gf.update_enemies(ai_settings, screen, stats, sb, ship, enemies, bullets)

run_game()
