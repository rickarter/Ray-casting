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
        direction_vector.SetAngleInRads(self.direction)
        if keys[pygame.K_w]:
            self.position += direction_vector * self.movement_speed * delta_time
        if keys[pygame.K_s]:
            self.position -= direction_vector * self.movement_speed * delta_time
        if keys[pygame.K_a]:
            self.direction -= self.rotation_speed * delta_time
        if keys[pygame.K_d]:
            self.direction += self.rotation_speed * delta_time

        if keys[pygame.K_u]:
            self.FOV += 1*delta_time
        if keys[pygame.K_j]:
            self.FOV -= 1*delta_time

    def clamp_angle(self, angle):
        new_angle = 0
        if angle >= 0:
            new_angle = angle - angle//(2*math.pi) * (2*math.pi)
        else:
            pi2 = math.pi * 2
            new_angle = pi2 + ((abs(angle)//pi2)*pi2 + angle)

        return new_angle

    def cast_ray(self, direction, map, CELLSIZE, screen):
        angle = self.clamp_angle(direction)

        looks_up = not (0 < angle < math.pi)
        looks_right = not (math.pi/2 < angle < 3*math.pi/2)

        ROV = 10

        tan = math.tan(direction)

        # Check horizontal intersection
        has_horizontal_intersection = False
        horizontal_distance = 0

        if tan != 0:
            # Projection of the vector to the nearest horizontal intersection
            yn = -(self.position.y - (self.position.y // CELLSIZE) * CELLSIZE)
            if not looks_up:
                yn = CELLSIZE + yn
            xn = yn / tan

            # Projection of the step vector
            ys = -CELLSIZE
            if not looks_up:
                ys = -ys
            xs = ys / tan

            current_x = self.position.x + xn
            current_y = self.position.y + yn
            for i in range(0, ROV+1):
                ix = int(current_x // CELLSIZE)
                iy = int(current_y // CELLSIZE)-1

                if not looks_up:
                    iy += 1

                if ix < 0 or iy < 0 or ix > len(map[0])-1 or iy > len(map)-1:
                    break

                if map[iy][ix] == 1:
                    has_horizontal_intersection = True
                    horizontal_distance = (
                        Vector2D(current_x, current_y) - self.position).Magnitude()
                    break

                current_x += xs
                current_y += ys

        # Check vertical intersection
        has_vertical_intersection = False
        vertical_distance = 0
        if tan != 1:
            # Projection of the vector to the nearest vertical intersection
            xn = -(self.position.x - (self.position.x // CELLSIZE) * CELLSIZE)
            if looks_right:
                xn = CELLSIZE + xn
            yn = tan * xn

            # Projection of the step vector
            xs = -CELLSIZE
            if looks_right:
                xs = -xs

            ys = tan * xs

            current_x = self.position.x + xn
            current_y = self.position.y + yn

            for i in range(0, ROV+1):
                ix = int(current_x // CELLSIZE)-1
                iy = int(current_y // CELLSIZE)

                if looks_right:
                    ix += 1

                if ix < 0 or iy < 0 or ix > len(map[0])-1 or iy > len(map)-1:
                    break

                if map[iy][ix] == 1:
                    has_vertical_intersection = True
                    vertical_distance = (
                        Vector2D(current_x, current_y) - self.position).Magnitude()
                    break

                current_x += xs
                current_y += ys

        distance = 0
        is_horizontal_the_nearest = False
        if has_horizontal_intersection and not has_vertical_intersection:
            distance = horizontal_distance
            is_horizontal_the_nearest = True
        elif has_vertical_intersection and not has_horizontal_intersection:
            distance = vertical_distance
        else:
            distance = min(horizontal_distance, vertical_distance)
            if horizontal_distance < vertical_distance:
                is_horizontal_the_nearest = True

        # Removing destortion
        beta = abs(self.clamp_angle(self.direction)-angle)
        if looks_up:
            beta = math.pi*2 - abs(self.clamp_angle(self.direction)-angle)
        distance = distance * math.cos(beta)
        return has_horizontal_intersection or has_vertical_intersection, distance, is_horizontal_the_nearest
