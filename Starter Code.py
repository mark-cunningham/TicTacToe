#!/usr/bin/python
# Tic Tac Toe
# Code Angel


import sys
import os
import pygame
from pygame.locals import *
import random

# Define the colours
X_COLOUR = (54, 169, 225)
O_COLOUR = (149, 193, 31)
TIE_COLOUR = (130, 163, 161)
BACK_COLOUR = (41, 35, 92)
GRID_COLOUR = (45, 46, 131)


# Define constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BOX_BLOCK_SIZE = 112
BOARD_TOP = 64
LINE_WIDTH = 16
WINNING_LINE_WIDTH = 8
SCOREBOARD_MARGIN = 4
SCOREBOARD_HEIGHT = 36

# Setup
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
clock = pygame.time.Clock()
score_font = pygame.font.SysFont('Helvetica', 24)
board_font = pygame.font.SysFont('Helvetica Bold', 128)

# Load sounds
win_sound = pygame.mixer.Sound('win.ogg')