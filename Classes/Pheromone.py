import pygame


class Pheromone(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = pygame.Surface((10, 10))
        self.color = self.get_color()
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.type = type
        self.intensity = 1
        self.lifespan = 3
        self.age = 0

    def update(self):
        self.age += 1
        if self.age == self.lifespan:
            self.intensity -= 0.02
            self.age = 0
            originalColor = self.get_color()
            self.color = (originalColor[0] * self.intensity, originalColor[1]
                          * self.intensity, originalColor[2] * self.intensity)
            if self.intensity <= 0.1:
                return self.kill()

    def get_color(self):
        if self.type == "food":
            return (200, 0, 0)  # red color for food pheromone
        elif self.type == "home":
            return (0, 50, 0)  # green color for home pheromone
        else:
            # default color for other types of pheromones
            return (150, 150, 150)


    def draw(self, screen):
        screen_width, screen_height = screen.get_size()
        x, y = int(self.rect.centerx), int(self.rect.centery)
        radius = 1
        if x < radius:
            x = radius
        elif x > screen_width - radius:
            x = screen_width - radius
        if y < radius:
            y = radius
        elif y > screen_height - radius:
            y = screen_height - radius
        
        pygame.draw.circle(screen, self.color, (x, y), radius)
