import pygame
import random
from Classes.Colony import Colony
from Classes.Ant import Ant
from Classes.Food import Food
from Classes.Pheromone import Pheromone
from Classes.Grid import Grid

# Initialize pygame
pygame.init()

# Set up colors
GREEN = (0, 255, 0)
PURPLE = (112, 30, 82)
BLACK = (0, 0, 0)

# Set up the display
screen_width, screen_height = 1500, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the grid
sprite_grid = Grid(screen, 20)

# Set up sprite groups
all_sprite_group = pygame.sprite.Group()
ant_sprite_group = pygame.sprite.Group()
food_sprite_group = pygame.sprite.Group()
colony_sprite_group = pygame.sprite.Group()
pheromone_sprite_group = pygame.sprite.Group()

# Spawn the colony
def spawn_colony(x, y, size, color):
    colony = Colony(x, y, size, color, screen, ant_sprite_group, pheromone_sprite_group, food_sprite_group, colony_sprite_group, sprite_grid)
    colony_sprite_group.add(pygame.sprite.Group(colony))

# Spawn ants
def spawn_ants(x, y, num_ants):
    ants = []
    for i in range(num_ants):
      ants.append(Ant(BLACK, x, y, 7, screen, pheromone_sprite_group, food_sprite_group, colony_sprite_group, sprite_grid))
    ant_sprite_group.add(pygame.sprite.Group(ants))

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
spawn_colony(100, 100, 50, PURPLE)
spawn_food_cluster(550, 200, 5, GREEN, 120)
spawn_food_cluster(900, 150, 5, GREEN, 100)
spawn_food_cluster(1450, 550, 5, GREEN, 300)
spawn_ants(100, 100, 50)

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
    
    # Update the ants
    for ant in ant_sprite_group:
        ant.check_food_collision(food_sprite_group)
        ant.check_colony_collision(colony_sprite_group)
        ant.update()

    # Draw all sprites
    for pheromone in pheromone_sprite_group:
        pheromone.draw(screen)

    for food in food_sprite_group:
        food.draw(screen)

    for ant in ant_sprite_group:
        ant.draw(screen)

    for colony in colony_sprite_group:
        colony.draw(screen)

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(FPS)

# Clean up pygame
pygame.quit()
