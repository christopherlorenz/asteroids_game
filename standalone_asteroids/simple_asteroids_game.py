import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pygame
import sys
import time

from pygame.locals import *

from asteroid import Asteroid
from spaceship import Spaceship



def build_game():
    # Game board parameters
    FPS = 30
    pygame.init()
    fpsClock = pygame.time.Clock()
    SCREEN_WIDTH, SCREEN_HEIGHT = 640, 640
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    surface.fill((255,255,255))
    clock = pygame.time.Clock()
    myfont = pygame.font.SysFont("monospace", 20)
    endfont = pygame.font.SysFont("monospace", 30)

    pygame.key.set_repeat(1, 20)

    score = 0
    num_asteroids = 20
    asteroids = []

    # Initialize spaceship and asteroids
    spaceship = Spaceship(SCREEN_WIDTH, SCREEN_HEIGHT)
    for i in range(0,num_asteroids):
        new_ast = Asteroid(SCREEN_WIDTH, SCREEN_HEIGHT)
        asteroids.append(new_ast)

    shoot_bullet_prevent_auto = 1

    # Run game
    while True:
        # Fill area with white
        surface.fill((255,255,255))

        shoot_bullet = 0

        # Get keys for thrust and direction
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and keys[K_RIGHT]:
            angular_vel = 0
        elif keys[K_LEFT]:
            angular_vel = -1
        elif keys[K_RIGHT]:
            angular_vel = 1
        else:
            angular_vel = 0
        if keys[K_UP]:
            thrust_on = 1
        else:
            thrust_on = 0

        # Get spacebar press for firing bullet, force new press for each shot
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if shoot_bullet_prevent_auto:
                        shoot_bullet = 1
                        shoot_bullet_prevent_auto = 0
            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    shoot_bullet_prevent_auto = 1

        # Draw asteroids and check if they've exited the playing area
        for num, asteroid in enumerate(asteroids):
            asteroid.step()
            if asteroid.is_valid():
                pygame.draw.circle(surface,asteroid.color,
                (int(asteroid.xpos), int(asteroid.ypos)),asteroid.size)
            # Create new asteroid and delete old when exists playing area
            else:
                asteroids.pop(num)
                new_ast = Asteroid(SCREEN_WIDTH, SCREEN_HEIGHT)
                asteroids.append(new_ast)

        # Move spaceship for this timestep, check if dead
        spaceship.step(thrust_on, angular_vel, shoot_bullet)
        lives = spaceship.check_collision(asteroids)
        if lives:
            spaceship.draw(surface)
        # If dead, display final score
        else:
            while True:
                screen.blit(surface, (0,0))
                gameover_text = endfont.render("GAME OVER", 1, (0,0,0))
                score_text = endfont.render("YOUR SCORE: {0}".format(score), 1, (0,0,0))
                screen.blit(gameover_text, (SCREEN_WIDTH/2.0-100.0,SCREEN_HEIGHT/2.0-50.0))
                screen.blit(score_text, (SCREEN_WIDTH/2.0-100.0,SCREEN_HEIGHT/2.0))

                pygame.display.flip()
                pygame.display.update()
               
        # Delete bullets and asteroids that collide, redraw bullets
        num_hits = spaceship.check_bullet_hits(asteroids)
        score = score + num_hits
        spaceship.draw_bullets(surface)

        # Render game and overlay score
        screen.blit(surface, (0,0))
        scoretext = myfont.render("Score {0}".format(score), 1, (0,0,0))
        screen.blit(scoretext, (0,0))

        # Display everything
        pygame.display.flip()
        pygame.display.update()
        fpsClock.tick(FPS)


def main():
    build_game()


if __name__ == "__main__":
    main()


