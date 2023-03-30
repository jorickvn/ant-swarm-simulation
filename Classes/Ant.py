import pygame
import math
import random
from Classes.Pheromone import Pheromone


class Ant(pygame.sprite.Sprite):
    def __init__(self, color, x, y, size, screen, pheromone_group, food_group, colony_group):

        # Sprite and image
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size * 1.5, size * 0.7))
        self.color = color
        self.image.fill((self.color))
        self.original_image = self.image
        self.rect = self.image.get_rect()

        # Storing globals
        self.screen = screen
        self.pheromone_group = pheromone_group
        self.food_group = food_group
        self.colony_group = colony_group

        # Movement and rotation
        self.rect.x = x
        self.rect.y = y
        self.angle = random.uniform(0, 2 * math.pi)  # starting angle is random
        self.speed = 3
        self.destination = None

        # Pheromones
        self.pheromone_type = "home"  # the type of pheromone this ant will drop
        self.ticksSincePheromoneDropped = 21
        self.pheromoneDropInterval = 22
        self.strongest_recent_pheromone = None

        # Food
        self.has_food = False

        # Senses
        self.pheromone_sense_sprite = pygame.sprite.Sprite()
        self.pheromone_sense_sprite.rect = pygame.Rect(self.rect.x, self.rect.y, 130, 130)

    def setDestination(self, destination):
        self.destination = [destination.rect.x, destination.rect.y]

    def turnToDestination(self):
        if self.destination is not None:
            dx = self.destination[0] - self.rect.x
            dy = self.destination[1] - self.rect.y
            self.angle = math.atan2(dy, dx)

        # add some randomness to the angle of rotation
        self.angle += random.uniform(-math.pi/16, math.pi/16)
        self.image = pygame.transform.rotate(self.original_image, math.degrees(-self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self):
        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        if new_x < 0 or new_x > self.screen.get_width() or new_y < 0 or new_y > self.screen.get_height():
            self.angle += random.uniform(-math.pi/4, math.pi/4)
        else:
            self.rect.x = new_x
            self.rect.y = new_y
            self.pheromone_sense_sprite.rect.center = self.rect.center

        self.ticksSincePheromoneDropped += 1
        if (self.ticksSincePheromoneDropped == self.pheromoneDropInterval):
            self.ticksSincePheromoneDropped = 0
            self.drop_pheromone()

    def draw(self):
        # draw self
        pygame.draw.rect(self.screen, self.color, self.rect)

        # draw pheromone sense
        #pygame.draw.rect(self.screen, (255, 255, 255), self.pheromone_sense_sprite.rect, 2)

    def update(self):
        self.checkIfPheromoneReached()
        self.turnToDestination()
        self.move()

    def drop_pheromone(self):
        if self.pheromone_type != None:
            pheromone = Pheromone(self.rect.x, self.rect.y, self.pheromone_type, self.screen)
            self.pheromone_group.add(pygame.sprite.Group(pheromone))

    def check_food_collision(self, food_group):
        food_collision = pygame.sprite.spritecollideany(self, food_group)
        if food_collision:
            if self.has_food == False:
                self.has_food = True
                self.pheromone_type = "food"
                self.strongest_recent_pheromone = None
                self.drop_pheromone()
                food_collision.kill()

    def check_colony_collision(self, colony_group):
        colony_collision = pygame.sprite.spritecollideany(self, colony_group)
        if colony_collision:
            if self.has_food == True:
                self.has_food = False
                colony_collision.spawn_ant()
                self.pheromone_type = "home"
                self.strongest_recent_pheromone = None
                self.drop_pheromone()

    def check_vision_collision(self):
        if self.has_food == False:
            food_collisions = pygame.sprite.spritecollide(self.pheromone_sense_sprite, self.food_group, False)
            if food_collisions:
                self.setDestination(food_collisions[0])
                return

        if self.has_food == True:
            colony_collisions = pygame.sprite.spritecollide(self.pheromone_sense_sprite, self.colony_group, False)
            if colony_collisions:
                self.setDestination(colony_collisions[0])
                return

        pheromone_collisions = pygame.sprite.spritecollide(self.pheromone_sense_sprite, self.pheromone_group, False)
        for pheromone_collision in pheromone_collisions:
            if pheromone_collision is not None:
                if self.strongest_recent_pheromone is None:
                    if self.pheromone_type != pheromone_collision.type and pheromone_collision.type != None:
                        self.strongest_recent_pheromone = pheromone_collision
                        self.setDestination(pheromone_collision)
    
                elif self.pheromone_type != pheromone_collision.type and pheromone_collision.type != None:
                    if self.strongest_recent_pheromone.age < pheromone_collision.age:
                        self.setDestination(pheromone_collision)
                        self.strongest_recent_pheromone = pheromone_collision
    
    def checkIfPheromoneReached(self):
        if self.destination is not None:
            pheromone_distance = ((self.rect.centerx - self.destination[0]) ** 2 + (self.rect.centery - self.destination[1]) ** 2) ** 0.5
            if pheromone_distance <= 30: # adjust this value to change the distance threshold
                self.destination = None
