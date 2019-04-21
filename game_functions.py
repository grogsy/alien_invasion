'''functions for the game'''
import random
import sys
import time
import pygame

from alien import Alien
from bullet import Bullet, AlienBullet

###################
#####Constants#####
###################
BTN_PRESS  = pygame.KEYDOWN
RELEASED   = pygame.KEYUP
MOVE_RIGHT = pygame.K_RIGHT
MOVE_LEFT  = pygame.K_LEFT
MOVE_UP    = pygame.K_UP
MOVE_DOWN  = pygame.K_DOWN
FIRE_ONE   = pygame.K_z
FIRE_TWO   = pygame.K_SPACE
QUIT       = pygame.K_q
CLICK      = pygame.MOUSEBUTTONDOWN
ESCAPE     = pygame.K_ESCAPE

####################
###Event methods####
####################
def check_events(meta_objs, game_objs):
    '''Respond to keypresses and mouse movement as well as track other events
       occurring during an instance of the game
       Method is called from the main game loop
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == BTN_PRESS:
            check_button_pressed(event, meta_objs, game_objs)
        elif event.type == RELEASED:
            check_button_released(event, game_objs)
        elif event.type == CLICK:
            if meta_objs.buttons.play.activatable:
                mousex, mousey = pygame.mouse.get_pos()
                check_play_button(meta_objs, game_objs, mousex, mousey)


def check_button_pressed(event, meta_objs, game_objs):
    '''function that is run if a button is pressed down.
       if a move key is held down, ship will continue to move
       in specified direction.
    '''
    if event.key == MOVE_RIGHT:
        game_objs.ship.moving_right = True
    elif event.key == MOVE_LEFT:
        game_objs.ship.moving_left = True
    elif event.key == MOVE_UP:
        game_objs.ship.moving_up = True
    elif event.key == MOVE_DOWN:
        game_objs.ship.moving_down = True
    elif event.key == FIRE_ONE or event.key == FIRE_TWO:
        fire_bullet(meta_objs, game_objs)
    elif event.key == QUIT:
        sys.exit()
    elif event.key == ESCAPE:
        switch_pause(meta_objs)

def check_button_released(event, game_objs):
    '''Key presses are released. Mainly concerned about ship movement'''
    if event.key == MOVE_RIGHT:
        game_objs.ship.moving_right = False
    elif event.key == MOVE_LEFT:
        game_objs.ship.moving_left = False
    elif event.key == MOVE_UP:
        game_objs.ship.moving_up = False
    elif event.key == MOVE_DOWN:
        game_objs.ship.moving_down = False


def check_play_button(meta_objs, game_objs, mousex, mousey):
    '''Start game when player clicks on screen
       Make play button uninteractable while main game loops
       is in effect
       Reset the stats upon starting a new game
    '''
    if meta_objs.buttons.play.rect.collidepoint(mousex, mousey):
        meta_objs.stats.reset_stats()
        # Reset and display level 1
        meta_objs.scoreboard.prep_level()
        meta_objs.settings.initialize_dynamic_settings()
        meta_objs.stats.active = True
        meta_objs.buttons.play.activatable = False

        game_objs.aliens.empty()
        game_objs.bullets.empty()

        create_alien_fleet(meta_objs, game_objs)
        game_objs.ship.center_ship()


def switch_pause(meta_objs):
    '''Pause/Unpause game
       These boolean stats attributes act like toggle switches
    '''
    meta_objs.stats.paused = not meta_objs.stats.paused
    meta_objs.stats.active = not meta_objs.stats.active


def fire_bullet(meta_objs, game_objs):
    '''function for firing projectile.
       Method is called from check_button_pressed()
       if the player toggles the fire button
    '''
    # limit the number of shots fired
    # to the number specified in settings
    if len(game_objs.bullets) < meta_objs.settings.available_bullets:
        # Create a new bullet and add it to the bullets group
        bullet = Bullet(meta_objs.settings, meta_objs.screen, game_objs.ship)
        game_objs.bullets.add(bullet)
        meta_objs.stats.shots_fired += 1

#######################
#Screen update methods#
#######################
def update_bullets(meta_objs, game_objs):
    '''Update position of bullets and remove bullets that have fallen off the surface
       Method is called by the game's main loop
    '''
    # Calling a method on a pygame.Group object
    # causes every obj in the group to call that method.
    # In this case we are calling the Bullet.update()
    # method and the bullets group is a collection of
    # bullets so all the bullets in effect
    # call their update method
    game_objs.bullets.update()
    game_objs.alien_bullets.update()

    for bullet in game_objs.bullets.copy():
        if bullet.rect.bottom <= 0:
            game_objs.bullets.remove(bullet)

    for bullet in game_objs.alien_bullets.copy():
        if bullet.rect.bottom > 1000:
            game_objs.alien_bullets.remove(bullet)

    check_bullet_collisions(meta_objs, game_objs)


def check_bullet_collisions(meta_objs, game_objs):
    '''Respond to bullet-alien collisions
       Remove any bullets and aliens that have collided
       Tally score for every alien shot down
    '''
    collisions = pygame.sprite.groupcollide(game_objs.bullets, game_objs.aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            meta_objs.stats.shots_landed += 1
            meta_objs.stats.play_score += meta_objs.settings.alien_points
            meta_objs.scoreboard.prep_score()

    # Entire fleet destroyed
    if not game_objs.aliens:
        # Increase the level
        meta_objs.stats.level += 1
        meta_objs.scoreboard.prep_level()
        # Modify game settings
        meta_objs.settings.increase_speed(meta_objs.stats.level)
        # Adjust ship speed
        game_objs.ship.adjust_ship_speed(meta_objs.settings.ship_speed_factor)
        # reset the board
        reset_board(meta_objs, game_objs)


def update_aliens(meta_objs, game_objs):
    '''update the position of all aliens in the fleet
       Called from the main game loop
    '''
    check_fleet_edges(meta_objs, game_objs)
    game_objs.aliens.update()

    check_alien_collision(meta_objs, game_objs)

    for alien in game_objs.aliens.sprites():
        # TODO: Find a better way to get aliens to fire
        if random.choice(range(1000000)) % (len(game_objs.aliens)*meta_objs.settings.alien_fire_rate) == 0:
            fire_alien_bullet(alien, meta_objs, game_objs)

    check_aliens_bottom(meta_objs, game_objs)


def check_alien_collision(meta_objs, game_objs):
    '''check if aliens or their bullets make contact with ship'''
    if (pygame.sprite.spritecollideany(game_objs.ship, game_objs.aliens) or
    pygame.sprite.spritecollideany(game_objs.ship, game_objs.alien_bullets)):
        game_objs.alien_bullets.empty()
        ship_hit(meta_objs, game_objs)



def fire_alien_bullet(alien, meta_objs, game_objs):
    bullet = AlienBullet(meta_objs.settings, meta_objs.screen, alien, speed=random.uniform(.5, 2.5))
    game_objs.alien_bullets.add(bullet)


def ship_hit(meta_objs, game_objs):
    '''Respond to ship being hit by alien by restarting the board
       and deducting 1 life
    '''
    if meta_objs.stats.ships_left > 0:
        meta_objs.stats.ships_left -= 1
        reset_board(meta_objs, game_objs)
        # Short pause
        time.sleep(0.5)
    else:
        game_over(meta_objs, game_objs)


def reset_board(meta_objs, game_objs):
    '''Reinitialize board'''
    game_objs.aliens.empty()
    game_objs.bullets.empty()
    create_alien_fleet(meta_objs, game_objs)


def game_over(meta_objs, game_objs):
    '''Run when player has no extra ships left'''
    check_high_score(meta_objs)
    # Game is now inactive
    meta_objs.stats.active             = False
    # Play button is not interactable
    meta_objs.buttons.play.activatable = True
    meta_objs.settings.initialize_dynamic_settings()
    # Reset ship speed
    game_objs.ship.adjust_ship_speed(meta_objs.settings.ship_speed_factor)


def check_high_score(meta_objs):
    '''Check to see if there's a new high score, called when game is over'''
    if meta_objs.stats.play_score > meta_objs.stats.high_score:
        meta_objs.stats.high_score = meta_objs.stats.play_score
        meta_objs.scoreboard.prep_high_score()
    # TODO: Have a rolling credits display all high scores


def check_aliens_bottom(meta_objs, game_objs):
    '''Check if any aliens reach the bottom of the screen'''
    screen_rect = meta_objs.screen.get_rect()
    for alien in game_objs.aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat it as ship hit
            ship_hit(meta_objs, game_objs)
            break


def update_screen(meta_objs, game_objs):
    '''Update the game surface
       Method is called by the game's main loop
    '''
    # Redraw the screen on every loop iteration
    meta_objs.screen.fill(meta_objs.settings.bg_color)

    # Draw stars & bullets being fired on the surface first,
    for star in game_objs.stars.sprites():
        star.draw_star()
    for bullet in game_objs.bullets.sprites():
        bullet.draw_bullet()
    for bullet in game_objs.alien_bullets.sprites():
        bullet.draw_bullet()

    # then the ship and aliens
    game_objs.ship.blitme()
    # draw() here is a method belonging to pygame.sprite.Group()
    game_objs.aliens.draw(meta_objs.screen)
    # Update star positions
    game_objs.stars.update()

    # Display current score
    meta_objs.scoreboard.show_score()

    # Draw the play button if the game is inactive
    if not meta_objs.stats.active and meta_objs.buttons.play.activatable:
        meta_objs.buttons.play.draw_button()
    elif meta_objs.stats.paused:
        meta_objs.buttons.pause.draw_button()

    # Make most recently drawn screen visible
    pygame.display.flip()


#####################
#Alien spawn methods#
#####################
def create_alien_fleet(meta_objects, game_objects):
    '''Spawn a full fleet of aliens
       This function is called in the main game file
    '''
    # Calculate how many aliens fit into a row
    # based off the rect of the alien
    alien            = Alien(meta_objects.settings, meta_objects.screen)
    fleet_size       = get_fleet_size(meta_objects.settings, alien.rect.width)
    num_rows         = get_vertical_space(meta_objects.settings,
                                          game_objects.ship.rect.height,
                                          alien.rect.height)

    # Create rows of aliens
    for row in range(num_rows):
        # Fit alien size to row
        for i in range(fleet_size):
            create_alien(meta_objects, game_objects, i, row)


def get_fleet_size(settings, alien_width):
    PADDING = 400
    '''Get how many aliens can fit into a single row'''
    horizantal_space = settings.screen_width - 2 * alien_width - PADDING
    fleet_size       = int(horizantal_space / (2*alien_width))

    return fleet_size


def create_alien(meta_objects, game_objects, num, row):
    '''Create aliens and place them into the row'''
    alien        = Alien(meta_objects.settings, meta_objects.screen)
    width        = alien.rect.width
    alien.x      = width + 2 * width * num
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row + 40
    # Add this alien to the group
    game_objects.aliens.add(alien)


def get_vertical_space(settings, ship_height, alien_height):
    '''Determine the number of rows of aliens that fit on the screen'''
    vertical_space = (settings.screen_height - (12*alien_height) - ship_height)-100
    # Magic to me, but this gets me 3 rows with my alien img
    rows           = int(vertical_space / (2 * alien_height))

    return rows

########################
#Alien Movement methods#
########################
def check_fleet_edges(meta_objs, game_objs):
    '''Respond appropriately if aliens have reached the edge of the screen
       Called in update_aliens()
    '''
    for alien in game_objs.aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(meta_objs, game_objs)
            break


def change_fleet_direction(meta_objs, game_objs):
    '''Drop the entire fleet and change the fleet's direction'''
    for alien in game_objs.aliens.sprites():
        alien.rect.y += meta_objs.settings.fleet_drop_speed
    meta_objs.settings.fleet_direction *= -1
