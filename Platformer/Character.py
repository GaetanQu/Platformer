from math import *
import pygame

import Settings

FPS = int(Settings.read()["FPS"])

clock = pygame.time.Clock()

class Player():
    def __init__(self, screen, pos_init):

        self.screen = screen

        self.x_velocity = 5
        self.y_velocity = 0
        self.pos_x = pos_init[0]
        self.pos_y = pos_init[1]

        self.orientation = "right"

        self.original_sprite = pygame.image.load("img/player.png")
        self.sprite = self.original_sprite
        self.original_sprite = pygame.transform.scale(self.original_sprite,(self.original_sprite.get_width()*3, self.original_sprite.get_height()*3))
        self.rect = self.original_sprite.get_rect()

        self.jump_ability = False
        self.is_jumping = False
        
        self.colliding_left = False
        self.colliding_right = False
        self.colliding_top = False
        self.colliding_bottom = False

        self.ability_to_move_right = True
        self.ability_to_move_left = True

        self.is_hooked = False
        self.rope_length = 0
        self.grappling_velocity = 0
        
    def collisions(self, platforms):
        self.rect.topleft = (self.pos_x, self.pos_y)    #A chaque iteration, on deplace la zone de collision du joueur

        self.colliding_left = False
        self.colliding_right = False
        self.colliding_top = False
        self.colliding_bottom = False

        for platform in platforms:
            for i in range (self.x_velocity,self.sprite.get_width()-self.x_velocity):
                if platform.rect.collidepoint(self.pos_x + i, self.pos_y + self.sprite.get_height()):
                    self.colliding_bottom = True
                    self.is_jumping = False
                    self.jump_ability = True
                    self.pos_y = platform.pos_y - self.sprite.get_height()
                    self.y_velocity = 0

                if platform.rect.collidepoint(self.pos_x + i, self.pos_y):
                    self.colliding_top = True
                    self.jump_ability = False
                    self.y_velocity = 0
                    self.pos_y = platform.pos_y + platform.Surface.get_height() +10

            for i in range (int(self.sprite.get_height() - self.x_velocity)):
                if platform.rect.collidepoint(self.pos_x + self.sprite.get_width(), self.pos_y +i):
                    self.colliding_right = True
                    self.pos_x = platform.pos_x - self.sprite.get_width() + 1

                if platform.rect.collidepoint(self.pos_x, self.pos_y + i):
                    self.colliding_left = True
                    self.pos_x = platform.pos_x+platform.width - 1

        if not self.colliding_bottom:
            self.jump_ability = False

    def sprite_animation(self):
        if self.orientation == "left":
            self.sprite = pygame.transform.flip(self.original_sprite, True, False)
        else:
            self.sprite = self.original_sprite

    def move(self, keys, platforms):    #La methode move ne boucle pas, elle est appelee dans une boucle
        self.gravity(platforms)
        self.collisions(platforms)

        if keys[pygame.K_d]:
            self.orientation = "right"
            avancer = True
            pos_x = self.pos_x
            for i in range (int(self.x_velocity)):
                self.pos_x += 1
                self.collisions(platforms)
                if self.colliding_right :
                    avancer = False
            self.pos_x = pos_x
            if avancer:
                self.pos_x += self.x_velocity

        if keys[pygame.K_q]:
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

        if keys[pygame.K_SPACE] and self.colliding_bottom or self.is_jumping:     #On verifie si le joueur veut sauter ou est deja en train de sauter
            self.pos_y -= 2
            self.jump()

    #La fonction de saut sera appelee en boucle jusqu'a ce que le Player aie atteint le point haut de son saut
    def jump(self):
        if self.jump_ability and not self.colliding_top:
            
            if self.is_jumping:
                self.pos_y += self.y_velocity                           #On augmente la hauteur du sprite de la vitesse, sachant que la vitesse depend de la gravite

            if not self.is_jumping :
                self.is_jumping = True
                self.y_velocity = -7

            pygame.draw.rect(self.screen, (0,0,0), self.rect)
            self.screen.blit(self.sprite, (self.pos_x, self.pos_y))
            self.rect.topleft = (self.pos_x, self.pos_y)
            pygame.display.update(self.rect)


    def grappling(self, hook_pos, platforms):
        pass

    def norm(self, posA, posB):
        return sqrt((posB[0] - posA[0])**2 + (posB[1] - posA[1])**2)

    def gravity(self, platforms):
        if not self.colliding_bottom:       #Si il n'y a pas de collision avec le dessous du sprite //bug pour les petites plateformes
            if self.y_velocity < 10 :       #Si la vitesse est inferieure a 9px/frame
                for i in range (int(self.y_velocity)):
                    self.pos_y += 1
                    self.collisions(platforms)
                self.y_velocity += 0.2      #On ajoute 0.2 = la vitesse
            self.pos_y += self.y_velocity   #On fait descendre le sprite de la valeur de la vitesse

class Ennemy():
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
        for i in range (player.sprite.get_width()):
            if self.rect.collidepoint(player.pos_x + i, player.pos_y + player.sprite.get_height()):
                self.is_alive = False
                player.pos_y -= player.y_velocity 
                player.jump_ability = True
                player.is_jumping = False
                player.jump()
            