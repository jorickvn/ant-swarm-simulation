import pygame

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([size, size])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.size = size
        self.color = color

    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, self.size)