import math

from projectile import Projectile


class Gun():

    def __init__(self, name, damage, fire_rate, bullet_speed):
        self.name = name
        self.damage = damage
        self.fire_rate = fire_rate
        self.bullet_speed = bullet_speed
        self.time_since_last_shot = 0
        self.fire_delay = 1 / fire_rate

    def fire(self, player, direction_x, direction_y):
            # Check if enough time has passed since the last shot
            if self.time_since_last_shot >= self.fire_delay:
                orientation_angle = math.degrees(math.atan2(direction_y, direction_x))

                if self.name == 'Pistol' or self.name == 'Rifle':
                    gun_tip_x, gun_tip_y = player.gun_sprite.get_gun_tip()
                    projectile = Projectile(
                        gun_tip_x,
                        gun_tip_y,
                        direction_x,
                        direction_y,
                        self.bullet_speed,
                        orientation_angle,
                    )
                    self.time_since_last_shot = 0
                    return [projectile]
            else:
                return None