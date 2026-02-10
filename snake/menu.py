
from Main import start_game
from Main import Game
import pygame
from pygame import Vector2
display_width = 800
display_heigth = 600
screen = pygame.display.set_mode((display_width, display_heigth))
clock = pygame.time.Clock()
pygame.init()

class menu:
    def __init__(self, running):
        self.running = running

m = menu(True)

while m.running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            m.running = False

    

    pygame.display.flip()
    clock.tick(60)
