import math
from gun import Gun
from projectile import Projectile


class Shotgun(Gun):

    def __init__(self, damage=35, fire_rate=2, pellet_number=3, spread_angle=20, lifespan=12):
        super().__init__('Shotgun', damage, fire_rate, 20)
        self.pellet_number = pellet_number
        self.spread_angle = spread_angle
        self.lifespan = lifespan

    def fire(self, player, direction_x, direction_y):
        # Check if enough time has passed since the last shot
        if self.time_since_last_shot >= self.fire_delay:
            orientation_angle = math.degrees(math.atan2(direction_y, direction_x))
            pellet_number = self.pellet_number
            spread_angle = self.spread_angle
            projectiles = []

            for i in range(pellet_number):
                spread = (i - (pellet_number - 1) / 2) * spread_angle
                orientation = orientation_angle + spread
                orientation_radians = math.radians(orientation)
                direction_x_shot = math.cos(orientation_radians)
                direction_y_shot = math.sin(orientation_radians)
                projectile = Projectile(
                    player.rect.centerx,
                    player.rect.centery,
                    direction_x_shot,
                    direction_y_shot,
                    self.bullet_speed,
                    orientation,
                    self.lifespan,
                )
                projectiles.append(projectile)

            self.time_since_last_shot = 0
            return projectiles
        else:
            return None