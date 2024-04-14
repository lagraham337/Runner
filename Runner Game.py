import pygame
from sys import exit

# Docs: https://www.pygame.org/docs/
# Graphics: itch.io
# Background autumn landscale park background from macrovector on freepik.com

pygame.init()

# create display surface
# screen = pygame.display.set_mode((width, height))
screen = pygame.display.set_mode((800, 400))

# title. Could also set icon with pygame.display.set_icon('img.jpg')
pygame.display.set_caption('Runner')

# clock object helps us with time and making sure framerate is constant
clock = pygame.time.Clock()
# test_font = pygame.font.Font(font type, font size)
font = pygame.font.Font('./Projects/Runner/Assets/Font/SenorSaturno-Aw9g.ttf', 50)

# background suface
background_surface = pygame.image.load('./Projects/Runner/Assets/Graphics/background.jpg').convert()
background_surface = pygame.transform.scale(background_surface, (800, 400))

# text_surface = test_font.render(text, Antialiasing?, color)
score_surface = font.render('My Game', False, 'White')
score_rect = score_surface.get_rect(center=(400, 55))

# snail surface
snail_surface = pygame.image.load('./Projects/Runner/Assets/Graphics/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(600, 337))

# player surface
player_surf = pygame.image.load('./Projects/Runner/Assets/Graphics/player_walk_1.png').convert_alpha()
# player_rect = pygame.Rect(left, top, width, height)
player_rect = player_surf.get_rect(midbottom=(80, 337))

# while loop keeps the screen open
while True:
    # event loop checking for all types of player input
    # most common events: https://www.pygame.org/docs/ref/event.html
    for event in pygame.event.get():
        # close window
        if event.type == pygame.QUIT:
            pygame.quit()
            # using exit from sys import exit breaks out of the loop
            exit()
        # prints mouse position
        # if event.type == pygame.MOUSEMOTION:
        #     print(event.pos)
        # prints if mouse has been released
        # if event.type == pygame.MOUSEBUTTONUP:
        #     print('mouse up')
        # prints if mouse is clicked
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     print('mouse down')
        # prints collision if collision with mouse
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos):
        #         print("collision")


    # draw all out elements
    # blit means block image transfer
    # screen.blit(suface, position)

    # background
    screen.blit(background_surface, (0, 0))
    screen.blit(score_surface, score_rect)

    # snail
    snail_rect.x -= 4
    if snail_rect.right <= 0:
        snail_rect.left = 800
    screen.blit(snail_surface, snail_rect)

    # player
    screen.blit(player_surf, player_rect)

    # collision
    # if player_rect.colliderect(snail_rect):
    #     print('collision')

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint((x,y)):
    #     print('collision')
    # is player and mouse collide, get status of buttons
    # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())

    # update everything
    pygame.display.update()
    # sets ceiling/max at 60 fps. Should also set floor for more complex games
    # but that is not done here.
    clock.tick(60)