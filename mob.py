import math
import pygame
import random
import os


class Mob(pygame.sprite.Sprite):
    SCREEN_SIZE = (1280, 720)

    def __init__(self, health, speed, size, reward, damage, score):
        super().__init__()
        self.size = size
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(center=(self.get_random_spawn()))
        self.image = pygame.image.load(os.path.join("sprites", "mob.png"))

        # Resize the image to match the mob size
        self.image = pygame.transform.scale(self.image, (size, size))

        self.health = health
        self.speed = speed
        self.is_alive = True

        self.reward = reward
        self.damage = damage
        self.score = score

    def update(self, player):
        # Move towards the player
        distance_to_player_x = player.rect.x - self.rect.x
        distance_to_player_y = player.rect.y - self.rect.y
        if distance_to_player_x != 0 or distance_to_player_y != 0:
            direction = pygame.math.Vector2(distance_to_player_x, distance_to_player_y).normalize()
            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed

    def receive_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
            self.kill()
            return

    def get_random_spawn(self):
        random_edge = random.choice(['top', 'bottom', 'left', 'right'])

        if random_edge == 'top':
            return [random.randint(0, self.SCREEN_SIZE[0]), -self.size]
        elif random_edge == 'bottom':
            return [random.randint(0, self.SCREEN_SIZE[0]), self.SCREEN_SIZE[1] + self.size]
        elif random_edge == 'left':
            return [-self.size, random.randint(0, self.SCREEN_SIZE[1])]
        elif random_edge == 'right':
            return [self.SCREEN_SIZE[0] + self.size, random.randint(0, self.SCREEN_SIZE[1])]

    def calculate_angle(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        return math.atan2(dy, dx)

    def calculate_distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
