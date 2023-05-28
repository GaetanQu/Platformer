import pygame
from Level.Platforms import *

def launch(screen):
    platforms_list = []
    platforms_list.append(Rect_Platform(screen, (screen.get_width(), 10), (0,screen.get_height() - 10), (255,255,255)))
    platforms_list.append(Rect_Platform(screen, (100, 10), (200, screen.get_height()-20), (255,0,0)))
    platforms_list.append(Rect_Platform(screen, (10,10), (1500, 1040), (0,0,255)))

    return platforms_list