import pygame
from pygame import Vector2
import random


display_heigth = int(600)
display_width = int(800)
tile_size = 50
running = True

pygame.init()
screen = pygame.display.set_mode((display_width, display_heigth))
clock = pygame.time.Clock()

snake = []
tilemap = []
fruits = []

# instantiate_part drawing tile for every object

class Fruit:
    def __init__(self, position, index, rect):
        self.position = position
        self.index = index
        self.rect = pygame.Rect(position.x, position.y, tile_size, tile_size)
    def instantiate_part(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.position, (tile_size, tile_size)))

#class for every tile of tile_size length in scene 

class Tile:
    def __init__(self, position=Vector2, taken=bool, occupant=str):
        self.position = position
        self.taken = taken
        self.occupant = occupant

#class following the head of the snake

class Body:
    def __init__(self, position, marker, index):
        self.position = position
        self.marker = marker
        self.index = index
    def instantiate_part(self):
        pygame.draw.rect(screen, (0, 0, 255), (self.position, (tile_size, tile_size)))

    #moves to his front body's position
    
    def move(self):
        if snake[-1] == self:
            tile = get_tile_from_pos(self.position)
            tilemap[int(tile.y)][int(tile.x)].taken = False
            tilemap[int(tile.y)][int(tile.x)].occupant = None
        self.position = snake[self.index-1].marker.copy()
    
    #sets up marker for back body

    def mark(self):
        self.marker = self.position.copy()

class Snake:
    
    def __init__(self, position, thrust, marker, rect):
        self.position = position
        self.thrust = thrust
        self.marker = marker
        self.rect = pygame.Rect(
            position.x, position.y, tile_size, tile_size
        )
    def instantiate_part(self):
        pygame.draw.rect(screen, (0, 0, 255), (self.position, (tile_size, tile_size)))

    #moves the head in the x or y direction tile_size times and senses collision between himself and the body

    def move(self):
        self.position.x += self.thrust.x * tile_size
        self.position.y += self.thrust.y * tile_size
        self.rect.topleft = (self.position.x, self.position.y)
        tile_index = get_tile_from_pos(self.position)
        tile = tilemap[int(tile_index.y)][int(tile_index.x)]
        if tile.taken == True and tile.occupant != "fruit":
            print("lost the game")
            global running
            running = False
        else:
            tile.taken = True
            tile.occupant = "snake"
    def change_throttle(self, value):
        self.thrust.x = value.x
        self.thrust.y = value.y

    #sets up marker for the body

    def mark(self):
        self.marker = self.position.copy()



def make_tilemap():
    for j in range(0, display_heigth, 50):
        column = []
        for i in range(0, display_width, 50):
            column.append(Tile(Vector2(i, j), False))
        tilemap.append(column)

#gives index of a tile from a vector2 position

def get_tile_from_pos(position=Vector2):
    x = position.x // tile_size
    y = position.y // tile_size
    return Vector2(x, y)

#spawns a fruit in a random non occupied spot

def spawn_fruit():
    rand_x = random.randrange(0, display_width, 50)
    rand_y = random.randrange(0, display_heigth, 50)
    tile_index = get_tile_from_pos(Vector2(rand_x, rand_y))
    tile = tilemap[int(tile_index.y)][int(tile_index.x)]
    if not tile.taken:
       tile.taken = True
       tile.occupant = "fruit"

       prefab = Fruit(Vector2(rand_x, rand_y), len(fruits), None)
       fruits.append(prefab)
    else:
        spawn_fruit()

#makes the beginner 3 part snake

def make_snake():
    for i in range(0, 3):
        if i == 0:      
            snake_pos = Vector2(display_width/2, display_heigth/2)
            snake_throttle = Vector2(0, -1)
            snake.append(Snake(snake_pos, snake_throttle, Vector2(snake_pos.x, snake_pos.y+50), None))
        else:
            snake_pos = Vector2(snake[i-1].marker.x, snake[i-1].marker.y)
            
            snake.append(Body(snake_pos,Vector2(snake_pos.x, snake_pos.y+50), i))
    instntiate_snake()

#instantiates the snake every frame

def instntiate_snake():
    for i in range(0, len(snake)):
        snake[i].mark()
        snake[i].move()
        snake[i].instantiate_part()

#instantiates the fruits every frame

def instantiate_fruits():
    for i in range(0, len(fruits)):
        fruits[i].index = i
        fruits[i].instantiate_part()

#instantiates all bodies on the screen

def instantiate_main():
    screen.fill((0, 0, 0))
    instntiate_snake()
    instantiate_fruits()

#adds a snake part

def add_part():
    snake_index = len(snake)
    snake_pos = snake[snake_index-1].marker
    snake.append(Body(snake_pos, Vector2(snake_pos.x, snake_pos.y), snake_index))

#detects collision betweenthe head and the fruit

def collision_fruit():
        
    for i in range(len(fruits) - 1, -1, -1):
        if snake[0].rect.colliderect(fruits[i].rect):
            fruits.pop(i)
            add_part()
            spawn_fruit()

#checks if head is out of borders and returns false if touched

def check_borders():
    head = snake[0]
    if head.position.x > display_width or head.position.x < 0 or head.position.y > display_heigth or head.position.y < 0:
        print("lost the game")
        return False
    else:
        return True
    
        


   
#main game loop

def start_game():
    
    pressed = False
    global running


    make_tilemap()
    make_snake()
    spawn_fruit()

    

    while running:
        for event in pygame.event.get():

            #checks if quit game

            if event.type == pygame.QUIT:
                running = False
            
            #input detection

            if event.type == pygame.KEYDOWN and pressed == False:
                value = snake[0].thrust.copy()
    
                if event.key in (pygame.K_w, pygame.K_UP) and value.y != 1:
                    value = Vector2(0, -1)
                elif event.key in (pygame.K_s, pygame.K_DOWN) and value.y != -1:
                    value = Vector2(0, 1)
                elif event.key in (pygame.K_d, pygame.K_RIGHT) and value.x != -1:
                    value = Vector2(1, 0)
                elif event.key in (pygame.K_a, pygame.K_LEFT) and value.x != 1:
                    value = Vector2(-1, 0)
    
                snake[0].change_throttle(value)
                pressed = True
           
        
           
            
            
        
        #----

        collision_fruit()
        running = check_borders()
        instantiate_main()
        #----
        #disables the ability to move in the opposite direction pressing both keys at once
        pressed = False

        pygame.display.flip()

        #3 frames per second update

        clock.tick(3)
    
start_game()
