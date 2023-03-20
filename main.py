import pygame
from Classes.Ant import Ant

# Initialize pygame
pygame.init()

# Set up the display
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))

# Create an ant sprite and add it to a sprite group
ants = []
i = 0
while(i < 500):
    ants.append(Ant((255, 0, 0), 0, 0, 10, 10, screen))
    i += 1
ants.append(Ant((0, 255, 0), 0, 0, 10, 10, screen))
ant_group = pygame.sprite.Group(ants)

# Set up the clock
clock = pygame.time.Clock()
FPS = 30

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Update the ants
    ant_group.update()
    ant_group.draw(screen)

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(FPS)

# Clean up pygame
pygame.quit()
