import pygame
from sys import exit
from random import randint, choice
import math

# Docs: https://www.pygame.org/docs/
# Graphics: itch.io
# Background autumn landscale park background from macrovector on freepik.com
# font https://www.fontspace.com/golden-avocado-sans-font-f114319 
# music by Spencer Y.K. from Pixabay
# https://www.youtube.com/watch?v=AY9MnQ4x3zk

pygame.init()

# create display surface
# screen = pygame.display.set_mode((width, height))
frame_height = 400
frame_width = 800
screen = pygame.display.set_mode((frame_width, frame_height))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('./Assets/Graphics/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('./Assets/Graphics/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        player_squat_1 = pygame.transform.scale(player_walk_1, (68, 65))
        player_squat_2 = pygame.transform.scale(player_walk_2, (68, 65))
        self.player_squat = [player_squat_1, player_squat_2]
        self.player_jump = pygame.image.load('./Assets/Graphics/jump.png').convert_alpha()
        self.is_jumping = False
        self.is_squatting = False

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, 337))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('./Assets/Audio/jump.mp3')
        self.jump_sound.set_volume(.15)
        self.squat_sound = pygame.mixer.Sound('./Assets/Audio/whoosh.mp3')
        self.squat_sound.set_volume(.15)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 337:
            self.gravity = -20
            self.jump_sound.play()
            self.is_jumping = True
        else:
            self.is_jumping = False
        
        if keys[pygame.K_s] and not self.is_jumping:
            #self.squat_sound.play()
            self.is_squatting = True
        else:
            self.is_squatting = False

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 337:
            self.rect.bottom = 337
            self.gravity = 0

    def animation_state(self):
        if self.is_jumping:
            self.image = self.player_jump
        elif self.is_squatting:
            self.rect.y = 277
            self.player_index += 0.1
            if int(self.player_index) % 2 == 0:
                self.image = self.player_squat[0]
            else:
                self.image = self.player_squat[1]
            if self.player_index >= 2:
                self.player_index = 0
        else:
            self.player_index += 0.1
            if int(self.player_index) % 2 == 0:
                self.image = self.player_walk[0]
            else:
                self.image = self.player_walk[1]
            if self.player_index >= 2:
                self.player_index = 0

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('./Assets/Graphics/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('./Assets/Graphics/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 270
        else:
            snail_1 = pygame.image.load('./Assets/Graphics/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('./Assets/Graphics/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 337
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self, type = 'snail'):
        if type == 'fly':
            self.animation_index += 0.3
        else:
            self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):                          
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surf = font.render(f'Score: {current_time}', False, ('White'))
    score_rect = score_surf.get_rect(bottomleft = (300,90))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    #pygame.sprite.spritecollide(sprite,group,bool)
    # bool represents if we want sprite deleted in collision
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True

game_active = False
start_time = 0
score = 0
background_music = pygame.mixer.Sound('./Assets/Audio/little_slime.mp3')
background_music.set_volume(.5)
# music
background_music.play(loops = -1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

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
instructions_surf = small_font.render('Press spacebar to jump and S to duck', False, 'White')
instructions_rect = instructions_surf.get_rect(center = (400, 320))

# background suface
background_surface = pygame.image.load('./Assets/Graphics/background.jpg').convert()
background_surface = pygame.transform.scale(background_surface, (800, 400))
scroll = 0
tiles = math.ceil(frame_width / background_surface.get_width()) + 1

# snail iconn
snail_frame_1 = pygame.image.load('./Assets/Graphics/snail1.png').convert_alpha()
pygame.display.set_icon(snail_frame_1)

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
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail'])))    
        else:
            # restart game if space is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
    end_time = 0
    # draw all out elements
    if game_active:
        # scrolling background
        i = 0
        while i < tiles:
            screen.blit(background_surface, (background_surface.get_width()*i + scroll, 0))
            i += 1
        scroll -= 3
        if abs(scroll) > background_surface.get_width():
            scroll = 0

        # score
        score = display_score()

        # draw player and obstacles
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        # collision
        game_active = collision_sprite()

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
