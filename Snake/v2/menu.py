
#import Main
import pygame
from pygame import Vector2
import Main
def Start_menu():
    display_width = 800
    display_heigth = 600
    screen = pygame.display.set_mode((display_width, display_heigth))
    clock = pygame.time.Clock()
    pygame.init()

    class Button:
        def __init__(self, enalbled, pressed , Color, Color_when_pressed,  position, size,text=None):
            self.enabled = enalbled
            self.pressed = pressed
            self.Color = Color
            self.Color_when_pressed = Color_when_pressed
            self.position = position
            self.size = size
            self.rect = pygame.Rect(self.position, self.size)
            self.text = text
            self.now_color = (0, 0, 0)
        def Instantiate(self):
            if text != None:
                pass
            self.rect = pygame.Rect(self.position, self.size)
            pygame.draw.rect(screen, self.now_color, (self.position, self.size))
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

    m = Menu(True, [])
    mouse = Mouse(pygame.Rect(0, 0, 10, 10),pygame.mouse.get_pos())
    smallfont = pygame.font.SysFont('Corbel',35) 
    menu_button = Button(True, False, (255, 0, 0), (100, 100, 100), Vector2(display_width/2, display_heigth/2), Vector2(50, 50))
    m.buttons.append(menu_button)
    def Instantiate_buttons():
        for i in m.buttons:
            i.detect_collision()
            i.Instantiate()
    text = smallfont.render('SNAKE (v2)' , True , (70, 50, 255)) 
    while m.running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                m.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in m.buttons:
                    if i.pressed == True:
                        print("started game")
                        pygame.quit()
                        Main.start_game()
                        m.running = False
                        


        #----

        try:
            screen.fill((0, 0, 0))
            # -instantiate visible things only after this-

            mouse.update_pos()
            Instantiate_buttons()
            pygame.draw.rect(screen, (255, 0, 0), (mouse.position, (10, 10)))
            text_rect = text.get_rect(center=(display_width // 2, display_heigth // 2-200))
            screen.blit(text , text_rect) 

            #----

            pygame.display.flip()
            clock.tick(60)
        except pygame.error:
            pass

Start_menu()