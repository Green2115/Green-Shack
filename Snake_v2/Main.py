import pygame
from pygame import Vector2
import random
import subprocess
import sys
import time
import random
try:
    import pygame as pygame
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
def run_game(screen, clock):
    pygame.init()
    print("started snake")
    display_heigth = int(600)
    display_width = int(800)
    tile_size = 50
    class stop_game(Exception):
        pass
    
    class Game:
        def __init__(self, snake_refresh_cooldown, last_snake_refresh, snake, tilemap, fruits, running, score):
            self.snake_refresh_cooldown = snake_refresh_cooldown
            self.last_snake_refresh = last_snake_refresh
            self.snake = snake
            self.tilemap = tilemap
            self.fruits = fruits
            self.running = running
            self.score = score
    

    
    
    g = Game(250, 0, [], [], [], True, 0)
    # instantiate_part drawing tile for every object
    
    class Fruit:
        def __init__(self, position, index, color):
            self.position = position
            self.index = index
            self.rect = pygame.Rect(position.x, position.y, tile_size, tile_size)
            self.color = color
        def instantiate_part(self):
            pygame.draw.rect(screen, self.color, (self.position, (tile_size, tile_size)))
    
    #class for every tile of tile_size length in scene 
    
    class Tile:
        def __init__(self, position=Vector2, taken=bool, occupant=str):
            self.position = position
            self.taken = taken
            self.occupant = occupant
    
    #class following the head of the g.snake
    
    class Body:
        def __init__(self, position, marker, index):
            self.position = position
            self.marker = marker
            self.index = index
        def instantiate_part(self):
            pygame.draw.rect(screen, (0, 0, 255), (self.position, (tile_size, tile_size)))
    
        #moves to his front body's position
        
        def move(self):
            if g.snake[-1] == self:
                tile = get_tile_from_pos(self.position)
                g.tilemap[int(tile.y)][int(tile.x)].taken = False
                g.tilemap[int(tile.y)][int(tile.x)].occupant = None
            self.position = g.snake[self.index-1].marker.copy()
        
        #sets up marker for back body
    
        def mark(self):
            self.marker = self.position.copy()
    class Snake:
        
        def __init__(self, position, thrust, marker, rect, img, angle):
            self.position = position
            self.thrust = thrust
            self.marker = marker
            self.rect = pygame.Rect(
                position.x, position.y, tile_size, tile_size
            )
            self.img = img
            self.angle = angle
        def instantiate_part(self):
            head_img = pygame.image.load(self.img).convert()
            head_img = pygame.transform.scale(head_img, (tile_size, tile_size))
            self.angle.x = {-1: 90, 1: 270}.get(self.thrust.x, 0)
            self.angle.y = {-1: 0, 1: 180}.get(self.thrust.y, 0)
            rotated_head = pygame.transform.rotate(head_img, self.angle.x + self.angle.y)
            screen.blit(rotated_head, self.position)
    
        #moves the head in the x or y direction tile_size times and senses collision between himself and the body
    
        def move(self):
            self.position.x += self.thrust.x * tile_size
            self.position.y += self.thrust.y * tile_size
            self.rect.topleft = (self.position.x, self.position.y)
            try:
                tile_index = get_tile_from_pos(self.position)
                tile = g.tilemap[int(tile_index.y)][int(tile_index.x)]
                if tile.taken == True and tile.occupant not in ["apple", "lime"]:
                    print("lost the game")
                    raise stop_game
                elif tile.occupant == "lime":
                    print("ate lime")
                    g.score += 1
                else:
                    tile.taken = True
                    tile.occupant = "snake"
            except IndexError:
                print("lost the game")
                raise stop_game
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
                column.append(Tile(Vector2(i, j), False, "None"))
            g.tilemap.append(column)
    
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
        tile = g.tilemap[int(tile_index.y)][int(tile_index.x)]
        if not tile.taken:
            tile.taken = True
            
            if random.randint(0, 10) == 1:
                color = (0, 255, 0)
                tile.occupant = "lime"
                print(f"spawned line: {tile.occupant}")
            else:
                color = (255, 0, 0)
                tile.occupant = "apple"
            prefab = Fruit(Vector2(rand_x, rand_y), len(g.fruits), color)
            g.fruits.append(prefab)
        else:
            spawn_fruit()
    
    #makes the beginner 3 part g.snake
    
    def make_snake():
        for i in range(0, 3):
            if i == 0:      
                snake_pos = Vector2(display_width/2, display_heigth/2)
                snake_throttle = Vector2(0, -1)
                g.snake.append(Snake(snake_pos, snake_throttle, Vector2(snake_pos.x, snake_pos.y+50), None, r'Snake_v2/sprites/snake_head.png', Vector2(0, 90)))
            else:
                snake_pos = Vector2(g.snake[i-1].marker.x, g.snake[i-1].marker.y)
                
                g.snake.append(Body(snake_pos,Vector2(snake_pos.x, snake_pos.y+50), i))
        instntiate_snake()
    
    #instantiates the g.snake every frame
    
    def instntiate_snake():
        for i in range(0, len(g.snake)):
            g.snake[i].mark()
            g.snake[i].move()
            g.snake[i].instantiate_part()
    
    #instantiates the g.fruits every frame
    
    def instantiate_fruits():
        for i in range(0, len(g.fruits)):
            g.fruits[i].index = i
            g.fruits[i].instantiate_part()
    
    #instantiates all bodies on the screen
    
    
    
    #adds a g.snake part
    
    def add_part():
        g.score += 1
        snake_index = len(g.snake)
        snake_pos = g.snake[snake_index-1].marker
        g.snake.append(Body(snake_pos, Vector2(snake_pos.x, snake_pos.y), snake_index))
    
    #detects collision betweenthe head and the fruit
    
    def collision_fruit():
            
        for i in range(len(g.fruits) - 1, -1, -1):
            if g.snake[0].rect.colliderect(g.fruits[i].rect):
                g.fruits.pop(i)
                add_part()
                spawn_fruit()
    
    
    #main game loop
    
    
    
    pressed = False
    make_tilemap()
    make_snake()
    spawn_fruit()

    while g.running:
        try:
            for event in pygame.event.get():
                #checks if quit game
                if event.type == pygame.QUIT:
                    not g.running
                    raise stop_game


                #input detection
                if event.type == pygame.KEYDOWN and pressed == False:
                    value = g.snake[0].thrust.copy()

                    if event.key in (pygame.K_w, pygame.K_UP) and value.y != 1:
                        value = Vector2(0, -1)
                    elif event.key in (pygame.K_s, pygame.K_DOWN) and value.y != -1:
                        value = Vector2(0, 1)
                    elif event.key in (pygame.K_d, pygame.K_RIGHT) and value.x != -1:
                        value = Vector2(1, 0)
                    elif event.key in (pygame.K_a, pygame.K_LEFT) and value.x != 1:
                        value = Vector2(-1, 0)

                    g.snake[0].change_throttle(value)
                    pressed = True




            try:  

                #----
                
                now = time.perf_counter() * 1000
                collision_fruit()
                if g.snake[0].position.x > display_width or g.snake[0].position.x < 0 or g.snake[0].position.y > display_heigth or g.snake[0].position.y < 0:
                    not g.running
                    raise stop_game

                if now - g.last_snake_refresh > g.snake_refresh_cooldown:
                    g.last_snake_refresh = now
                    screen.fill((0, 0, 0))
                    instantiate_fruits()
                    instntiate_snake()
                    pressed = False
                #----
                pygame.display.flip()
                #60 frames per second update
                clock.tick(60)
            except pygame.error:
                pass
        except stop_game:
            return (1, g.score)
            