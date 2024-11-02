import json
import os
import pygame
from hud_handler import HudHandler
from pistol import Pistol
from player import Player
from mob import Mob
from shop_handler import ShopHandler


class GameScreen():

    def __init__(self, difficulty):
        # Load configuration file
        self.load_game_screen_config()

        # Instance difficulty, gun and player
        self.difficulty = difficulty
        self.gun = Pistol()
        self.player = Player(self.gun)

        # Difficulty changes
        self.set_game_difficulty(difficulty)

        # Mob variables
        self.time_since_last_mob_creation = 0
        self.wave_number = 0

        # Pause
        self.paused = False

        # Set shop config
        self.show_shop_menu = False
        self.shop_handler = ShopHandler(self.player, self.price_multiplier)

        # Set the HUD positions
        self.hud_handler = HudHandler(self.hud_positions)

    def run(self):
        pygame.init()

        screen = pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_caption("Placeholder Title")
        clock = pygame.time.Clock()
        frame_rate = 60

        all_sprites = pygame.sprite.Group()
        projectiles = pygame.sprite.Group()
        mobs = pygame.sprite.Group()

        all_sprites.add(self.player)
        all_sprites.add(self.player.gun_sprite)
        background_image = pygame.image.load(os.path.join("sprites", "background_image.jpg"))

        while self.player.is_alive:
            for event in pygame.event.get():
                self.handle_input(event)

            screen.blit(background_image, (0, 0))

            if self.show_shop_menu and not self.paused:
                self.draw_elements(screen, all_sprites)
                self.shop_handler.handle_shop()
            elif not self.paused:
                if self.player.shooting:
                    self.handle_shooting(projectiles, all_sprites)

                self.update_game_state(self.player, mobs, projectiles, clock)

                self.handle_collisions(self.player, mobs, projectiles)

                self.create_mobs(mobs, all_sprites)

                self.draw_elements(screen, all_sprites)

            else:
                self.draw_elements(screen, all_sprites)
                self.hud_handler.draw_paused(screen)

            pygame.display.flip()
            clock.tick(frame_rate)

        pygame.quit()

    def load_game_screen_config(self):
        # Load configurations from config.json
        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)

        # Extract values from the config file
        self.SCREEN_SIZE = tuple(config_data["screen_size"])
        self.DASH_COOLDOWN = config_data["dash_cooldown"]
        self.mobs = config_data["mobs"]
        self.player_attributes = config_data["player"]
        self.mob_attributes = config_data["mob_attributes"]
        self.hud_positions = config_data["hud_positions"]

    def set_game_difficulty(self, difficulty):
        # Gets difficulty modifiers from the config dictionary
        difficulty_config = self.mobs[difficulty]
        self.mobs_to_create = difficulty_config["to_create"]
        self.MOB_CREATION_INTERVAL = difficulty_config["creation_interval"]
        self.price_multiplier = difficulty_config["price_multiplier"]
        self.max_mob_spawn = difficulty_config["max_spawn"]

    def create_mob(self, health, speed, damage):
        # Create mob based on game difficulty
        if self.difficulty == 'Easy':
            return Mob(health, speed, 50, 10, damage, 100)
        elif self.difficulty == 'Medium':
            return Mob((damage * 2), (speed * 1.1), 50, 10, (damage * 1.5), 150)
        elif self.difficulty == 'Hard':
            return Mob((damage * 3), (speed * 1.2), 50, 10, (damage * 2), 200)

    def create_mobs(self, mobs, all_sprites):
        # Create mobs based on game difficulty and wave number
        if self.time_since_last_mob_creation >= self.MOB_CREATION_INTERVAL:
            self.wave_number += 1
            self.mobs_to_create += 1

            mob_health = 5 + self.wave_number * 2
            mob_speed = 1.1 + self.wave_number * 0.05
            if mob_speed >= 2:
                mob_speed = 2
            mob_damage = 5 + self.wave_number * 0.5

            num_mobs_to_spawn = min(int(self.mobs_to_create), self.max_mob_spawn)
            for _ in range(num_mobs_to_spawn):
                mob = self.create_mob(mob_health, mob_speed, mob_damage)
                mobs.add(mob)
                all_sprites.add(mob)

            self.hud_handler.wave_text_alpha = 255
            self.time_since_last_mob_creation = 0

    def handle_input(self, event):
        # Handle user input events
        if event.type == pygame.QUIT:
            self.player.is_alive = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.player.shooting = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.player.shooting = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.show_shop_menu:
                    self.show_shop_menu = False
                elif not self.paused:
                    self.paused = True
                elif self.paused and not self.show_shop_menu:
                    self.paused = False
            elif event.key == pygame.K_v and not self.paused:
                self.show_shop_menu = not self.show_shop_menu
            # TODO: Remove cheat
            elif event.key == pygame.K_c:
                self.player.money = 999999

    def handle_shooting(self, projectiles, all_sprites):
        mouse_vector = pygame.math.Vector2(
            pygame.mouse.get_pos()[0] - self.player.rect.centerx,
            pygame.mouse.get_pos()[1] - self.player.rect.centery
        )
        if mouse_vector.x != 0 or mouse_vector.y != 0:
            normalized_vector = mouse_vector.normalize()
            direction_x, direction_y = normalized_vector.x, normalized_vector.y

            projectile = self.player.fire_gun(direction_x, direction_y)

            if projectile:
                projectiles.add(projectile)
                all_sprites.add(projectile)
                self.player.gun.time_since_last_shot = 0

    def update_game_state(self, player, mobs, projectiles, clock):
        # Update game state, player, mobs, projectiles, etc.
        player.update()
        mobs.update(player)
        projectiles.update()

        self.player.gun.time_since_last_shot += clock.get_time() / 1000.0
        self.time_since_last_mob_creation += clock.get_time()

    def handle_collisions(self, player, mobs, projectiles):
        # Check for collisions between projectiles, mobs, and player
        for projectile in projectiles:
            mobs_hit = pygame.sprite.spritecollide(projectile, mobs, False)

            for mob in mobs_hit:
                mob.receive_damage(player.gun.damage)
                projectile.kill()
                if not mob.is_alive:
                    player.money += mob.reward
                    player.score += mob.score
                break

        mobs_who_collided = pygame.sprite.spritecollide(player, mobs, False)
        if mobs_who_collided:
            mob = mobs_who_collided[0]
            player.receive_damage(mob.damage)

    def draw_elements(self, screen, all_sprites):
        # Draw sprites, HUD, and other elements on the screen
        all_sprites.draw(screen)
        self.hud_handler.draw_health_bar(screen, self.player.health, self.player.max_health)
        self.hud_handler.draw_dash_cooldown_bar(screen, max(0, min(1, self.player.dash_cooldown / self.DASH_COOLDOWN)))
        self.hud_handler.draw_money(screen, self.player.money)
        self.hud_handler.draw_score(screen, self.player.score)
        if self.wave_number > 0:
            self.hud_handler.draw_wave(screen, self.wave_number)
        if self.show_shop_menu:
            self.hud_handler.draw_shop_menu(screen, self.shop_handler)