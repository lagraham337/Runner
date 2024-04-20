import pygame
from sys import exit
from random import randint

# Docs: https://www.pygame.org/docs/
# Graphics: itch.io
# Background autumn landscale park background from macrovector on freepik.com
# front https://www.fontspace.com/golden-avocado-sans-font-f114319 
# https://www.youtube.com/watch?v=AY9MnQ4x3zk 2:51:43

pygame.init()

def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surf = font.render(f'Score: {current_time}', False, ('White'))
    score_rect = score_surf.get_rect(bottomleft = (300,90))
    screen.blit(score_surf, score_rect)
    return current_time

# obstacles logic
# 1. we create a list of obstacle rectangles
# 2. everytime the timer triggers we add a new rectangle to that list.
# 3. We move every rectangle in that list to the left on every frame.
# 4. We delete rectangles too far left. 
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 337:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)
        # only copies existing item in list if obstacle is on the screen
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_surf, player_index
    # display the jump surface when player is not on floor
    if player_rect.bottom < 337:
        player_surf = player_jump
    # play walking animation if the player is on the floor
    else:
        player_index += 0.1
        if int(player_index) % 2 == 0:
            player_surf = player_walk[0]
        else:
            player_surf = player_walk[1]
        if player_index >= 2:
            player_index = 0

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
font = pygame.font.Font('./Assets/Font/GoldenAvocadoSans-Yqq1q.otf', 50)
small_font = pygame.font.Font('./Assets/Font/GoldenAvocadoSans-Yqq1q.otf', 40)

# title
title_surf = small_font.render('Snail Runner', False, 'White')
title_rect = title_surf.get_rect(center=(400, 80))

# instructions
instructions_surf = small_font.render('Press spacebar to run', False, 'White')
instructions_rect = instructions_surf.get_rect(center = (400, 320))

# background suface
background_surface = pygame.image.load('./Assets/Graphics/background.jpg').convert()
background_surface = pygame.transform.scale(background_surface, (800, 400))

# OBSTACLES
# fly surface
fly_frame_1 = pygame.image.load('./Assets/Graphics/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('./Assets/Graphics/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index] 

# snail surface
snail_frame_1 = pygame.image.load('./Assets/Graphics/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('./Assets/Graphics/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

pygame.display.set_icon(snail_frame_1)

obstacle_rect_list = []

# player surface
player_walk_1 = pygame.image.load('./Assets/Graphics/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('./Assets/Graphics/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('./Assets/Graphics/jump.png').convert_alpha()
# player_rect = pygame.Rect(left, top, width, height)
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 337))

# starting/ending screen
player_stand = pygame.image.load('./Assets/Graphics/player_stand.png').convert_alpha()
# scale player
player_stand = pygame.transform.scale(player_stand, (100, 130))
player_stand_rect = player_stand.get_rect(center=(400, 200))

# gravity
player_gravity = 0

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 250)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 80)

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
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 337)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1100), 250)))
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]
                    
        else:
            # restart game if space is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                #snail_rect.left = 800
                start_time = pygame.time.get_ticks()


    end_time = 0

    # draw all out elements
    if game_active:
        # background
        screen.blit(background_surface, (0, 0))

        # score
        score = display_score()

        # player
        player_gravity += 1
        player_rect.y += player_gravity
        player_animation()
        screen.blit(player_surf, player_rect)
        if player_rect.bottom >= 337:
            player_rect.bottom = 337
            player_gravity = 0

        # obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        # game menu screen
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title_surf, title_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 337)
        player_gravity = 0
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
