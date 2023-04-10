import pygame
import math
import random
from Classes.Pheromone import Pheromone
from Classes.Grid import Grid


class Ant(pygame.sprite.Sprite):
    def __init__(self, color, x, y, size, screen, pheromone_group, food_group, colony_group, grid):

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
        self.grid = grid

        # Movement and rotation
        self.speed = 3  # constant speed the ant moves at
        self.position = pygame.math.Vector2(x, y)
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * self.speed
        self.acceleration = pygame.math.Vector2(0, 0)
        self.max_turn_angle = math.pi  # maximum angle the ant can turn per update
        self.destination = None

        # Pheromones
        self.pheromone_type = "home"  # the type of pheromone this ant will drop
        self.pheromoneDropInterval = 15
        self.ticksSincePheromoneDropped = random.randint(0, self.pheromoneDropInterval-1)
        self.strongest_recent_pheromone = None

        # Food
        self.has_food = False

        # Senses
        self.pheromone_sense_sprite = pygame.sprite.Sprite()
        self.pheromone_sense_sprite.rect = pygame.Rect(self.rect.x, self.rect.y, 250, 250)

    def setDestination(self, x, y):
        self.destination = pygame.math.Vector2(x, y)

    def turnToDestination(self):
        if self.destination is None:
            self.velocity.rotate_ip(random.uniform(-self.max_turn_angle / 18, self.max_turn_angle / 18))
        else:
            desired_direction = self.destination - self.position
            if desired_direction.length() > 0:
                desired_direction = desired_direction.normalize()
                angle_diff = math.degrees(math.atan2(desired_direction.y, desired_direction.x) - math.atan2(self.velocity.y, self.velocity.x))
                angle_diff = max(-self.max_turn_angle, min(self.max_turn_angle, angle_diff))
                self.velocity.rotate_ip(angle_diff)
    
            self.image = pygame.transform.rotate(self.original_image, -self.velocity.as_polar()[1])
            self.rect = self.image.get_rect(center=self.position)
    
    def move(self):
        # Update position and velocity
        self.velocity = self.velocity.normalize() * self.speed
        new_position = self.position + self.velocity
        self.position = new_position
        self.rect.center = self.position

        # Reflect off screen boundaries
        if self.position.x < 0:
            self.position.x = abs(self.position.x)
            self.velocity.x *= -1
        elif self.position.x > self.screen.get_width():
            self.position.x = 2 * self.screen.get_width() - self.position.x
            self.velocity.x *= -1

        if self.position.y < 0:
            self.position.y = abs(self.position.y)
            self.velocity.y *= -1
        elif self.position.y > self.screen.get_height():
            self.position.y = 2 * self.screen.get_height() - self.position.y
            self.velocity.y *= -1

        # Update pheromone sprite position
        self.pheromone_sense_sprite.rect.center = self.position

        # Drop pheromone if appropriate
        self.ticksSincePheromoneDropped += 1
        if self.ticksSincePheromoneDropped == self.pheromoneDropInterval:
            self.ticksSincePheromoneDropped = 0
            self.drop_pheromone()
    
    def draw(self, screen):
        # draw self
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        self.check_highest_intensity_pheromone_cell()
        self.check_vision_collision()
        self.turnToDestination()
        self.move()

    def drop_pheromone(self):
        if self.pheromone_type != None:
            pheromone = Pheromone(self.rect.x, self.rect.y, self.pheromone_type)
            self.pheromone_group.add(pygame.sprite.Group(pheromone))
            self.grid.add_pheromone(self.rect.x, self.rect.y, pheromone)

    def check_food_collision(self, food_group):
        food_collision = pygame.sprite.spritecollideany(self, food_group)
        if food_collision:
            if self.has_food == False:
                self.has_food = True
                self.pheromone_type = "food"
                self.strongest_recent_pheromone = None
                food_collision.kill()

    def check_colony_collision(self, colony_group):
        colony_collision = pygame.sprite.spritecollideany(self, colony_group)
        if colony_collision:
            if self.has_food == True:
                self.has_food = False
                colony_collision.spawn_ant()
                self.pheromone_type = "home"
                self.strongest_recent_pheromone = None

    def check_vision_collision(self):
        if self.has_food == False:
            food_collisions = pygame.sprite.spritecollide(self.pheromone_sense_sprite, self.food_group, False)
            if food_collisions:
                self.setDestination(food_collisions[0].rect.x, food_collisions[0].rect.y)

        if self.has_food == True:
            colony_collisions = pygame.sprite.spritecollide(self.pheromone_sense_sprite, self.colony_group, False)
            if colony_collisions:
                self.setDestination(colony_collisions[0].rect.x, colony_collisions[0].rect.y)

    def check_highest_intensity_pheromone_cell(self):
        if self.has_food == False:
            destination = self.grid.get_highest_intensity_pheromone_cell_coordinates(self.rect.x, self.rect.y, 'food')
        else:
            destination = self.grid.get_highest_intensity_pheromone_cell_coordinates(self.rect.x, self.rect.y, 'home')

        if(destination == None):
            return
        
        self.setDestination(destination[0],destination[1])
