import pygame

import Settings

FPS = int(Settings.read()["FPS"])

clock = pygame.time.Clock()

class Player():
    def __init__(self, screen, pos_init):
        self.velocity = 7
        self.pos_x = pos_init[0]
        self.pos_y = pos_init[1]
        self.sprite = pygame.Surface((50,50))
        self.sprite.fill((255,255,255))
        self.rect = self.sprite.get_rect()
        self.jump_ability = False
        self.jump_velocity = 0
        self.is_jumping = False
        self.screen = screen
        self.ability_to_move_right = True
        self.ability_to_move_left = True
        self.on_floor = False


    def move(self, keys, platforms):    #La methode move ne boucle pas, elle est appelee dans une boucle

        self.rect.topleft = (self.pos_x, self.pos_y)    #A chaque iteration, on deplace la zone de collision du joueur

        """
        on teste les collisions
        si collision => 
            on tp pour que ce soit clean                    j'aurais bien ajoute la velocite aux conditions mais apres ca fait un ecart c'est moche
        sinon =>
            on fait bouger le joueur
        """

        self.on_floor = False
        for platform in platforms:
            for i in range(0,self.sprite.get_width()):
                if platform.rect.collidepoint(self.pos_x + i, self.pos_y+self.sprite.get_height()) and not self.is_jumping:
                    self.on_floor = True
                    self.jump_ability = True
                    self.jump_velocity = 0
                    self.pos_y -= abs(platform.pos_y - (self.pos_y + self.sprite.get_height()))


        if keys[pygame.K_d]:
            self.ability_to_move_right = True   #Permet de reset le droit de se deplacer vers la droite, notamment suite a une chute lorsqu'on s'est pris un obstacle volant
            self.ability_to_move_left = True #Si on se deplace vers la droite, par defaut on doit pouvoir se deplacer vers la gauche apres
            for platform in platforms:      #On isole chaque plateforme pour en tester les collisions avec l'objet Player
                for i in range (1,self.sprite.get_height()):
                    if platform.rect.collidepoint(self.pos_x + self.sprite.get_width(), self.pos_y + i):   #On teste les collisions pour la ligne de droite du rect
                        self.ability_to_move_right = False      #Si il est colle, il peut plus bouger, il suffit d'une seule plateforme
                        self.pos_x -= abs(self.pos_x + self.sprite.get_width() - platform.pos_x)    #On tp le joueur de sorte qu'il traverse pas la plateforme
            if self.ability_to_move_right == True :
                self.pos_x += self.velocity

        if keys[pygame.K_q]:
            self.ability_to_move_left = True
            self.ability_to_move_right = True
            for platform in platforms:
                for i in range (1,self.sprite.get_height()):
                    if platform.rect.collidepoint(self.pos_x -1, self.pos_y + i):
                        self.pos_x += abs(self.pos_x - (platform.pos_x + platform.width))
                        self.ability_to_move_left = False

            if self.ability_to_move_left == True :
                self.pos_x -= self.velocity

        if keys[pygame.K_SPACE] or self.is_jumping:     #permet de sauter, on verifie si le player est deha en train de sauter afin de continuer ce saut
            if not self.is_jumping and self.jump_ability == True:   #Si il n'est pas en train de sauter, alors on initialise le saut
                self.jump_velocity = 10
            self.jump()

        if not self.on_floor and not self.is_jumping:
            if self.jump_velocity < 10:
                self.jump_velocity += 0.2
            self.pos_y += self.jump_velocity

    def jump(self):
        if self.jump_ability or self.is_jumping:
            if self.jump_velocity > 0:

                self.is_jumping = True
                self.jump_ability = False

                self.jump_velocity -= 0.2
                self.pos_y -= self.jump_velocity

                pygame.draw.rect(self.screen, (0,0,0), self.rect)
                self.screen.blit(self.sprite, (self.pos_x, self.pos_y))
                self.rect.topleft = (self.pos_x, self.pos_y)
                pygame.display.update(self.rect)
            else:
                self.is_jumping = False

class Ennemy():
    def __init__(self, damage, pos):
        self.pos = pos
        self.damage = damage
        self.sprite = pygame.Surface((10,10))
        self.sprite.fill((255,0,0))
        self.rect = self.sprite.get_rect()
        self.rect.topleft = pos
        self.is_alive = True

    def harm(self, player):
        player.life -= self.damage

    def is_killed(self, player):
        for i in range (0, player.sprite.get_width()):
            if self.rect.collidepoint(player.pos_x + i, player.pos_y + player.sprite.get_height()) and player.is_jumping == False:
                self.is_alive = False
                player.jump_ability = True
                player.jump()
            