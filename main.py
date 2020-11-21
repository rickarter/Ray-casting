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
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
            ]
CELLSIZE = 64
map_width = len(world_map[0]) * CELLSIZE
map_height = len(world_map) * CELLSIZE

#Init window
window_width = 800#320
window_height = 800#180
window = pygame.display.set_mode((window_width, window_height))

#Init plaeyer
player_position = Vector2D(map_width/2, map_height/2)
player = Player(player_position, 60*math.pi/180, 0, 100, 10);

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
    pygame.draw.line(screen, (255, 255, 255), (new_x, new_y), (new_x + math.cos(player.direction)*line_length, new_y + math.sin(player.direction)*line_length))

#Main loop
fps = 60
clock = pygame.time.Clock()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    delta_time = clock.tick(fps)/1000
    
    draw_map(window, world_map)  
    draw_player(window, player, len(world_map)*35, len(world_map[0])*35);  

    player.move_and_rotate(delta_time, pygame.key.get_pressed())   
    pygame.display.update()
