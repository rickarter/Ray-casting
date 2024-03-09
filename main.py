import pygame
import math
from player import Player
from vector import Vector2D


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

window_width = 640
window_height = 480


def draw_map(screen, map):
    cell_size = 35
    # Colors
    wallColor = (43, 82, 121)
    floorColor = (98, 163, 176)
    
    [pygame.draw.rect(screen, wallColor if map[y][x] == 1 else floorColor, (x * cell_size, y * cell_size, x + cell_size, y + cell_size)) 
        for y in range(0, len(map)) 
        for x in range(0, len(map[0]))]

def draw_player(screen, player, width, height):
    new_x = int(player.position.x / map_width * width)
    new_y = int(player.position.y / map_height * height)
    
    # Draw the player
    pygame.draw.circle(screen, (255, 255, 255), (new_x, new_y), 3)

    # Drawing raycasts
    step = player.FOV / window_width
    current_angle = player.direction - player.FOV  / 2
    for i in range(0, window_width):
        draw, line_length, draw_vertical = player.cast_ray(
            current_angle, world_map, CELLSIZE)
        line_length = line_length / map_width * width
        if draw:
            pygame.draw.line(screen, (24, 224, 134), (new_x, new_y), (new_x + math.cos(
                current_angle)*line_length, new_y + math.sin(current_angle)*line_length))
        current_angle += step



def render(screen, player):
    half_cell = CELLSIZE / 2
    half_height = window_height / 2
    d = half_cell / math.tan(player.FOV/2)
    initial_color = (0, 159, 66)
    final_color = (0, 151, 66)
    
    current_angle = player.direction - player.FOV/2
    step = player.FOV/(window_width-1)
    for i in range(0, window_width):
        draw, length, draw_horizontal = player.cast_ray(
            current_angle, world_map, CELLSIZE)
        h2 = (length/d) * half_cell
        if h2 != 0:
            line_ratio = half_cell/h2
            half_line_length = half_height * line_ratio
            if draw:
                color = final_color
                if draw_horizontal:
                    color = initial_color
                pygame.draw.line(screen, color, (i, half_height +
                                 half_line_length), (i, half_height-half_line_length))
            current_angle += step


def main():
    fps = 60
    clock = pygame.time.Clock()
    run = True

    # Init player
    player_position = Vector2D(map_width/2, map_height/2)
    player = Player(player_position, 80 * math.pi/180, 0, 100, 5)
    
    # Init window
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("ray-casting")

    # Main loop
    while run:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        delta_time = clock.tick(fps)/1000

        window.fill((0, 0, 0))

        render(window, player)
        draw_map(window, world_map)
        draw_player(window, player, len(world_map)
                    * 35, len(world_map[0])*35)

        player.move_and_rotate(delta_time, pygame.key.get_pressed())
        pygame.display.update()


if __name__ == "__main__":
    main()
