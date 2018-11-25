import random


class Asteroid:
    def __init__(self, max_x, max_y):
        # Size
        size_magnitude = 30.0
        self.size = int(size_magnitude + random.random()*size_magnitude)

        # Choose start position from 4 sides randomly, each side equally weighted
        from_x = int(random.random()*2.0)
        from_top_right = int(random.random()*2.0)

        # Set position on side, and then set velocity so it heads somewhere
        # towards the middle
        vel_magnitude = 3.0
        if from_x and from_top_right:
            self.xpos = random.random()*max_x
            self.ypos = max_y+self.size
            self.xvel = (random.random()-0.5*2.0)
            self.yvel = -random.random()*vel_magnitude
        elif from_x and not from_top_right:
            self.xpos = random.random()*max_x
            self.ypos = 0.0-self.size
            self.xvel = (random.random()-0.5)*2.0
            self.yvel = random.random()*vel_magnitude
        elif not from_x and from_top_right:
            self.xpos = max_x+self.size
            self.ypos = random.random()*max_y
            self.xvel = -random.random()*vel_magnitude
            self.yvel = (random.random()-0.5)*2.0
        else:
            self.xpos = 0.0-self.size 
            self.ypos = random.random()*max_y
            self.xvel = random.random()*vel_magnitude
            self.yvel = (random.random()-0.5)*2.0

        self.max_x = max_x
        self.max_y = max_y


        # Set to random RBG triple
        self.color = (random.random()*256, random.random()*256, random.random()*256) 

    def step(self):
        self.xpos = self.xpos + self.xvel
        self.ypos = self.ypos + self.yvel

    def get_pos(self):
        return (self.xpos, self.ypos)

    def is_valid(self):
        # Kill once they leave the screen completely
        if (self.xpos+self.size < 0 or self.xpos-self.size > self.max_x or self.ypos+self.size < 0 or self.ypos-self.size > self.max_y):
            return 0
        else:
            return 1






