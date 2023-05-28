import pygame
pygame.init()
screen = pygame.display.set_mode((0,0))
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()

import Settings
setting = Settings.read()   #setting["parametre"]=valeur

import Game

def menu(screen):
    while True:
        clock.tick(int(setting["FPS"]))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            elif event.type == pygame.MOUSEBUTTONUP:
                Game.Play(screen)
menu(screen)