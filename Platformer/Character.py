from math import *
import pygame
from Maths import *

import Settings

FPS = int(Settings.read()["FPS"])

clock = pygame.time.Clock()

class Player():
    def __init__(self, screen, pos_init):

        self.screen = screen    #Permet de recuperer la fenetre sans devoir l'appeler constamment

        self.x_velocity = 5     #On definit les vitesses x et y par defaut 
        self.y_velocity = 0
        self.pos_x = pos_init[0]    #On definit les positions initiales par defaut, sachant que dans la definition du joueur, ses coordonnees seront un tuple
        self.pos_y = pos_init[1]

        self.orientation = "right"  #L'orientation de depart, fixe, qui permettra de changer l'orientation correctement en fonction des deplacements

        self.original_sprite = pygame.image.load("img/player.png")  #Definition du sprite du joueur, voue a changer
        self.original_sprite = pygame.transform.scale(self.original_sprite,(self.original_sprite.get_width()*3, self.original_sprite.get_height()*3))
        
        self.sprite = self.original_sprite                  #Le sprite qui sera voue a changer d'orientation en fonction de la direction
        self.rect = self.original_sprite.get_rect()         #Sa zone de collisions
        self.width, self.height = self.sprite.get_size()    #On recupere ses dimensions UNE SEULE FOIS (plus opti)

        self.jump_ability = False   #Par defaut, le joueur etant en l'air, il ne doit pas pouvoir sauter, peut changer
        self.is_jumping = False     #Idem
        self.jump_intensity = -7    #Set l'intensite des sauts, on pourra la faire evoluer par la suite si on pousse le truc plus loin
        
        self.colliding_left = False     #On set les collisions sur False parce qu'il leur faut un etat de depart
        self.colliding_right = False
        self.colliding_top = False
        self.colliding_bottom = False

        self.ability_to_move_right = True   #dependra des collisions
        self.ability_to_move_left = True

        self.is_hooked = False      #Grappin (non operationnel)
        self.rope_length = 0
        self.grappling_velocity = 0
        
    def collisions(self, platforms):
        self.rect.topleft = (self.pos_x, self.pos_y)    #A chaque iteration, on deplace la zone de collision du joueur

        self.colliding_left = False     #On reset les collisions sur False
        self.colliding_right = False    #Elles sont calculees a chaque frame
        self.colliding_top = False
        self.colliding_bottom = False

        #Les tests de collisions etaient une usine a bugs, notamment pour les petites plateformes, donc j'ai un peu galere a faire ca, mais ca marche

        for platform in platforms:                                                          #On va tester les collisions sur chaque plateforme
            for i in range (self.x_velocity,self.width-self.x_velocity):                    #Je soustrais la vitesse horizontale a la zone de test afin d'eviter des tp malencontreux
                if platform.rect.collidepoint(self.pos_x + i, self.pos_y + self.height):    #Test des collisions entre la plateforme en lecture et la ligne du bas du Player
                    self.colliding_bottom = True                                            #On set le colliding si il y a au moins une collision avec au moins une plateforme
                    self.is_jumping = False                                                 #Si il est sur une plateforme, c'est qu'il saute pas
                    self.jump_ability = True
                    self.pos_y = platform.pos_y - self.height                               #Permet d'eviter des bugs graphiques moches
                    self.y_velocity = 0                                                     #Si il est pose, alors sa vitesse verticale est nulle, permet d'eviter que le saut reprenne lorsqu'on quitte une plateforme

                if platform.rect.collidepoint(self.pos_x + i, self.pos_y):              #idem pour les collisions avec la partie haute du sprite
                    self.colliding_top = True                                           #On set le collider
                    self.jump_ability = False                                           #Si il tape, alors il ne saute pas
                    self.y_velocity = 0                                                 #Et on set sa vitesse en y a 0
                    self.pos_y = platform.pos_y + platform.Surface.get_height() +10     #Rustine permettant d'eviter les bugs

            for i in range (int(self.height - self.x_velocity)):                            #Cette fois on boucle les hauteurs pour tester les collisions laterales
                if platform.rect.collidepoint(self.pos_x + self.width, self.pos_y +i):      #On teste les collisions a droite
                    self.colliding_right = True
                    self.pos_x = platform.pos_x - self.width + 1                            #Le +1 est une rustine

                if platform.rect.collidepoint(self.pos_x, self.pos_y + i):                  #On teste les collisions a gauche
                    self.colliding_left = True  
                    self.pos_x = platform.pos_x+platform.width - 1                          #idem, rustine

        if not self.colliding_bottom:
            self.jump_ability = False   #Si le player est dans les airs, alors il ne peut pas sauter

    def sprite_animation(self):     #Oriente et anime le sprite du joueur en fonction de ses deplacements
        if self.orientation == "left":
            self.sprite = pygame.transform.flip(self.original_sprite, True, False)
        elif self.orientation == "right":
            self.sprite = self.original_sprite

    def move(self, keys, platforms):    #La methode move ne boucle pas, elle est appelee dans une boucle
        self.gravity(platforms)         #On commence par appliquer la gravite (fonction definie plus bas)
        self.collisions(platforms)      #Puis on applique les collisions, attention a bien respecter cet ordre

        if keys[pygame.K_d]:                        #L'utilisateur appuie sur D pour se deplacer a droite
            self.orientation = "right"
            avancer = True                          #Set une variable "avancer" permet de regler les problemes de collision
            pos_x = self.pos_x                      #idem pour la variable pos_x, qui permet de stocker self.pos_x le temps des collisions precises
            for i in range (int(self.x_velocity)):
                self.pos_x += 1
                self.collisions(platforms)
                if self.colliding_right :
                    avancer = False
            self.pos_x = pos_x
            if avancer:
                self.pos_x += self.x_velocity

        if keys[pygame.K_q]:                            #idem a gauche
            self.orientation = "left"
            avancer = True
            pos_x = self.pos_x
            for i in range(int(self.x_velocity)):
                self.pos_x-=1
                self.collisions(platforms)
                if self.colliding_left:
                    avancer = False
            self.pos_x = pos_x
            if avancer == True:
                self.pos_x -= self.x_velocity

        if keys[pygame.K_SPACE] and self.colliding_bottom or self.is_jumping:     #On verifie si le joueur veut et peut sauter ou est deja en train de sauter
            self.pos_y -= 2     #rustine permettant d'eviter les bugs
            self.jump()         #execution du saut

    def jump(self):
        if self.jump_ability:                #On ne saute que si on peut sauter
            
            if self.is_jumping:                     #On teste si le joueur est deja en saut, auquel cas
                self.pos_y += self.y_velocity       #On augmente la hauteur du sprite de la vitesse, sachant que la vitesse depend de la gravite

            if not self.is_jumping :                #Si le joueur n'est pas deja en train de sauter
                self.is_jumping = True              #Alors on initialise le saut
                self.y_velocity = self.jump_intensity

            pygame.draw.rect(self.screen, (0,0,0), self.rect)               #Voue a disparaitre, permet l'affichage des sprites
            self.screen.blit(self.sprite, (self.pos_x, self.pos_y))
            self.rect.topleft = (self.pos_x, self.pos_y)
            pygame.display.update(self.rect)

        if not pygame.key.get_pressed()[pygame.K_SPACE]:    #On arrete le saut si la touche espace est lachee
            self.jump_ability = False
            self.is_jumping = False

    def grappling(self, hook_pos, platforms):
        pass

    def gravity(self, platforms):
        if not self.colliding_bottom:       #Si il n'y a pas de collision avec le dessous du sprite //bug pour les petites plateformes
            if self.y_velocity < 10 :       #Si la vitesse est inferieure a 9px/frame
                for i in range (int(self.y_velocity)):
                    self.pos_y += 1
                    self.collisions(platforms)
                self.y_velocity += 0.2      #On ajoute 0.2 = la vitesse
            self.pos_y += self.y_velocity   #On fait descendre le sprite de la valeur de la vitesse

class Enemy():
    def __init__(self, damage, pos):
        self.pos = pos
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.damage = damage
        self.sprite = pygame.Surface((10,10))
        self.sprite.fill((255,0,0))
        self.rect = self.sprite.get_rect()
        self.rect.topleft = pos
        self.is_alive = True

    def harm(self, player):
        player.life -= self.damage

    def is_killed(self, player):
        for i in range (player.width):
            if self.rect.collidepoint(player.pos_x + i, player.pos_y + player.height) and player.y_velocity > 0:
                self.is_alive = False
                player.y_velocity = player.jump_intensity
                player.jump()  