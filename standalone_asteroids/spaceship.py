import math
import pygame

from asteroid import Asteroid
from bullet import Bullet

class Spaceship:
    def __init__(self, max_x, max_y):
        # Set position to center
        self.xpos = max_x/2.0
        self.ypos = max_y/2.0

        self.max_x = max_x
        self.max_y = max_y

        # Start at 0 velocity
        self.xvel = 0.0
        self.yvel = 0.0

        self.angle = 0.0
        self.angular_vel = 0.0
        self.angular_vel_factor = 5.0

        self.acc_magnitude = 0.2

        self.size = 20.0

        # Set color to black
        self.color = (0.0, 0.0, 0.0)

        self.bullets = []

    def step(self, thrust_on, angular_vel, shoot_bullet):
        # Update velocities with acceleration input
        self.xvel = self.xvel + thrust_on*math.cos(math.radians(self.angle))*self.acc_magnitude
        self.yvel = self.yvel + thrust_on*math.sin(math.radians(self.angle))*self.acc_magnitude

        # Simple friction factor to slow down
        self.xvel = self.xvel*0.985
        self.yvel = self.yvel*0.985

        self.angular_vel = angular_vel*self.angular_vel_factor
        # Update positions with velocity data
        self.xpos = self.xpos + self.xvel
        self.ypos = self.ypos + self.yvel
        self.angle = self.angle + self.angular_vel

        # Deal with my bullets
        if shoot_bullet:
            self.spawn_new_bullet()

        self.step_bullets()


    def draw(self, surface):
        pygame.draw.polygon(surface, (0,0,0),
                            [[self.xpos+self.size/2.0*math.cos(math.radians(self.angle)), self.ypos+self.size/2.0*math.sin(math.radians(self.angle))],
                             [self.xpos+self.size/2.0*math.cos(math.radians(self.angle+135.0)), self.ypos+self.size/2.0*math.sin(math.radians(self.angle+135.0))],
                             [self.xpos+self.size/4.0*math.cos(math.radians(self.angle+180.0)), self.ypos+self.size/4.0*math.sin(math.radians(self.angle+180.0))],
                             [self.xpos+self.size/2.0*math.cos(math.radians(self.angle+225.0)), self.ypos+self.size/2.0*math.sin(math.radians(self.angle+225.0))]],
                            2)



    def check_collision(self, asteroids):
        for asteroid in asteroids:
            dist_x = abs(self.xpos - asteroid.xpos)
            dist_y = abs(self.ypos - asteroid.ypos)
            dist = math.sqrt(dist_x*dist_x + dist_y*dist_y)

            # Check if collided, asteroid size is already radius 
            if dist < (self.size/2.0 + asteroid.size):
                return 0
        return 1

    
    def spawn_new_bullet(self):
        new_bullet = Bullet(self.max_x, self.max_y, self)
        self.bullets.append(new_bullet)


    def step_bullets(self):
        for num_bullet, bullet in enumerate(self.bullets):
            bullet.step()
            if not bullet.is_valid():
                self.bullets.pop(num_bullet)


    def draw_bullets(self, surface):
        for bullet in self.bullets:
            bullet.draw(surface)


    def check_bullet_hits(self, asteroids):
        num_hits = 0
        for num_bullet, bullet in enumerate(self.bullets):
            for num_asteroid, asteroid in enumerate(asteroids):
                hit = bullet.check_bullet_hit(asteroid)
                if hit:
                    self.bullets.pop(num_bullet)
                    asteroids.pop(num_asteroid)
                    num_hits = num_hits + 1
                    new_ast = Asteroid(self.max_x, self.max_y)
                    asteroids.append(new_ast)
                    break
        return num_hits






