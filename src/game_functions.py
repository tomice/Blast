import sys
from time import sleep
import pygame
from bullet import Bullet
from enemy import Alien

def ship_hit(blast_settings, screen, stats, sb, ship, enemies, bullets):
    """Respond to ship being hit by enemies"""
    shipDeathSfx = pygame.mixer.Sound('../audio/shipExplosion.ogg')
    gameOverSfx = pygame.mixer.Sound('../audio/lastShipExplosion.ogg')

    if stats.ships_left > 0:
        stats.ships_left -= 1
        shipDeathSfx.play()
        sb.prep_ships()
        enemies.empty()
        bullets.empty()
        create_fleet(blast_settings, screen, ship, enemies)
        ship.center_ship()
        sleep(0.5)
    else:    
        gameOverSfx.play()
        pygame.mixer.music.stop()
        stats.game_active = False
        pygame.mouse.set_visible(True)

def get_number_of_enemies_x(blast_settings, enemy_width):
    """Determine the number of enemies that fit in a row"""
    available_space_x = blast_settings.screen_width - 2 * enemy_width
    number_enemies_x = int(available_space_x / (2 * enemy_width))
    
    return number_enemies_x

def get_number_rows(blast_settings, ship_height, enemy_height):
    """Determine number of rows"""
    available_space_y = (blast_settings.screen_height - 
                         (3 * enemy_height) - ship_height)
    number_rows = int(available_space_y / (2 * enemy_height))

    return number_rows

def create_enemy(blast_settings, screen, enemies, enemy_number, row_number):
    """Create an enemy and place in row"""
    enemy = Alien(blast_settings, screen)
    enemy_width = enemy.rect.width
    enemy.x = enemy_width + 2 * enemy_width * enemy_number
    enemy.rect.x = enemy.x
    enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * row_number
    enemies.add(enemy)

def create_fleet(blast_settings, screen, ship, enemies):
    """Create a fleet of enemies"""
    enemy = Alien(blast_settings, screen)
    number_enemies_x = get_number_of_enemies_x(blast_settings, enemy.rect.width)
    number_rows = get_number_rows(blast_settings, ship.rect.height, enemy.rect.height)

    for row_number in range(number_rows):
        for enemy_number in range(number_enemies_x):
            create_enemy(blast_settings, screen, enemies, enemy_number, row_number)
        
def check_keydown_events(event, blast_settings, screen, ship, bullets):
    """Respond to key press"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(blast_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
        
def fire_bullet(blast_settings, screen, ship, bullets):
    """Respond to a bullet fired"""
    laserSfx = pygame.mixer.Sound('../audio/laser.ogg')

    if len(bullets) < blast_settings.bullets_allowed:
        new_bullet = Bullet(blast_settings, screen, ship)
        bullets.add(new_bullet)
        laserSfx.play()

def check_keyup_events(event, ship):
    """Respond to key release."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(blast_settings, screen, stats, sb, play_button, ship, enemies, 
    bullets):
    """Respond to key and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(blast_settings, screen, stats, sb, play_button, 
                ship, enemies, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, blast_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_play_button(blast_settings, screen, stats, sb, play_button, ship, 
    enemies, bullets, mouse_x, mouse_y):
    """Start new game when player clicks Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('../audio/gameMusic.ogg')
        pygame.mixer.music.play(-1, 0)
        blast_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        enemies.empty()
        bullets.empty()
        create_fleet(blast_settings, screen, ship, enemies)
        ship.center_ship()

def update_screen(blast_settings, screen, stats, sb, ship, enemies, bullets, 
    play_button, bg):
    """Update images on the screen and flip to a new screen"""
    screen.fill(blast_settings.bg_color)
    bg.blitme()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    
    enemies.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def update_bullets(blast_settings, screen, stats, sb, ship, enemies, bullets):
    """Update position of bullets and remove old ones"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_enemy_collisions(blast_settings, screen, stats, sb, ship, 
        enemies, bullets)

def check_bullet_enemy_collisions(blast_settings, screen, stats, sb, ship, 
    enemies, bullets):
    """Respond to bullet-enemy collisions"""
    collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)
    enemySfx = pygame.mixer.Sound('../audio/enemyHit.ogg')
    
    if collisions:
        for enemies in collisions.values():
            stats.score += blast_settings.enemy_points * len(enemies)
            sb.prep_score()
            enemySfx.play()
        check_high_score(stats, sb)
    if len(enemies) == 0:
        bullets.empty()
        blast_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(blast_settings, screen, ship, enemies)

def check_enemies_bottom(blast_settings, screen, stats, sb, ship, enemies, 
    bullets):
    """Check if enemies reached bottom"""
    screen_rect = screen.get_rect()

    for enemy in enemies.sprites():
        if enemy.rect.bottom >= screen_rect.bottom:
            ship_hit(blast_settings, screen, stats, sb, ship, enemies, bullets)
            break

def update_enemies(blast_settings, screen, stats, sb, ship, enemies, bullets):
    """Update enemy sprites on the screen"""
    check_fleet_edges(blast_settings, enemies)
    check_enemies_bottom(blast_settings, screen, stats, sb, ship, enemies, bullets)
    enemies.update()
    if pygame.sprite.spritecollideany(ship, enemies):
        ship_hit(blast_settings, screen, stats, sb, ship, enemies, bullets)
    check_enemies_bottom(blast_settings, screen, stats, sb, ship, enemies, bullets)

def check_fleet_edges(blast_settings, enemies):
    """Check if enemies reach edge of screen"""
    for enemy in enemies.sprites():
        if enemy.check_edges():
            change_fleet_direction(blast_settings, enemies)
            break

def change_fleet_direction(blast_settings, enemies):
    """Allow enemies to move left/right"""
    for enemy in enemies.sprites():
        enemy.rect.y += blast_settings.fleet_drop_speed
    blast_settings.fleet_direction *= -1

def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        save_high_score(stats)
        sb.prep_high_score()

def save_high_score(stats):
    """Save high score to file"""
    # FIXME: This basically repeats what's inside of game_stats.py
    high_score_file = open("highscore.txt", "w")
    high_score_file.write(str(stats.score))
    high_score_file.close()
