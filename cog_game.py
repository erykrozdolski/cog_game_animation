__author__ = 'Eryk'
__author__ = 'Eryk'
#!/usr/bin/python
#-*-coding: utf-8-*-
import sys
import pygame
import random
from animation_module import *
from colors import *
pygame.init()
window_size = window_width,window_height = 1200,600
window = pygame.display.set_mode(window_size)
player_mainsheet = ('mainsheet.png',6,16)
central_cog =('trybik duzy-01.png')
left_cog = ('trybik lewy-01.png')
right_cog = ('trybik prawy-01.png')
clock = pygame.time.Clock()
fps=30
run_right = [0,24]
run_left = [24,48]
static_left = [48,49]
static_right = [54,55]
dunk_left = [51,52]
dunk_right = [57,58]
right_shot = [60,72]
left_shot = [72,84]
right_jump_shot = [84,89]
class Cog(pygame.sprite.Sprite):

    def __init__(self,source,where):
        super(Cog,self).__init__()
        self.image = pygame.image.load(source)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = where[0]
        self.rect.y = where[1]
        self.degree=0

    def set_position(self,x,y):
        self.rect.x = x
        self.rect.y = y
    def rotate(self,angle):
        # window.blit(self.image,self.rect)
        obraz = self.image
        oldCenter = self.rect.center
        rotatedSurf =  pygame.transform.rotate(obraz, self.degree)
        rotRect = rotatedSurf.get_rect()
        rotRect.center = oldCenter
        window.blit(rotatedSurf, rotRect)
        self.degree += 1

        if self.degree > 360:
            self.degree = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.width = 10
        self.height = 120
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255,0,255))
        self.image.set_colorkey((255,0,255))
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.mainsheet = player_mainsheet

        self.last_move = 'right'
        self.cog_list = pygame.sprite.Group()
        self.animation_x = 80
        self.animation_y = 25
        self.cell_range = static_right
        self.new_cell_range = static_right
        self.animation = Animation(self.mainsheet[0],self.mainsheet[1],self.mainsheet[2])
        self.fireshot = False
    def set_position(self,x,y):
        self.rect.x = x
        self.rect.y = y

    def update(self):

        self.gravitation()

        self.rect.x += self.change_x

        cog_hit_list = pygame.sprite.spritecollide(self, self.cog_list, False)
        for cog in cog_hit_list:
            if self.change_x > 0:
                self.rect.right = cog.rect.left
            elif self.change_x < 0:
                self.rect.left = cog.rect.right


        self.rect.y += self.change_y
        cog_hit_list = pygame.sprite.spritecollide(self, self.cog_list, False)
        for cog in cog_hit_list:
            if self.change_y > 0:
                self.rect.bottom = cog.rect.top
            elif self.change_y < 0:
                self.rect.top = cog.rect.bottom
            self.change_y = 0
        if self.rect.x >= window_width - self.width-40:
            self.change_x =0
            self.rect.x = window_width - self.width-40
            self.ecll_range = static_left
        if self.rect.x <= 0 + self.width+self.width:
            self.change_x = 0
            self.rect.x = self.width+self.width
            self.cell_range = static_right



    def go_left(self):
        self.last_move ='left'
        self.change_x -= 10


    def go_right(self):
        self.last_move='right'
        self.change_x += 10


    def stop(self):
        self.change_x = 0

    def gravitation(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.75
        if self.rect.y >= window_height - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = window_height - self.rect.height


    def jump(self):
        self.rect.y += 2
        cog_hit_list = pygame.sprite.spritecollide(self,self.cog_list, False)
        self.rect.y -= 2
        if len(cog_hit_list)>0 or self.rect.bottom >= window_height-self.width :
            self.change_y = -15

    def set_cell_range(self):
        if self.fireshot == False:
            if self.change_y == 0 and self.change_x != 0:
                if self.change_x > 0:
                    self.new_cell_range = run_right
                if self.change_x < 0:
                    self.new_cell_range = run_left
            elif self.change_y == 0 and self.change_x == 0 :
                if self.last_move == 'left':
                    self.new_cell_range = static_left
                if self.last_move == 'right':
                    self.new_cell_range = static_right
            elif self.change_y != 0 and self.change_x != 0:
                if self.last_move == 'left':
                    self.new_cell_range = dunk_left
                if self.last_move == 'right':
                    self.new_cell_range = dunk_right
            elif self.change_y != 0 and self.change_x == 0:
                if self.last_move == 'left':
                    self.new_cell_range = dunk_left
                if self.last_move == 'right':
                    self.new_cell_range = dunk_right
        if self.fireshot == True:
            if self.change_y == 0:
                if self.last_move == 'left':
                    self.new_cell_range = left_shot
                if self.last_move == 'right':
                    self.new_cell_range = right_shot
            self.stop()
            if self.animation.cell_position == left_shot[1]-1 or self.animation.cell_position == right_shot[1]-1:
                self.fireshot = False

player_group = pygame.sprite.Group()
first_player=Player()

first_player.set_position(10,1000)
player_group.add(first_player)
c_cog=Cog(central_cog,[600,10])
l_cog=Cog(left_cog,[10,50])
r_cog=Cog(right_cog,[300,200])
first_player.cog_list.add(c_cog)
first_player.cog_list.add(l_cog)
first_player.cog_list.add(r_cog)



while True:

    for event in pygame.event.get():


        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT :
                first_player.go_left()

            if event.key == pygame.K_RIGHT:
                first_player.go_right()
            if event.key == pygame.K_UP:

                first_player.jump()
            if event.key == pygame.K_SPACE:
                first_player.fireshot = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:

                first_player.stop()
            if event.key == pygame.K_RIGHT:
                first_player.stop()
            if event.key == pygame.K_UP and not (pygame.KEYDOWN and pygame.K_LEFT or pygame.K_RIGHT):
                first_player.stop()


    first_player.set_cell_range()



    window.fill(white)
    player_group.draw(window)
    first_player.update()

    player_group.update()

    player_group.draw(window)
    if first_player.new_cell_range != first_player.cell_range:
        first_player.cell_range = first_player.new_cell_range

    l_cog.rotate(20)
    c_cog.rotate(20)
    r_cog.rotate(20)

    first_player.animation.animate(window,first_player.rect.x-first_player.animation_x,first_player.rect.y-first_player.animation_y,first_player.cell_range)


    pygame.display.update()

    clock.tick(fps)