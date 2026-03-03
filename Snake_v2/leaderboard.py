
import pygame
from pygame import Vector2
import socket
import json
import time
import requests



def run_leaderboard(screen, clock, score):
    client = socket.socket() 
    def get_leaderboard(name, score):
        port = 2345
        client.connect(('127.0.0.1', port))
        client.send(name.encode())
        time.sleep(0.01)
        client.send(str(score).encode())
        data_str = client.recv(1024).decode()
        data = json.loads(data_str)
        client.close()
        return data
    player_data = get_leaderboard(requests.get('https://api.ipify.org').text, score)
    pygame.init()
    display_width = 800
    display_heigth = 600
      
    class change_menu(Exception):
        def __init__(self, scene):
            self.scene = scene
    class Leaderboard_Cloumn:
        def __init__(self, color, position):
            self.color = color
            self.position = position
            self.rect = pygame.Rect(self.position, Vector2(display_width-(display_width//8), 25))
            self.place = 0
            self.name = "nil"
            self.score = 0
            self.font = pygame.font.SysFont("Corbel", 20)
            self.rect.center = self.position
        def instantiate(self):
            pygame.draw.rect(screen, self.color, self.rect)
            text_positions = [(self.position.x-300, self.position.y),(self.position.x - 150, self.position.y), (self.position.x + 200, self.position.y)]
            text_text = [str(self.place), self.name,  str(self.score)]
            for i in range(0, 3):
                text = self.font.render(text_text[i], True, (255, 255, 255))
                text_rect = text.get_rect(center=text_positions[i])
                screen.blit(text ,text_rect)

    class Button:
        def __init__(self, enalbled, pressed , Color, Color_when_pressed,  position, size, text, ID):
            self.enabled = enalbled
            self.pressed = pressed
            self.Color = Color
            self.Color_when_pressed = Color_when_pressed
            self.position = position
            self.size = size
            self.rect = pygame.Rect(self.position, self.size)
            self.text = text
            self.ID = ID
            self.now_color = (0, 0, 0)
            self.font = pygame.font.SysFont('Corbel', 20)
            self.button_text = self.font.render(str(text), True, (255, 255, 255))
            self.button_text_rect = self.button_text.get_rect(center=self.position)
        def Instantiate(self):
            self.rect = pygame.Rect((0, 0), self.size)
            self.rect.center = self.position
            pygame.draw.rect(screen, self.now_color, self.rect)
            if text != None:
                screen.blit(self.button_text, self.button_text_rect)

        def detect_collision(self):
            if self.enabled and self.rect:
                if self.rect.colliderect(mouse.rect):
                    self.now_color = self.Color_when_pressed
                    self.pressed = True
                else:
                    self.pressed = False
                    self.now_color = self.Color
    class Mouse:
        def __init__(self, rect, position):
            self.rect = rect
            self.position = position
        def update_pos(self):
            self.position = pygame.mouse.get_pos()
            self.rect.center = self.position

    class Leaderboard:
        def __init__(self, running, buttons, columns):
            self.running = running
            self.buttons = buttons
            self.columns = columns
            self.leaderboard_players = player_data
        def change_scene(self, val):
            raise change_menu(val)

    m = Leaderboard(True, [], [])
    mouse = Mouse(pygame.Rect(0, 0, 10, 10),pygame.mouse.get_pos())
    #instantiate buttons in here and put them into the array
    back_button = Button(True, False, (255, 0, 0), (100, 100, 100), (display_width/2+100, display_heigth/2+250), (70, 50), "Back", 1)
    m.buttons = [back_button]
    #-----
    
    def Instantiate_buttons():
        for i in m.buttons:
            i.detect_collision()
            i.Instantiate()
    def make_leaderboard():
        for i in range(0, 10):
            c = Leaderboard_Cloumn((100, 100, 100), Vector2(display_width//2, display_heigth//2-200+30*i+20))
            c.place = i+1
            try:
                c.name = list(m.leaderboard_players.keys())[i]
                c.score = m.leaderboard_players[c.name]
            except IndexError:
                c.name = ""
                c.score = 0
            m.columns.append(c)
            c.instantiate()
    make_leaderboard()
    def instantiate_leaderboard():
        for i in m.columns:
            i.instantiate()
    smallfont = pygame.font.SysFont('Corbel',35) 
    text = smallfont.render('Leaderbard' , True , (70, 50, 255)) 
    while m.running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    m.change_scene(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in m.buttons:
                        if i.pressed and i.ID == 1:
                            m.change_scene(1)



            #----

            try:
                screen.fill((0, 0, 0))
                # -instantiate visible things only after this-

                mouse.update_pos()
                Instantiate_buttons()
                instantiate_leaderboard()
                text_rect = text.get_rect(center=(display_width // 2, display_heigth // 2-250))
                screen.blit(text , text_rect) 

                #----

                pygame.display.flip()
                clock.tick(60)
            except pygame.error:
                pass
        except change_menu as e:
            return e.scene