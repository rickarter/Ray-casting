import pygame
import math
from vector import Vector2D

class Player:
    def __init__(self, position, FOV, direction, movement_speed, rotation_speed):
        self.position = position
        self.FOV = FOV
        self.direction = direction
        self.movement_speed = movement_speed
        self.rotation_speed = rotation_speed

    def move_and_rotate(self, delta_time, keys):
        direction_vector = Vector2D(1, 0)
        direction_vector.SetAngleInRads(self.direction);
        if keys[pygame.K_w]:
            self.position += direction_vector * self.movement_speed * delta_time
        if keys[pygame.K_s]:
            self.position -= direction_vector * self.movement_speed * delta_time
        if keys[pygame.K_a]:
            self.direction -= self.rotation_speed * delta_time
        if keys[pygame.K_d]:
            self.direction += self.rotation_speed * delta_time

    def clamp_angle(self, angle):
        if angle < 0:
            angle = -angle
            if angle < math.pi:
                angle = math.pi * 2 - angle
        if angle > math.pi * 2:
            angle = angle % (math.pi * 2)
        return angle

    def cast_ray(self, direction, map, cellSize):
        angle = self.clamp_angle(direction)

        looks_right = not (math.pi/2 < angle < 3*math.pi/2)
        looks_up = (math.pi > angle > 0)

        ROV = 10

        is_only_horizontal = angle == math.pi/2 or angle == 3 * math.pi / 2
        is_only_vertical = angle == math.pi or angle == 0

        # Check horizontal intersections
        has_horizontal_intersection = False  
        distance_to_horizontal_intersection = 0

        xa = 0
        if math.tan(angle) != 0:
            xa = cellSize / math.tan(angle)
        ya = cellSize
        
        if not looks_right:
            xa = -xa
        if looks_up:
            ya = -ya

        yo = -(self.position.y - (self.position.y // cellSize) * cellSize)
        if not looks_up:
            yo = cellSize + yo

        xo = 0
        if math.tan(angle) != 0:
            xo = abs(yo) / math.tan(angle)
        if not looks_right:
            xo = -xo

        current_x = self.position.x + xo
        current_y = self.position.y + yo

        if not is_only_vertical:
            for i in range(0, ROV+1):
                ix = int(current_x // cellSize)
                iy = int((current_y // cellSize) - 1)
                if not looks_up:
                    iy += 1

                if ix < 0 or iy < 0 or ix > len(map[0])-1 or iy > len(map)-1:
                    break

                if map[iy][ix] == 1:
                    has_horizontal_intersection = True
                    distance_to_horizontal_intersection = (Vector2D(current_x, current_y) - self.position).Magnitude()
                    break

                current_x += xa
                current_y += ya

        # Check vertical intersections
        has_vertical_intersection = False
        distance_to_vertical_intersection = 0
        xa = cellSize
        ya = math.tan(angle) * cellSize

        if looks_up:
            ya = -ya
        if not looks_right:
            xa = -xa

        xo = -(self.position.x - (self.position.x // cellSize) * cellSize)
        if looks_right: 
            xo = cellSize + xo

        yo = math.tan(angle) * abs(xo)
        if not looks_up:
            yo = -yo

        current_x = self.position.x + xo
        current_y = self.position.y + yo

        if not is_only_horizontal:
            for i in range(0, ROV+1):
                ix = int(current_x // cellSize)
                iy = int(current_y // cellSize)
                if not looks_right:
                    ix -= 1

                if ix < 0 or iy < 0 or ix > len(map[0])-1 or iy > len(map)-1:
                    break

                if map[iy][ix] == 1:
                    has_vertical_intersection = True
                    distance_to_vertical_intersection = (Vector2D(current_x, current_y) - self.position).Magnitude()
                    break

                current_x += xa
                current_y += ya

        # print('hor: ' + str(has_horizontal_intersection) + ' ' + str(distance_to_horizontal_intersection))
        # print('ver: ' + str(has_vertical_intersection) + ' ' + str(distance_to_vertical_intersection))

        # Return values
        distance = 0
        if has_horizontal_intersection and has_vertical_intersection:
            distance = min(distance_to_vertical_intersection, distance_to_horizontal_intersection)
        elif has_horizontal_intersection and not has_vertical_intersection:
            distance = distance_to_horizontal_intersection
        elif not has_horizontal_intersection and has_vertical_intersection:
            distance = distance_to_vertical_intersection

        return has_horizontal_intersection or has_vertical_intersection, distance