import math
import pygame


class Bullet:
    def __init__(self, max_x, max_y, spaceship):
        self.max_x = max_x
        self.max_y = max_y

        self.xpos = spaceship.xpos+spaceship.size/2.0*math.cos(math.radians(spaceship.angle))
        self.ypos = spaceship.ypos+spaceship.size/2.0*math.sin(math.radians(spaceship.angle))

        vel_magnitude = 5.0

        self.xvel = spaceship.xvel + vel_magnitude*math.cos(math.radians(spaceship.angle))
        self.yvel = spaceship.yvel + vel_magnitude*math.sin(math.radians(spaceship.angle))

        self.length = 5
        self.width = 2

        self.angle = spaceship.angle

    def step(self):
        self.xpos = self.xpos + self.xvel
        self.ypos = self.ypos + self.yvel


    def draw(self, surface):
         pygame.draw.polygon(surface, (0,0,0), 
                             [[self.xpos, self.ypos],
                              [self.xpos+self.length*math.cos(math.radians(self.angle)), 
                               self.ypos+self.length*math.sin(math.radians(self.angle))]],
                             self.width)

    def check_bullet_hit(self, asteroid):
        dist_x_base = abs(self.xpos - asteroid.xpos)
        dist_y_base = abs(self.ypos - asteroid.ypos)

        dist_base = math.sqrt(dist_x_base*dist_x_base + dist_y_base*dist_y_base)

        dist_x_tip = abs(self.xpos + self.length*math.cos(math.radians(self.angle)))
        dist_y_tip = abs(self.ypos + self.length*math.sin(math.radians(self.angle)))

        dist_tip = math.sqrt(dist_x_tip*dist_x_tip + dist_y_tip*dist_y_tip)

        if dist_base < asteroid.size or dist_tip < asteroid.size:
            return 1
        return 0

    def is_valid(self):
        if self.xpos < 0 or self.xpos > self.max_x or self.ypos < 0 or self.ypos > self.max_y:
            return 0
        return 1 
