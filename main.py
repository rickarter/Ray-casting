import pygame
import math
from player import Player
from vector import Vector2D

# Colors
wallColor  = (43, 82, 121)
floorColor = (98, 163, 176)

# Init map and its size
world_map = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1]
            ]

CELLSIZE = 64
map_width = len(world_map[0]) * CELLSIZE
map_height = len(world_map) * CELLSIZE

#Init window
window_width = 320*2#175
window_height = 180*2#175
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("ray-casting")

#Init plaeyer
player_position = Vector2D(map_width/2, map_height/2)
player = Player(player_position, 80*math.pi/180, 0, 100, 5)

def draw_map(screen, map):
    cellSize = 35 

    for y in range(0, len(map)):
        for x in range(0, len(map[0])):
            # print(str(y) + str(x))
            color = floorColor
            if map[y][x] == 1:
                color = wallColor

            current_x = x
            current_y = y
            pygame.draw.rect(screen, color, (current_x*cellSize, current_y*cellSize, current_x+cellSize, current_y+cellSize))

def draw_player(screen, player, width, height):
    new_x = int(player.position.x / map_width * width)
    new_y = int(player.position.y / map_height * height)

    line_length = 10;
    pygame.draw.circle(screen, (255, 255, 255),(new_x, new_y), 3);
    # pygame.draw.line(screen, (255, 255, 255), (new_x, new_y), (new_x + math.cos(player.direction)*line_length, new_y + math.sin(player.direction)*line_length))
    pygame.draw.line(screen, (255, 255, 255), (new_x, new_y), (new_x + math.cos(player.direction+player.FOV/2)*line_length, new_y + math.sin(player.direction+player.FOV/2)*line_length))
    pygame.draw.line(screen, (255, 255, 255), (new_x, new_y), (new_x + math.cos(player.direction-player.FOV/2)*line_length, new_y + math.sin(player.direction-player.FOV/2)*line_length))

    # Drawing lines
    step = player.FOV / window_width
    current_angle = player.direction-player.FOV/2
    for i in range(0, window_width):
        draw, line_length, draw_vertical = player.cast_ray_2(current_angle, world_map, CELLSIZE, screen)
        line_length = line_length / map_width * width
        if draw:
            pygame.draw.line(screen, (24, 224, 134), (new_x, new_y), (new_x + math.cos(current_angle)*line_length, new_y + math.sin(current_angle)*line_length))
        current_angle += step
    

    '''draw, line_length = player.cast_ray_2(player.direction, world_map, CELLSIZE, screen)
    line_length = line_length / map_width * width
    if draw:
        pygame.draw.line(screen, (0, 255, 0), (new_x, new_y), (new_x + math.cos(player.direction)*line_length, new_y + math.sin(player.direction)*line_length))'''

def get_interpolated_color(initial_color, final_color, t):
    if t > 1:
        t = 1
    red = initial_color[0] + (final_color[0]-initial_color[0])*t
    green = initial_color[1] + (final_color[1]-initial_color[1])*t
    blue = initial_color[2] + (final_color[2]-initial_color[2])*t
    new_color = (red, green, blue)
    return new_color

half_cell = CELLSIZE/2
half_height = window_height/2
d = half_cell/math.tan(player.FOV/2)
initial_color = (0, 159, 66)#(24, 224, 134)#(248, 12, 254)
final_color = (0, 151, 66)#(121, 0, 156)
max_length = CELLSIZE * 2

def render(screen, player, map):
    current_angle = player.direction - player.FOV/2
    step = player.FOV/(window_width-1)
    for i in range(0, window_width):
        draw, length, draw_horizontal = player.cast_ray_2(current_angle, world_map, CELLSIZE, screen)
        h2 = (length/d) * half_cell
        if h2 != 0:
            line_ratio = half_cell/h2
            half_line_length = half_height * line_ratio
            if draw:
                # color = get_interpolated_color(initial_color, final_color, length/max_length)
                color = final_color
                if draw_horizontal:
                    color = initial_color
                pygame.draw.line(screen, color, (i, half_height+half_line_length), (i, half_height-half_line_length))
            current_angle += step
      
#Main loop
fps = 60
clock = pygame.time.Clock()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    delta_time = clock.tick(fps)/1000

    window.fill((0,0,0))    
    
    render(window, player, world_map)
    draw_map(window, world_map)  
    draw_player(window, player, len(world_map)*35, len(world_map[0])*35);  

    player.move_and_rotate(delta_time, pygame.key.get_pressed())   
    pygame.display.update()