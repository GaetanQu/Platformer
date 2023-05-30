import pygame                           #Le jeu tournera sous pygame, pas le plus opti, mais le seul que je maitrise
pygame.init()                           #ON N'INITIALISE QU'UNE FOIS, pas besoin de plus
screen = pygame.display.set_mode((0,0)) #IDEM POUR LE SCREEN, si on créée un nouveau screen on va avoir une fenêtre qui pop c'est moche
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()

import Settings             #Permettra de lire et de changer les parametres du jeu, stockes dans un csv, va peut-etre pas rester
setting = Settings.read()   #setting["parametre"]=valeur

import Game     #Le jeu

def menu(screen):   #Voue a disparaitre au profit d'un vrai menu, sans doute avec un authentificateur (je m'en charge)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            elif event.type == pygame.MOUSEBUTTONUP:
                Game.Play(screen)
menu(screen)