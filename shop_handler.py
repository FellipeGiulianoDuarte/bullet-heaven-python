import json
import pygame
import time
from shotgun import Shotgun

class ShopHandler:

    def __init__(self, player, price_multiplier):
        self.player = player
        self.price_multiplier = price_multiplier

        self.potion_index = 1
        self.weapon_upgrade_level = 1
        self.shotgun_upgrade_level = 1
        self.player_speed_upgrade_level = 1
        self.player_max_health_upgrade_level = 1

        self.load_shop_prices()

        self.set_prices()

        self.gun_upgrade_limit = 3
        self.speed_upgrade_limit = 6
        self.health_upgrade_limit = 500
        self.shotgun_upgrade_limit = 4

    def load_shop_prices(self):
        # Load configurations from config.json
        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)

        # Extract values from the config file
        shop_prices = config_data["shop_prices"]
        self.POTION_COST = shop_prices["potion_cost"]
        self.NEW_WEAPON_COST = shop_prices["new_weapon_cost"]
        self.PLAYER_SPEED_COST = shop_prices["player_speed_cost"]
        self.PLAYER_MAX_HEALTH_COST = shop_prices["player_max_health_cost"]
        self.SHOTGUN_UPGRADE_COST = shop_prices["shotgun_upgrade_cost"]

    def set_prices(self):
        # Set prices for all items
        self.potion_cost = self.POTION_COST * self.price_multiplier * (self.player.max_health * 0.01)
        self.new_weapon_cost = self.NEW_WEAPON_COST * self.price_multiplier * self.weapon_upgrade_level
        self.shotgun_cost = self.SHOTGUN_UPGRADE_COST * self.price_multiplier * self.shotgun_upgrade_level
        self.player_speed_cost = self.PLAYER_SPEED_COST * self.price_multiplier * self.player_speed_upgrade_level
        self.player_max_health_cost = self.PLAYER_MAX_HEALTH_COST * self.price_multiplier * self.player_max_health_upgrade_level

    def handle_shop(self):
        time.sleep(0.1)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_1]:
            self.buy_health_potion()
        elif keys[pygame.K_2]:
            self.buy_new_weapon()
        elif keys[pygame.K_3]:
            self.buy_player_speed()
        elif keys[pygame.K_4]:
            self.buy_player_max_health()
        elif keys[pygame.K_5]:
            self.buy_shotgun_upgrade()

    def buy_health_potion(self):
        if self.player.money >= self.potion_cost and self.player.health < self.player.max_health:
            self.player.health += self.player.max_health * 0.1

            # Handle the life overflow
            if self.player.health > self.player.max_health:
                self.player.health = self.player.max_health

            self.player.money -= self.potion_cost
            self.potion_index += 1
            self.potion_cost = (
                self.POTION_COST
                * self.price_multiplier
                * (self.player.max_health * 0.01)
            )

    def buy_new_weapon(self):
        if (
            self.player.money >= self.new_weapon_cost
            and self.weapon_upgrade_level < self.gun_upgrade_limit
        ):
            self.player.gun = self.player.get_next_gun()
            self.player.gun_sprite.update_gun_type(self.player.gun)
            self.player.money -= self.new_weapon_cost
            self.weapon_upgrade_level += 1
            self.new_weapon_cost = (
                self.NEW_WEAPON_COST
                * self.price_multiplier
                * self.weapon_upgrade_level
            )

    def buy_player_speed(self):
        if (
            self.player.money >= self.player_speed_cost
            and self.player.max_speed <= self.speed_upgrade_limit
        ):
            self.player.max_speed += 1
            self.player.money -= self.player_speed_cost
            self.player_speed_upgrade_level += 1
            self.player_speed_cost = (
                self.PLAYER_SPEED_COST
                * self.price_multiplier
                * self.player_speed_upgrade_level
            )

    def buy_player_max_health(self):
        if (
            self.player.money >= self.player_max_health_cost
            and self.player.max_health < self.health_upgrade_limit
        ):
            self.player.max_health += 50
            self.player.health = self.player.max_health
            self.player.money -= self.player_max_health_cost
            self.player_max_health_upgrade_level += 1
            self.player_max_health_cost = (
                self.PLAYER_MAX_HEALTH_COST
                * self.price_multiplier
                * self.player_max_health_upgrade_level
            )
            self.potion_cost = (
                self.POTION_COST
                * self.price_multiplier
                * (self.player.max_health * 0.01)
            )

    def buy_shotgun_upgrade(self):
        if (
            self.player.money >= self.shotgun_cost
            and isinstance(self.player.gun, Shotgun)
            and self.shotgun_upgrade_level < self.shotgun_upgrade_limit
        ):
            if self.shotgun_upgrade_level == 1:
                self.player.gun = Shotgun(damage=40, fire_rate=3)
            elif self.shotgun_upgrade_level == 2:
                self.player.gun = Shotgun(damage=45, fire_rate=4, pellet_number=5, spread_angle=15)
            elif self.shotgun_upgrade_level == 3:
                self.player.gun = Shotgun(damage=50, fire_rate=5, pellet_number=6, spread_angle=10, lifespan=17)

            self.player.money -= self.shotgun_cost
            self.shotgun_upgrade_level += 1
            self.shotgun_cost = (
                self.SHOTGUN_UPGRADE_COST
                * self.price_multiplier
                * self.shotgun_upgrade_level
            )
