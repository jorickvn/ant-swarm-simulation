import pygame
import math
from Classes.Pheromone import Pheromone

class Grid:
    def __init__(self, screen, grid_cell_size):
        self.grid = []
        self.grid_cell_size = grid_cell_size

        # Calculating grid size
        grid_width = math.ceil(screen.get_width() / grid_cell_size)
        grid_height = math.ceil(screen.get_height() / grid_cell_size)
        print('width: ' + str(grid_width) + " height: " + str(grid_height))

        # Populating grid
        for x in range(grid_width):
            column = []
            for y in range(grid_height):
                cell = {
                    'food': pygame.sprite.Group(),
                    'colony': pygame.sprite.Group(),
                    'pheromone': pygame.sprite.Group(),
                }
                column.append(cell)
            self.grid.append(column)

    def get_cell(self, x, y):
        if(x < 0):
            x = 0
        if(y < 0):
            y = 0
        return self.grid[x][y]
    
    def is_valid_index(self, x, y):
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[x])
    
    def get_highest_intensity_pheromone_cell_coordinates(self, x, y, pheromone_type):
        x = self.convert_coordinate_to_cell_index(x)
        y = self.convert_coordinate_to_cell_index(y)
        highest_intensity_pheromone_cell_coordinates = None
        highest_recorded_intensity = 0

        for i in range(-5, 10):
            new_x = x + i
            for j in range (-5, 10):
                new_y = y +  j

                if self.is_valid_index(new_x, new_y):
                    pheromone_group = self.get_cell(new_x, new_y)['pheromone']
                    pheromone_intensity = 0

                    for pheromone in pheromone_group:
                        if pheromone.type == pheromone_type:
                            pheromone_intensity = pheromone_intensity + 1

                    if pheromone_intensity > highest_recorded_intensity:
                        x = new_x * self.grid_cell_size
                        y = new_y * self.grid_cell_size
                        highest_intensity_pheromone_cell_coordinates = [x, y]
                        highest_recorded_intensity = pheromone_intensity

        return highest_intensity_pheromone_cell_coordinates

    def add_pheromone(self, x, y, sprite):
        x = self.convert_coordinate_to_cell_index(x)
        y = self.convert_coordinate_to_cell_index(y)
        
        if self.is_valid_index(x, y):
            self.grid[x][y]['pheromone'].add(sprite)

    def add_food(self, x, y, sprite):
        x = self.convert_coordinate_to_cell_index(x)
        y = self.convert_coordinate_to_cell_index(y)
        
        if self.is_valid_index(x, y):
            self.grid[x][y]['food'].add(sprite)

    def remove_sprite_from_cell(self, x, y, sprite, sprite_type):
        if self.is_valid_index(x, y):
            self.grid[x][y][sprite_type].remove(sprite)

    def convert_coordinate_to_cell_index(self, coordinate):
        return math.floor(coordinate / self.grid_cell_size)
