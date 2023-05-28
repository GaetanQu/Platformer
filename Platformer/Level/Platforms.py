import pygame

class Rect_Platform():
    def __init__(self,screen, size, pos, color):
        self.Surface = pygame.Surface(size)
        self.Surface.fill(color)
        self.rect = self.Surface.get_rect()
        self.rect.topleft = pos
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.width = size[0]
        self.height = size[1]

        screen.blit(self.Surface, pos)
