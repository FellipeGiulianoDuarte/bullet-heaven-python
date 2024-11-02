import math
import os
import pygame

class GunSprite(pygame.sprite.Sprite):

    def __init__(self, player, gun):
        super().__init__()
        self.player = player

        self.gun = gun
        self.load_gun_image()
        self.orientation_angle = 0

        self.orbit_radius = 30

    def load_gun_image(self):
            gun_image_path = os.path.join("sprites", f"{self.gun.name.lower()}.png")
            self.original_image = pygame.image.load(gun_image_path)

            self.image = self.original_image.copy()
            self.rect = self.image.get_rect()

    def update_gun_type(self, new_gun_type):
        self.gun = new_gun_type
        self.load_gun_image()
        self.update()

    def update(self):
        # Calculate the angle between the gun and the mouse position
        mouse_vector = pygame.math.Vector2(
            pygame.mouse.get_pos()[0] - self.player.rect.centerx,
            pygame.mouse.get_pos()[1] - self.player.rect.centery
        )
        self.orientation_angle = math.degrees(math.atan2(mouse_vector.y, mouse_vector.x))

        # Calculate the new position based on the orbit
        orbit_x = self.player.rect.centerx + self.orbit_radius * math.cos(math.radians(self.orientation_angle))
        orbit_y = self.player.rect.centery + self.orbit_radius * math.sin(math.radians(self.orientation_angle))

        self.rect.centerx = round(orbit_x)
        self.rect.centery = round(orbit_y)

        # Rotate the gun sprite towards the mouse
        self.image = pygame.transform.rotate(self.original_image, -self.orientation_angle)
        if 90 < self.orientation_angle <= 180 or -180 <= self.orientation_angle < -90:
            self.image = pygame.transform.rotate(self.original_image, -self.orientation_angle)
            self.image = pygame.transform.flip(pygame.transform.rotate(self.original_image, self.orientation_angle), False, True)
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))

    def get_gun_tip(self):
        gun_tip_x = self.rect.centerx + self.orbit_radius * math.cos(math.radians(self.orientation_angle))
        gun_tip_y = self.rect.centery + self.orbit_radius * math.sin(math.radians(self.orientation_angle))
        return round(gun_tip_x), round(gun_tip_y)
