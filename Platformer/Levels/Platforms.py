import pygame

class Rect_Platform():
    def __init__(self,screen, size, pos, color):
        self.Surface = pygame.Surface(size)
        self.Surface.fill(color)
        self.rect = self.Surface.get_rect()
        self.rect.topleft = pos

        screen.blit(self.Surface, pos)
