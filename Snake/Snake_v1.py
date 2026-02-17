
import pygame
import random



running = True

display_heigth = int(600)

display_width = int(800)

tile_size = 50

pygame.init()





screen = pygame.display.set_mode((display_width, display_heigth))
clock = pygame.time.Clock()

#enables x/y coordinate 
tiles_c = []
class tile:
    def __init__(self, position=tuple, taken=bool):
        self.position = position
        self.taken = taken
    def switch(self):
        self.taken = not self.taken
class spawnpoint:
    def __init__(self, thrust, position):
        self.position = position
        self.thrust = thrust
class fruit:
    def __init__(self, position, color, show):
        self.position = position
        self.color = color
        self.rect = pygame.Rect(
            position.x, position.y, tile_size, tile_size
        )
        self.show = show

    def Instantiate(self):
        pygame.draw.rect(screen, self.color.get_color(), self.rect)

class vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def get_position(self):
        return self.x, self.y
class RGB:
    def __init__(self, R, G, B):
        self.R = R
        self.G = G
        self.B = B
    def get_color(self):
        return (self.R, self.G, self.B)

class cube:
    def __init__(self, position, color, marker, thrust, index):
        self.position = position
        self.color = color
        self.marker = marker
        self.thrust = thrust
        self.index = index
        self.rect = pygame.Rect(
            position.x, position.y, tile_size, tile_size
        )
        

    def move(self):
        self.position.x += self.thrust.x * tile_size
        self.position.y += self.thrust.y * tile_size
        self.rect.topleft = self.position.get_position()
    def Instantiate(self): 
        rect = pygame.draw.rect(screen, self.color.get_color(), (self.position.get_position(), (tile_size, tile_size))) 
    def move_body(self):
        
        self.position.x = snake[self.index - 1].marker.position.x
        self.position.y = snake[self.index - 1].marker.position.y
    def initiate_marker(self):
        if self == snake[-1] and self.marker.position.x != 0:
            tile = give_tile_index_from_pos(vector2(self.marker.position.x, self.marker.position.y))
            tilemap[tile.x][tile.y].switch()
        if self == snake[0] and self.marker.position.x != 0:
            tile = give_tile_index_from_pos(vector2(self.position.x, self.position.y))
            tilemap[tile.x][tile.y].switch()
        self.marker.position = vector2(self.position.x, self.position.y)
        self.marker.thrust = vector2(self.thrust.x, self.thrust.y)





Index = 0
tilemap = []
def make_tilemap():
    
    for j in range(0, display_heigth, 50):
        column = []
        for i in range(0, display_width, 50):
            column.append(tile(vector2(i, j), False))
        tilemap.append(column)

make_tilemap()
def give_tile_index_from_pos(position=type(vector2)):
    
    for j in range(0, len(tilemap)):
        if tilemap[j][0].position.y == position.y:
            y_cor = j
            print(f"y_index {j}")
        for i in range(0, len(tilemap[j])):
           
            if tilemap[j][i].position.x == position.x:
                x_cor = i      
                print(f"x_index {i}")
    
    return vector2(y_cor, x_cor)
            

def add_part(Index):
    Index = len(snake)

    part_index = len(snake)
    part = cube(snake[part_index-1].marker.position, RGB(0, 0, 255), spawnpoint(vector2(0, 0), snake[part_index-1].marker.thrust), snake[part_index-1].marker.thrust, Index)
    main_scene.append(part)
    snake.append(part)

def spawn_fruit():
    fruit_x = random.randrange(0, display_width, 50)
    fruit_y = random.randrange(0, display_heigth, 50)
    tile = give_tile_index_from_pos(vector2(fruit_x, fruit_y))
    if tilemap[tile.x][tile.y].taken != True:
       new_fruit = fruit(vector2(fruit_x, fruit_y), RGB(255, 0, 0), True)
       main_scene.append(new_fruit)
       fruits.append(new_fruit)
    else:
        spawn_fruit()
player = cube(vector2(0, 0), RGB(0, 0, 255), spawnpoint(vector2(0, 0), vector2(0, 0)), vector2(0, 0), Index )

snake = [player]
print(snake[0].position)
snake[0].position = vector2(350, 250)


main_scene = [player]
scenes = [
    main_scene
]
def refresh_scene():
    for i in range(0, len(main_scene)):
        try:

            if main_scene[i].show == False:
               main_scene.pop(i)
               break
        except AttributeError:
            pass
player.thrust = vector2(0, -1)

def instantiate_scene(scene):
    screen.fill((0, 0, 0))
    for i in range(0, len(scenes[scene-1])):
        scenes[scene-1][i].Instantiate()
pressed = False
fruit_spawn_rate = 2500
last_time = 0
fruits = []
print(type(fruits))
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and pressed == False:
            
            pressed = True
            if event.key == pygame.K_w and player.thrust.y != 1:
                player.thrust = vector2(0, -1)
            if event.key == pygame.K_s and player.thrust.y != -1:
                player.thrust = vector2(0, 1)
            if event.key == pygame.K_d and player.thrust.x != -1:
                player.thrust = vector2(1, 0)
            if event.key == pygame.K_a and player.thrust.x != 1:
                player.thrust = vector2(-1, 0)
            if event.key == pygame.K_SPACE:
                add_part(Index) 
        if event.type == pygame.WINDOWDISPLAYCHANGED:
            display_heigth = pygame.display.get_surface().get_height
            display_width = pygame.display.get_surface().get_width
      
        
    #-----------------------------#
    
    try:
        for i in range(len(fruits) - 1, -1, -1):
            if snake[0].rect.colliderect(fruits[i].rect):
                print("collided")
                fruits[i].show = False
                fruits.pop(i)
                add_part(Index)
                refresh_scene()
                
    except AttributeError:
        pass
    fruit_time_now = pygame.time.get_ticks()
    if fruit_time_now - last_time > fruit_spawn_rate:
        last_time = fruit_time_now
        spawn_fruit()
    if snake[0].position.x >= display_width or snake[0].position.x < 0:
        running = False 
    if snake[0].position.y >= display_heigth or snake[0].position.y < 0:
        running = False
    for i in range(0, len(snake)):
        snake[i].initiate_marker()
        if i == 0:
           snake[i].move()
        else:
            snake[i].move_body()
    
    #-----------------------------#
    instantiate_scene(1)
    pygame.display.flip()
    pressed = False
    clock.tick(4) 

pygame.quit()