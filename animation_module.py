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
clock = pygame.time.Clock()
fps=40





class Animation:

    def __init__(self,mainsheet_path,x_cells,y_cells):
        mainsheet= pygame.image.load(mainsheet_path).convert_alpha()

        sheet_size = mainsheet.get_size()
        cell_width = int(sheet_size[0] / x_cells)
        cell_height = int(sheet_size[1] / y_cells)
        self.cell_list=[]
        self.cell_position = 0
        for y in range(0,sheet_size[1],cell_height):
            for x in range(0,int(sheet_size[0]),int(cell_width)):
                surface = pygame.Surface((cell_width,cell_height))
                surface.blit(mainsheet,(0,0),(x,y,cell_width,cell_height))
                colorkey = surface.get_at((10,10))
                surface.set_colorkey(colorkey)
                self.cell_list.append(surface)



    def animate(self,window,x,y,cell_range):

        self.cell_range = cell_range
        if self.cell_position not in range(cell_range[0],cell_range[1]):
            self.cell_position = self.cell_range[0]

        if self.cell_position < self.cell_range[1]-1:
            self.cell_position += 1
        else:
            self.cell_position = self.cell_range[0]
        window.blit(self.cell_list[self.cell_position],(x,y))




