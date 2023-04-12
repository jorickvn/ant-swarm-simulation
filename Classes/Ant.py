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

        # Color
        self.WHITE = (255, 255, 255)

        # Storing globals
        self.screen = screen
        self.pheromone_group = pheromone_group
        self.food_group = food_group
        self.colony_group = colony_group
        self.grid = grid

        # Senses
        self.closest_visible_food = None
        self.closest_visible_colony = None

        # Movement and rotation
        self.speed = 3  # constant speed the ant moves at
        self.position = pygame.math.Vector2(x, y)
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * self.speed
        self.acceleration = pygame.math.Vector2(0, 0)
        self.turn_rate = math.pi * 2

        # Pheromones
        self.pheromone_type = "home"  # the type of pheromone this ant will drop
        self.pheromoneDropInterval = 5
        self.ticksSincePheromoneDropped = random.randint(0, self.pheromoneDropInterval-1)
        self.strongest_recent_pheromone = None

        # Food
        self.has_food = False

        # Senses
        self.vision_sprite = pygame.sprite.Sprite()
        self.vision_sprite.rect = pygame.Rect(self.rect.x, self.rect.y, 75, 75)

        self.left_vision_sprite = pygame.sprite.Sprite()
        self.left_vision_sprite.rect = pygame.Rect(self.rect.x + 20, self.rect.y - 40, 33, 33)

        self.center_vision_sprite = pygame.sprite.Sprite()
        self.center_vision_sprite.rect = pygame.Rect(self.rect.x + 33, self.rect.y, 33, 33)

        self.right_vision_sprite = pygame.sprite.Sprite()
        self.right_vision_sprite.rect = pygame.Rect(self.rect.x + 33, self.rect.y - 33, 33, 33)

    def setDestination(self, x, y):
        self.destination = pygame.math.Vector2(x, y)

    def turn_left(self):
        self.velocity.rotate_ip(-self.turn_rate)

    def turn_right(self):
        self.velocity.rotate_ip(self.turn_rate)

    def turn_around(self):
        self.velocity.rotate_ip(180)

    def turn_to_destination(self):
        destination = None

        if not self.has_food:
            if self.closest_visible_food is not None:
                destination = (self.closest_visible_food.rect.x, self.closest_visible_food.rect.y)

        if self.has_food:
            if self.closest_visible_colony is not None:
                destination = (self.closest_visible_colony.rect.x, self.closest_visible_colony.rect.y)

        if destination is None:
            # Follow strongest pheromone trail
            destination = self.get_coordinates_to_highest_intensity_pheromone()

        if destination is None:
            # Randomly wander around
            self.velocity.rotate_ip(random.uniform(-self.turn_rate, self.turn_rate))
            return

        desired_direction = (destination[0], destination[1]) - self.position
        desired_direction = desired_direction.normalize()
        angle_diff = math.atan2(desired_direction.y, desired_direction.x) - math.atan2(self.velocity.y, self.velocity.x)
        if angle_diff > 0:
            self.turn_right()
        elif angle_diff < 0:
            self.turn_left()

    def move(self):
        # Update position and velocity
        self.velocity = self.velocity.normalize() * self.speed
        new_position = self.position + self.velocity
        self.position = new_position

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

        # Drop pheromone if appropriate
        self.ticksSincePheromoneDropped += 1
        if self.ticksSincePheromoneDropped == self.pheromoneDropInterval:
            self.ticksSincePheromoneDropped = 0
            self.drop_pheromone()

        # Update the position of the ant's rect
        self.image = pygame.transform.rotate(self.original_image, -self.velocity.as_polar()[1])
        self.rect = self.image.get_rect(center=self.position)

        # Update the position of the vision sprite rects
        left_vision_offset = pygame.math.Vector2(33, -40).rotate(-self.velocity.as_polar()[1])
        center_vision_offset = pygame.math.Vector2(45, 0).rotate(-self.velocity.as_polar()[1])
        right_vision_offset = pygame.math.Vector2(33, 40).rotate(-self.velocity.as_polar()[1])
        self.left_vision_sprite.rect.center = self.rect.center + left_vision_offset
        self.center_vision_sprite.rect.center = self.rect.center + center_vision_offset
        self.right_vision_sprite.rect.center = self.rect.center + right_vision_offset
    
    def draw(self, screen):
        # draw self
        pygame.draw.rect(screen, self.color, self.rect)

        pygame.draw.rect(screen, self.WHITE, self.left_vision_sprite.rect)
        pygame.draw.rect(screen, self.WHITE, self.center_vision_sprite.rect)
        pygame.draw.rect(screen, self.WHITE, self.right_vision_sprite.rect)


    def update(self):
        self.check_collisions()
        self.check_vision()
        self.turn_to_destination()
        self.move()

    def check_collisions(self):
        self.check_food_collision()
        self.check_colony_collision()

    def check_vision(self):
        # Update pheromone sprite position
        self.vision_sprite.rect.center = self.position

        food_collisions = pygame.sprite.spritecollide(self.vision_sprite, self.food_group, False)
        if food_collisions:
            for food in food_collisions:
                if(self.closest_visible_food == None):
                    self.closest_visible_food = food
                else:
                    if (self.calculate_distance_to_other(food.rect) < self.calculate_distance_to_other(self.closest_visible_food.rect)):
                        self.closest_visible_food = food
        else:
            self.closest_visible_food = None

        colony_collisions = pygame.sprite.spritecollide(self.vision_sprite, self.colony_group, False)
        if colony_collisions:
            for colony in colony_collisions:
                if(self.closest_visible_colony == None):
                    self.closest_visible_colony = colony
                else:
                    if (self.calculate_distance_to_other(colony.rect) < self.calculate_distance_to_other(self.closest_visible_colony.rect)):
                        self.closest_visible_colony = colony
        else:
            self.closest_visible_colony = None

    def check_food_collision(self):
        food_collision = pygame.sprite.spritecollideany(self, self.food_group)
        if food_collision:
            if self.has_food == False:
                self.has_food = True
                self.pheromone_type = "food"
                self.strongest_recent_pheromone = None
                food_collision.kill()
                self.turn_around()

    def check_colony_collision(self):
        colony_collision = pygame.sprite.spritecollideany(self, self.colony_group)
        if colony_collision:
            if self.has_food == True:
                self.has_food = False
                colony_collision.spawn_ant()
                self.pheromone_type = "home"
                self.strongest_recent_pheromone = None
                self.turn_around()

    def drop_pheromone(self):
        if self.pheromone_type != None:
            pheromone = Pheromone(self.rect.x, self.rect.y, self.pheromone_type)
            self.pheromone_group.add(pygame.sprite.Group(pheromone))
            self.grid.add_pheromone(self.rect.x, self.rect.y, pheromone)

    def calculate_distance_to_other(self, other):
        return math.sqrt((self.rect.x - other.x)**2 + (self.rect.y - other.y)**2)
    
    def get_coordinates_to_highest_intensity_pheromone(self):
        destination = None
        if self.has_food == False:
            food_pheromones = self.grid.get_highest_intensity_cell(self.rect.x, self.rect.y, 'food')
            if food_pheromones:
                total_intensity = sum(pheromone.intensity for pheromone in food_pheromones)
                weighted_average_x = sum(pheromone.rect.x * pheromone.intensity for pheromone in food_pheromones) / total_intensity
                weighted_average_y = sum(pheromone.rect.y * pheromone.intensity for pheromone in food_pheromones) / total_intensity
                destination = (weighted_average_x, weighted_average_y)
        else:
            home_pheromones = self.grid.get_highest_intensity_cell(self.rect.x, self.rect.y, 'home')
            if home_pheromones:
                total_intensity = sum(pheromone.intensity for pheromone in home_pheromones)
                weighted_average_x = sum(pheromone.rect.x * pheromone.intensity for pheromone in home_pheromones) / total_intensity
                weighted_average_y = sum(pheromone.rect.y * pheromone.intensity for pheromone in home_pheromones) / total_intensity
                destination = (weighted_average_x, weighted_average_y)

        return destination