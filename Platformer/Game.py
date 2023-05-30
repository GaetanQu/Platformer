import pygame
import Character    #Contient les classes Player et Enemy
import Settings     #.read() donnera les parametres, .write() permettra de les changer
import Level.Generator  #Va sans doute disparaitre au profit d'un truc mieux

settings_list = Settings.read()     #Permettra de recuperer les differents parametres du jeu

clock = pygame.time.Clock()         #Initialise l'horloge, necessaire pour limiter le framerate

def Play(screen):                               #Contient le jeu
    player = Character.Player(screen,(0,0))     #On cree un objet Player controlable par l'utilisateur
    enemy = Character.Enemy(1,(100, 1040))      #Voue a disparaitre, permet le debug, cree un ennemi
    enemy_bis = Character.Enemy(1, (1920/2 + 100, 700))
    enemies = [enemy, enemy_bis]                           #On met les ennemis dans une liste pour pouvoir les faire disparaitre car pygame ne peut pas detruire un objet
    
    running = True                                  #On veut que le jeu se lance quand meme
    while running:
        clock.tick(int(settings_list["FPS"]))       #La fameuse limite de FPS

        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()             #Permet de recuperer les touches du clavier qui sont pressees
        mouse_buttons = pygame.mouse.get_pressed()  #Permet de recuperer les boutons de la souris qui sont presses
        
        screen.fill((0,0,0))    #Voue a disparaitre au profit d'un vrai affichage

        platforms = Level.Generator.launch(screen)  #Idem

        for enemy in enemies:                           #Va lire la liste des ennemis
            if not enemy.is_alive:                      #Teste si l'ennemi en lecture est en vie
                enemies.remove(enemy)                   #Le retire de la liste si ce n'est pas le cas
            else:
                screen.blit(enemy.sprite, enemy.pos)    #Autrement on l'affiche
                enemy.is_killed(player)                 #Et on verifie si il meurt
        for platform in platforms:                                                          #Permet l'utilisation du grappin, pas fonctionnel
            if platform.rect.collidepoint(pygame.mouse.get_pos()) and mouse_buttons[0]:
                player.is_jumping = False
                player.grappling(pygame.mouse.get_pos(), platforms)
            elif not mouse_buttons[0]:
                player.is_hooked = False
        
        screen.blit(player.sprite, (player.pos_x, player.pos_y))    #Gere tout l'affichage, voue a disparaitre au profit d'un truc plus propre
        player.move(keys, platforms)
        player.sprite_animation()
        platforms = Level.Generator.launch(screen)
        pygame.display.flip()
