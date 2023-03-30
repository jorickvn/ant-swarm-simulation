import pygame
import math
import random
from Classes.Pheromone import Pheromone


class Ant(pygame.sprite.Sprite):
    def __init__(self, color, x, y, size, screen, pheromone_group):

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

        # Movement and rotation
        self.rect.x = x
        self.rect.y = y
        self.angle = random.uniform(0, 2 * math.pi)  # starting angle is random
        self.speed = 3

        # Pheromones
        self.pheromone_type = "home"  # the type of pheromone this ant will drop
        self.ticksSincePheromoneDropped = 13
        self.pheromoneDropInterval = 14
        self.strongest_recent_pheromone = None

        # Food
        self.has_food = False

        # Senses
        self.pheromone_sense_sprite = pygame.sprite.Sprite()
        self.pheromone_sense_sprite.rect = pygame.Rect(self.rect.x, self.rect.y, 100, 100)

    def moveToPheromone(self):
        if self.strongest_recent_pheromone is not None:
            # calculate angle and distance to strongest recent pheromone
            dx = self.strongest_recent_pheromone.rect.x - self.rect.x
            dy = self.strongest_recent_pheromone.rect.y - self.rect.y
            self.angle = math.atan2(dy, dx)

        else:
            # randomly adjust angle to create irregular movement
            self.angle += random.uniform(-math.pi/32, math.pi/32)

          # calculate new position based on angle and speed
        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        
        # check if new position is out of bounds
        if new_x < 0 or new_x > self.screen.get_width() or new_y < 0 or new_y > self.screen.get_height():
            # if out of bounds, randomly adjust angle to steer back into screen
            self.angle += random.uniform(-math.pi/4, math.pi/4)
        else:
            # if within bounds, move to new position
            self.rect.x = new_x
            self.rect.y = new_y
            self.pheromone_sense_sprite.rect.center = self.rect.center
        
        # rotate rectangle based on angle
        self.image = pygame.transform.rotate(self.original_image, math.degrees(-self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)
        
        # add current position to trail if step interval has passed
        self.ticksSincePheromoneDropped += 1
        if (self.ticksSincePheromoneDropped == self.pheromoneDropInterval):
            # drop a pheromone of the current type at the current position
            self.ticksSincePheromoneDropped = 0
            self.drop_pheromone()

    def draw(self):
        # draw self
        pygame.draw.rect(self.screen, self.color, self.rect)

        # draw pheromone sense
        # pygame.draw.rect(self.screen, (255, 255, 255), self.pheromone_sense_sprite.rect, 2)

    def update(self):
        self.checkIfPheromoneReached()
        self.moveToPheromone()

    def drop_pheromone(self):
        if self.pheromone_type is not None:
            pheromone = Pheromone(self.rect.x, self.rect.y, self.pheromone_type, self.screen)
            self.pheromone_group.add(pygame.sprite.Group(pheromone))

    def check_food_collision(self, food_group):
        food_collision = pygame.sprite.spritecollideany(self, food_group)
        if food_collision:
            if self.has_food == False:
                self.has_food = True
                self.pheromone_type = "food"
                print("Picked up food")
                self.strongest_recent_pheromone = None
                self.drop_pheromone()
                food_collision.kill()

    def check_colony_collision(self, colony_group):
        colony_collision = pygame.sprite.spritecollideany(self, colony_group)
        if colony_collision:
            if self.has_food == True:
                self.has_food = False
                self.pheromone_type = "home"
                self.strongest_recent_pheromone = None
                self.drop_pheromone()

    def check_vision_collision(self, pheromone_group):
        # Clear strongest recent pheromone once an ants get close
        if self.strongest_recent_pheromone is not None:
            pheromone_distance = ((self.rect.centerx - self.strongest_recent_pheromone.rect.centerx) ** 2 + (self.rect.centery - self.strongest_recent_pheromone.rect.centery) ** 2) ** 0.5
            if pheromone_distance <= 5: # adjust this value to change the distance threshold
                self.strongest_recent_pheromone = None

        pheromone_collisions = pygame.sprite.spritecollide(self.pheromone_sense_sprite, pheromone_group, False)
        for pheromone_collision in pheromone_collisions:
            if pheromone_collision is not None:
                print(pheromone_collision.type)
                if self.strongest_recent_pheromone is None:
                    if self.pheromone_type != pheromone_collision.type and pheromone_collision.type != None:
                        self.strongest_recent_pheromone = pheromone_collision
    
                elif self.pheromone_type != pheromone_collision.type and pheromone_collision.type != None:
                    if self.strongest_recent_pheromone.age < pheromone_collision.age:
                        if self.has_food:
                                self.strongest_recent_pheromone = pheromone_collision
                        else:
                            if pheromone_collision.type == "food":
                                self.strongest_recent_pheromone = pheromone_collision

    
    def checkIfPheromoneReached(self):
        if self.strongest_recent_pheromone is not None:
            pheromone_distance = ((self.rect.centerx - self.strongest_recent_pheromone.rect.centerx) ** 2 + (self.rect.centery - self.strongest_recent_pheromone.rect.centery) ** 2) ** 0.5
            if pheromone_distance <= 15: # adjust this value to change the distance threshold
                self.strongest_recent_pheromone = None
