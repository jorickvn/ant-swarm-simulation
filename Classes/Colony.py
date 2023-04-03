import pygame
from Classes.Ant import Ant
from Classes.Food import Food
from Classes.Pheromone import Pheromone

class Colony(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, screen, ant_group, pheromone_group, food_group, colony_group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([size, size])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.ant_group = ant_group
        self.pheromone_group = pheromone_group
        self.food_group = food_group
        self.colony_group = colony_group
        self.screen = screen

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, self.size)

    def spawn_ant(self):
        ant = Ant((0, 0, 0), self.x, self.y, 7, self.screen, self.pheromone_group, self.food_group, self.colony_group)
        self.ant_group.add(pygame.sprite.Group(ant))
        print("spawn ant")
