import menu
import Main
import pygame
import leaderboard
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

class Launcher:
    def __init__(self, scene, score):
       self.scene = scene
       self.score = score
L = Launcher(1, 0)
scenes = [menu.run_menu ,Main.run_game , leaderboard.run_leaderboard] 
while True:
    if L.scene != 0:
        if L.scene == 2:
            L.scene, L.score = scenes[L.scene-1](screen, clock)
        elif L.scene == 1 or L.scene == 3:
            L.scene = scenes[L.scene-1](screen, clock, L.score)
        else:
            L.scene = scenes[L.scene-1](screen, clock)
    else:
        break