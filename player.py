import pygame
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