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
from background import Background

def run_game():
    """Main game loop"""
    # NOTE: Pre init to reduce audio lag and oddities
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    blast_settings = Settings()
    screen = pygame.display.set_mode(
        (blast_settings.screen_width, blast_settings.screen_height))
    pygame.display.set_caption("Blast!")
    play_button = Button(blast_settings, screen, "Play")
    stats = GameStats(blast_settings)
    sb = Scoreboard(blast_settings, screen, stats)
    ship = Ship(blast_settings, screen)
    bg = Background(screen)
    bullets = Group()
    enemies = Group()
    gf.create_fleet(blast_settings, screen, ship, enemies)
    menuMusic = pygame.mixer.Sound('../audio/menuMusic.ogg')
    menuMusic.play()
    
    while True:
        gf.check_events(blast_settings, screen, stats, sb, play_button, ship, 
            enemies, bullets)
        gf.update_screen(blast_settings, screen, stats, sb, ship, enemies,
            bullets, play_button, bg)
        if stats.game_active:
            menuMusic.stop()
            ship.update()
            gf.update_bullets(blast_settings, screen, stats, sb, ship, enemies, bullets)
            gf.update_enemies(blast_settings, screen, stats, sb, ship, enemies, bullets)

run_game()
