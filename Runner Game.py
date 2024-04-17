import pygame
from sys import exit

# Docs: https://www.pygame.org/docs/
# Graphics: itch.io
# Background autumn landscale park background from macrovector on freepik.com
# front https://www.fontspace.com/golden-avocado-sans-font-f114319 
# https://www.youtube.com/watch?v=AY9MnQ4x3zk 2:15:43

pygame.init()

def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surf = font.render(f'Score: {current_time}', False, ('White'))
    score_rect = score_surf.get_rect(bottomleft = (300,90))
    screen.blit(score_surf, score_rect)
    return current_time

game_active = False
start_time = 0
score = 0

# create display surface
# screen = pygame.display.set_mode((width, height))
screen = pygame.display.set_mode((800, 400))

# title. Could also set icon with pygame.display.set_icon('img.jpg')
pygame.display.set_caption('Snail Runner')

# clock object helps us with time and making sure framerate is constant
clock = pygame.time.Clock()

# fonts
font = pygame.font.Font('./Projects/Runner/Assets/Font/GoldenAvocadoSans-Yqq1q.otf', 50)
small_font = pygame.font.Font('./Projects/Runner/Assets/Font/GoldenAvocadoSans-Yqq1q.otf', 40)

# title
title_surf = small_font.render('Snail Runner', False, 'White')
title_rect = title_surf.get_rect(center=(400, 80))

# instructions
instructions_surf = small_font.render('Press spacebar to run', False, 'White')
instructions_rect = instructions_surf.get_rect(center = (400, 320))

# background suface
background_surface = pygame.image.load('./Projects/Runner/Assets/Graphics/background.jpg').convert()
background_surface = pygame.transform.scale(background_surface, (800, 400))

# snail surface
snail_surface = pygame.image.load('./Projects/Runner/Assets/Graphics/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(600, 337))
pygame.display.set_icon(snail_surface)

# player surface
player_surf = pygame.image.load('./Projects/Runner/Assets/Graphics/player_walk_1.png').convert_alpha()
# player_rect = pygame.Rect(left, top, width, height)
player_rect = player_surf.get_rect(midbottom=(80, 337))

# starting/ending screen
player_stand = pygame.image.load('./Projects/Runner/Assets/Graphics/player_stand.png').convert_alpha()
# scale player
player_stand = pygame.transform.scale(player_stand, (100, 130))
player_stand_rect = player_stand.get_rect(center=(400, 200))

# gravity
player_gravity = 0

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
        if game_active:
            # click on player to jump if player is on the floor
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 337:
                    player_gravity = -20
            # space bar to jump if player is on the floor
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 337:
                    player_gravity = -20
        else:
            # restart game if space is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                start_time = pygame.time.get_ticks()

    end_time = 0

    # draw all out elements
    if game_active:
        # background
        screen.blit(background_surface, (0, 0))

        # score
        # pygame.draw.rect(screen, '#5CA336', score_rect, 10, 20)
        # pygame.draw.rect(screen, '#5CA336', score_rect)
        # screen.blit(score_surface, score_rect)
        score = display_score()

        # snail
        snail_rect.x -= 4
        if snail_rect.right <= 0:
            snail_rect.left = 800
        screen.blit(snail_surface, snail_rect)

        # player
        player_gravity += 1
        player_rect.y += player_gravity
        screen.blit(player_surf, player_rect)
        if player_rect.bottom >= 337:
            player_rect.bottom = 337
            player_gravity = 0

        # collision
        if player_rect.colliderect(snail_rect):
            end_time = pygame.time.get_ticks() // 1000
            game_active = False

    else:
        # game menu screen
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title_surf, title_rect)
        if score == 0:
            screen.blit(instructions_surf, instructions_rect)
        else:
            score_message = font.render(f'Your score: {score}', False, 'White')
            score_message_rect = score_message.get_rect(center=(400,320))
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    # sets ceiling/max at 60 fps. Should also set floor for more complex games
    # but that is not done here.
    clock.tick(60)
