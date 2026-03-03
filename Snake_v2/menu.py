
import pygame
from pygame import Vector2

def run_menu(screen, clock, score):
    pygame.init()
    display_width = 800
    display_heigth = 600
    class change_menu(Exception):
        def __init__(self, scene):
            self.scene = scene
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

    class Menu:
        def __init__(self, running, buttons):
            self.running = running
            self.buttons = buttons
        def change_scene(self, val):
            raise change_menu(val)

    m = Menu(True, [])
    mouse = Mouse(pygame.Rect(0, 0, 10, 10),pygame.mouse.get_pos())
    smallfont = pygame.font.SysFont('Corbel',35) 
    score_text = smallfont.render('Score:  ' + str(score), True , (70, 50, 255)) 
    score_text_rect = score_text.get_rect(center=(display_width/2, display_heigth/2-50))
    menu_button = Button(True, False, (255, 0, 0), (100, 100, 100), Vector2(display_width/2, display_heigth/2), Vector2(100, 50), "Start", 2)
    leaderboard_button = Button(True, False, (255, 0, 0), (100, 100, 100), Vector2(display_width/2, display_heigth/2+70), Vector2(100, 50), "Leaderboard", 3)
    m.buttons = [menu_button, leaderboard_button]
    def Instantiate_buttons():
        for i in m.buttons:
            i.detect_collision()
            i.Instantiate()
    text = smallfont.render('SNAKE (v2)' , True , (70, 50, 255)) 
    while m.running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    m.change_scene(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in m.buttons:
                        if i.pressed and i.ID == 2:
                            print("started game")
                            m.change_scene(2)
                        if i.pressed and i.ID == 3:
                            m.change_scene(3)



            #----

            try:
                screen.fill((0, 0, 0))
                # -instantiate visible things only after this-

                mouse.update_pos()
                Instantiate_buttons()
                text_rect = text.get_rect(center=(display_width // 2, display_heigth // 2-200))
                screen.blit(text , text_rect) 
                screen.blit(score_text, score_text_rect)
                #----

                pygame.display.flip()
                clock.tick(60)
            except pygame.error:
                pass
        except change_menu as e:
            return e.scene