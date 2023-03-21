import pygame
import math
import random
from Classes.Pheromone import Pheromone

class Ant(pygame.sprite.Sprite):
    def __init__(self, color, x, y, size, screen, pheromone_group):

        # Drawing
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size, size * 0.66))
        self.color = color
        self.image.fill((self.color))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.screen = screen

        # Movement and rotation
        self.rect.x = x
        self.rect.y = y
        self.angle = random.uniform(0, 2*math.pi)  # starting angle is random
        self.speed = 3

        # Pheromones
        self.pheromone_group = pheromone_group
        self.ticksSincePheromoneDropped = 0
        self.pheromoneDropInterval = 2
        self.pheromone_type = "home"  # the type of pheromone this ant will drop
        self.pheromones = pygame.sprite.Group()  # list of pheromones dropped by this ant
        self.pheromone_sense_rect = pygame.Rect(self.rect.x, self.rect.y, 50, 50)
        self.strongest_recent_pheromone = None

        # Food
        self.has_food = False

    def move(self):
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
            self.pheromone_sense_rect.center = self.rect.center

        # randomly adjust angle to create irregular movement
        self.angle += random.uniform(-math.pi/8, math.pi/8)

        # rotate rectangle based on angle
        self.image = pygame.transform.rotate(self.original_image, math.degrees(-self.angle))
        self.rect = self.image.get_rect(center=self.rect.center)

        # add current position to trail if step interval has passed
        self.ticksSincePheromoneDropped += 1
        if(self.ticksSincePheromoneDropped == self.pheromoneDropInterval):
            # drop a pheromone of the current type at the current position
            self.ticksSincePheromoneDropped = 0
            if self.pheromone_type is not None:
                pheromone = Pheromone(self.rect.x, self.rect.y, self.pheromone_type)
                self.pheromones.add(pheromone)
                self.pheromone_group.add(pygame.sprite.Group(pheromone))

    def moveToPheromone(self):
      if self.strongest_recent_pheromone is not None:
          # calculate angle and distance to strongest recent pheromone
          dx = self.strongest_recent_pheromone.rect.x - self.rect.x
          dy = self.strongest_recent_pheromone.rect.y - self.rect.y
          distance = math.sqrt(dx ** 2 + dy ** 2)
          angle = math.atan2(dy, dx)

          # adjust angle to steer towards strongest recent pheromone
          angle_diff = angle - self.angle
          while angle_diff > math.pi:
              angle_diff -= 2 * math.pi
          while angle_diff < -math.pi:
              angle_diff += 2 * math.pi
          max_angle_diff = math.pi / 16
          if angle_diff > max_angle_diff:
              angle_diff = max_angle_diff
          elif angle_diff < -max_angle_diff:
              angle_diff = -max_angle_diff
          self.angle += angle_diff

          # adjust speed based on distance to strongest recent pheromone
          max_speed = 10
          if distance < max_speed:
              self.speed = distance
          else:
              self.speed = max_speed

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
          self.pheromone_sense_rect.center = self.rect.center

      # randomly adjust angle to create irregular movement
      self.angle += random.uniform(-math.pi/8, math.pi/8)

      # rotate rectangle based on angle
      self.image = pygame.transform.rotate(self.original_image, math.degrees(-self.angle))
      self.rect = self.image.get_rect(center=self.rect.center)

      # add current position to trail if step interval has passed
      self.ticksSincePheromoneDropped += 1
      if(self.ticksSincePheromoneDropped == self.pheromoneDropInterval):
          # drop a pheromone of the current type at the current position
          self.ticksSincePheromoneDropped = 0
          if self.pheromone_type is not None:
            pheromone = Pheromone(self.rect.x, self.rect.y, self.pheromone_type)
            self.pheromones.add(pheromone)
            self.pheromone_group.add(pygame.sprite.Group(pheromone))

            
    def draw(self):
        # draw self
        pygame.draw.rect(self.screen, self.color, self.rect)

        # draw cone
        self.draw_pheromone_sense()

        # draw pheromones
        for p in self.pheromones:
            p.update()
            p.draw(self.screen)

    def draw_pheromone_sense(self):
      # draw the cone using pygame's polygon function
      pygame.draw.rect(self.screen, (255, 255, 255), self.pheromone_sense_rect, 2)

    def update(self):
        self.moveToPheromone()
        self.draw()

    def check_food_collision(self, food_group):
        food_collision = pygame.sprite.spritecollideany(self, food_group)
        if food_collision:
          if self.has_food == False:
            self.has_food = True
            self.pheromone_type = "food"
            food_collision.kill()

    def check_colony_collision(self, colony_group):
        colony_collision = pygame.sprite.spritecollideany(self, colony_group)
        if colony_collision:
            if self.has_food == True:
                self.has_food = False
                self.pheromone_type = "home"
    
    def check_pheromone_collision(self, pheromone_group):
        pheromone_collision = pygame.sprite.spritecollideany(self, pheromone_group)
        if pheromone_collision:
            if self.strongest_recent_pheromone == None:
                self.strongest_recent_pheromone = pheromone_collision
            elif self.strongest_recent_pheromone.intensity <= pheromone_collision.intensity:
                if self.has_food == True:
                    if pheromone_collision.type == "home":
                      self.strongest_recent_pheromone = pheromone_collision
                else:
                    if pheromone_collision.type == "food":
                      self.strongest_recent_pheromone = pheromone_collision
