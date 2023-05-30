import pygame
import Character
import Settings
import Level.Generator

settings_list = Settings.read()

clock = pygame.time.Clock()

def Play(screen):
    player = Character.Player(screen,(0,0))
    ennemy = Character.Ennemy(1,(100, 1040))
    enemies = [ennemy]
    running = True
    while running:
        clock.tick(int(settings_list["FPS"]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        screen.fill((0,0,0))

        platforms = Level.Generator.launch(screen)

        for enemy in enemies:
            if not enemy.is_alive:
                enemies.remove(enemy)
            else:
                screen.blit(enemy.sprite, enemy.pos)
                enemy.is_killed(player)
        for platform in platforms:
            if platform.rect.collidepoint(pygame.mouse.get_pos()) and mouse_buttons[0]:
                player.is_jumping = False
                player.grappling(pygame.mouse.get_pos(), platforms)
            elif not mouse_buttons[0]:
                player.is_hooked = False
        
        screen.blit(player.sprite, (player.pos_x, player.pos_y))
        player.move(keys, platforms)
        player.sprite_animation()
        platforms = Level.Generator.launch(screen)
        pygame.display.flip()
