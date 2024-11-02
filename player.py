import json
import os
import pygame
from gun_sprite import GunSprite

from pistol import Pistol
from rifle import Rifle
from shotgun import Shotgun


class Player(pygame.sprite.Sprite):

    def __init__(self, gun):
        super().__init__()
        # Load configs from file
        self.load_player_config()

        # Player sprite
        self.image = pygame.Surface((self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.rect = self.image.get_rect(center=(self.SCREEN_SIZE[0] // 2, self.SCREEN_SIZE[1] // 2))
        self.image = pygame.image.load(os.path.join("sprites", "player.png"))

        # Flip sprite variables
        self.facing_right_image = self.image
        self.facing_left_image = pygame.transform.flip(self.image, True, False)
        self.facing_right = True

        # Resize the image to match the player size
        self.image = pygame.transform.scale(self.image, (self.PLAYER_SIZE, self.PLAYER_SIZE))

        # Player stats
        self.speed_x = 0
        self.speed_y = 0
        self.is_alive = True
        self.max_speed = 2

        # Dash logic
        self.dash_cooldown = 0
        self.is_dashing = False
        self.dash_frames = 0
        self.dash_distance = 30

        # Gun logic
        self.gun = gun
        self.shooting = False

        # Immunity frames logic
        self.immune = False
        self.immunity_timer = 0
        self.blink_timer = 0

        # Create gun sprite
        self.gun_sprite = GunSprite(self, self.gun)

    def load_player_config(self):
        # Load configurations from config.json
        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)

        # Extract values from the config file
        player_config = config_data["player"]

        # Draw on the screen
        self.SCREEN_SIZE = player_config["screen_size"]
        self.PLAYER_SIZE = player_config["player_size"]

        # Health
        self.health = player_config["health"]
        self.max_health = player_config["max_health"]

        # Money and Score
        self.money = player_config["money"]
        self.score = player_config["score"]

        # Player Physics
        self.PLAYER_ACCELERATION = player_config["acceleration"]
        self.PLAYER_FRICTION = player_config["friction"]

        # Immunity
        self.IMMUNITY_DURATION = player_config["immunity_duration"]
        self.BLINK_INTERVAL = player_config["blink_interval"]

    def dash(self):
        if not self.is_dashing and (self.speed_x != 0 or self.speed_y != 0):
            normalized_vector = pygame.math.Vector2(self.speed_x, self.speed_y).normalize()
            self.dash_frames = 10
            self.dash_vector = normalized_vector
            self.is_dashing = True

    def update(self):
        keys = pygame.key.get_pressed()

        # Updates immunity timer
        if self.immune:
            self.immunity_timer -= 1
            self.blink_timer += 1
            if self.immunity_timer <= 0:
                self.immune = False

        # Blinks when immune
        if self.immune and self.blink_timer % self.BLINK_INTERVAL == 0:
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)

        # Accelerates
        if keys[pygame.K_a] and self.rect.left > 0:
            self.speed_x -= self.PLAYER_ACCELERATION
            self.facing_right = False
        if keys[pygame.K_d] and self.rect.right < self.SCREEN_SIZE[0]:
            self.speed_x += self.PLAYER_ACCELERATION
            self.facing_right = True
        if keys[pygame.K_w] and self.rect.top > 0:
            self.speed_y -= self.PLAYER_ACCELERATION
        if keys[pygame.K_s] and self.rect.bottom < self.SCREEN_SIZE[1]:
            self.speed_y += self.PLAYER_ACCELERATION

        # Dashes
        if keys[pygame.K_SPACE] and self.dash_cooldown == 0:
            self.dash()

        # Dash cooldown logic
        if self.is_dashing:
            self.dash_frames -= 1
            if self.dash_frames > 0:
                # Interpolate the player's position during the dash
                interpolation_factor = self.dash_frames / 10.0
                self.rect.x += self.dash_distance * self.dash_vector.x * interpolation_factor
                self.rect.y += self.dash_distance * self.dash_vector.y * interpolation_factor
            else:
                self.is_dashing = False
                self.dash_cooldown = 300  # Set the cooldown duration (in frames)
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        # Apply friction
        self.speed_x *= 1 - self.PLAYER_FRICTION
        self.speed_y *= 1 - self.PLAYER_FRICTION

        # Limit max speed
        self.speed_x = max(-self.max_speed, min(self.max_speed, self.speed_x))
        self.speed_y = max(-self.max_speed, min(self.max_speed, self.speed_y))

        # Update player position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ensure player stays within screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.SCREEN_SIZE[0]:
            self.rect.right = self.SCREEN_SIZE[0]

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > self.SCREEN_SIZE[1]:
            self.rect.bottom = self.SCREEN_SIZE[1]

        # Updates gun sprite
        self.gun_sprite.update()

        # Updates player sprite
        if self.facing_right:
            self.image = self.facing_right_image
        else:
            self.image = self.facing_left_image

    def receive_damage(self, damage):
        if not self.immune:
            self.health -= damage
            if self.health <= 0:
                self.is_alive = False
                return

            self.immune = True
            frame_rate = 60
            self.immunity_timer = self.IMMUNITY_DURATION * frame_rate

    def fire_gun(self, direction_x, direction_y):
        return self.gun.fire(self, direction_x, direction_y)

    def get_next_gun(self):
        if isinstance(self.gun, Pistol):
            return Rifle()
        elif isinstance(self.gun, Rifle):
            return Shotgun()