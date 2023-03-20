import pygame
import math
import random
from Classes.Pheromone import Pheromone

class Ant(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width, height, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.angle = random.uniform(0, 2*math.pi)  # starting angle is random
        self.speed = 1.5
        self.screen = screen
        self.ticksSincePheromoneDropped = 0
        self.pheromoneDropInterval = 5
        self.pheromoneType = "home"  # the type of pheromone this ant will drop
        self.pheromones = pygame.sprite.Group()  # list of pheromones dropped by this ant

    def move(self):
        # calculate new position based on angle and speed
        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed
        new_x = self.x + dx
        new_y = self.y + dy

        # check if new position is out of bounds
        if new_x < 0 or new_x > self.screen.get_width() or new_y < 0 or new_y > self.screen.get_height():
            # if out of bounds, randomly adjust angle to steer back into screen
            self.angle += random.uniform(-math.pi/4, math.pi/4)
        else:
            # if within bounds, move to new position
            self.x = new_x
            self.y = new_y

        # randomly adjust angle to create irregular movement
        self.angle += random.uniform(-math.pi/16, math.pi/16)

        # add current position to trail if step interval has passed
        self.ticksSincePheromoneDropped += 1
        if(self.ticksSincePheromoneDropped == self.pheromoneDropInterval):
            # drop a pheromone of the current type at the current position
            self.ticksSincePheromoneDropped = 0
            if self.pheromoneType is not None:
                self.pheromones.add(Pheromone(self.x, self.y, self.pheromoneType))

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), 2)

        # draw pheromones
        for p in self.pheromones:
            p.update()
            p.draw(self.screen)

    def update(self):
        self.move()
        self.draw()