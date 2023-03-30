import pygame
import random
from Classes.Colony import Colony
from Classes.Ant import Ant
from Classes.Food import Food
from Classes.Pheromone import Pheromone

# Initialize pygame
pygame.init()

# Set up the display
screen_width, screen_height = 400, 300
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up colors
GREEN = (0, 255, 0)
PURPLE = (112, 30, 82)
BLACK = (0, 0, 0)

# Set up sprite groups
all_sprite_group = pygame.sprite.Group()
ant_sprite_group = pygame.sprite.Group()
food_sprite_group = pygame.sprite.Group()
colony_sprite_group = pygame.sprite.Group()
pheromone_sprite_group = pygame.sprite.Group()

# Spawn the colony
def spawn_colony(x, y, size, color):
    colony = Colony(x, y, size, color)
    colony_sprite_group.add(pygame.sprite.Group(colony))
    all_sprite_group.add(pygame.sprite.Group(colony))

# Spawn ants
def spawn_ants(x, y, num_ants):
    ants = []
    for i in range(num_ants):
      ants.append(Ant(BLACK, x, y, 7, screen, pheromone_sprite_group))
    ant_sprite_group.add(pygame.sprite.Group(ants))
    all_sprite_group.add(pygame.sprite.Group(ants))

# Spawn food clusters
def spawn_food_cluster(x, y, size, color, num_food):
    food = []
    for i in range(num_food):
        offset_x = random.uniform(-size * 10, size * 10)
        offset_y = random.uniform(-size * 10, size * 10)
        food_x = x + offset_x
        food_y = y + offset_y
        food.append(Food(food_x, food_y, size, color))
    food_sprite_group.add(pygame.sprite.Group(food))
    all_sprite_group.add(pygame.sprite.Group(food))

# Set up the clock
clock = pygame.time.Clock()
FPS = 30

# Call spawning methods
spawn_colony(60, 60, 50, PURPLE)
spawn_food_cluster(300, 200, 5, GREEN, 100)
spawn_ants(60, 60, 20)

# Spawn some food pheromones
##pheromone_sprite_group.add(Pheromone(100, 100, "food", screen))

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((86, 60, 24))

    # Update the pheromones
    for pheromone in pheromone_sprite_group:
        pheromone.update()
        pheromone.draw()
    
    # Update the ants
    for ant in ant_sprite_group:
        ant.check_food_collision(food_sprite_group)
        ant.check_colony_collision(colony_sprite_group)
        ant.check_vision_collision(pheromone_sprite_group)
        ant.update()

    # Draw all sprites
    food_sprite_group.draw(screen)
    colony_sprite_group.draw(screen)
    for ant in ant_sprite_group:
        ant.draw()

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(FPS)

# Clean up pygame
pygame.quit()
