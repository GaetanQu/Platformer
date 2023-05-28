import pygame

import Settings

FPS = int(Settings.read()["FPS"])

clock = pygame.time.Clock()
import Levels.Creator

class Player():
    def __init__(self, screen, pos_init):
        self.life = 3
        self.money = 0
        self.damage = 1
        self.velocity = 10
        self.pos_x = pos_init[0]
        self.pos_y = pos_init[1]
        self.sprite = pygame.Surface((50,50))
        self.sprite.fill((255,255,255))
        self.rect = self.sprite.get_rect()
        self.jump_ability = False
        self.jump_velocity = 10
        self.is_jumping = False
        self.screen = screen

    def move(self, keys, platforms):

        self.rect.topleft = (self.pos_x, self.pos_y)

        if keys[pygame.K_d]:
            self.pos_x += self.velocity

        if keys[pygame.K_q]:
            self.pos_x -= self.velocity

        if keys[pygame.K_SPACE] or self.is_jumping:
            self.jump()

        gravity = True
        for platform in platforms:
            if platform.rect.collidepoint(self.pos_x + 50, self.pos_y + 50) or platform.rect.collidepoint(self.pos_x, self.pos_y + 50):
                gravity = False
                self.is_jumping = False
                self.jump_ability = True
                self.jump_velocity = 10
                
        if gravity == True and not self.is_jumping:
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
        self.sprite = pygame.Surface((30,30))
        self.sprite.fill((255,0,0))
        self.rect = self.sprite.get_rect()
        self.rect.topleft = pos
        self.is_alive = True

    def harm(self, player):
        player.life -= self.damage

    def is_killed(self, player):
        if self.rect.collidepoint(player.pos_x + 50, player.pos_y + 50) or self.rect.collidepoint(player.pos_x, player.pos_y+50):
            self.is_alive = False
            player.jump_ability = True
            player.jump()
            