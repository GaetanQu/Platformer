import pygame
import Character
import Settings
import Level.Generator

settings_list = Settings.read()

clock = pygame.time.Clock()

def Play(screen):
    player = Character.Player(screen,(0,0))
    ennemy = Character.Ennemy(1,(1000, 1040))
    enemies = [ennemy]
    running = True
    while running:
        clock.tick(int(settings_list["FPS"]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0,0,0))
        platforms = Level.Generator.launch(screen)

        keys = pygame.key.get_pressed()

        player.move(keys, platforms)
        screen.blit(player.sprite, (player.pos_x, player.pos_y))

        for enemy in enemies:
            if not enemy.is_alive:
                enemies.remove(enemy)
            else:
                screen.blit(enemy.sprite, (1000, 1040))
                enemy.is_killed(player)
        
        
        pygame.display.flip()
