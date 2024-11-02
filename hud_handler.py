import pygame
from shotgun import Shotgun


class HudHandler:

    def __init__(self, hud_positions):
        self.hud_positions = hud_positions

        self.wave_text_alpha = 255
        self.wave_fade_speed = 130

    def draw_dash_cooldown_bar(self, surface, cooldown_percentage):
        x, y = self.hud_positions["cooldown_bar"]
        dash_cooldown_bar_width = 150
        dash_cooldown_bar_height = 25
        bar_width = int(dash_cooldown_bar_width * (1 - cooldown_percentage))
        cooldown_rect = pygame.Rect(x, y, bar_width, dash_cooldown_bar_height)
        outline_rect = pygame.Rect(x, y, dash_cooldown_bar_width, dash_cooldown_bar_height)
        pygame.draw.rect(surface, (255, 202, 79), cooldown_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 2)

    def draw_health_bar(self, surface, player_health, player_max_health):
        x, y = self.hud_positions["health_bar"]
        bar_width = 150 + player_max_health / 2
        bar_height = 25
        outline_rect = pygame.Rect(x, y, bar_width, bar_height)
        filled_rect = pygame.Rect(x, y, bar_width * (player_health / player_max_health), bar_height)
        pygame.draw.rect(surface, (255, 0, 0), filled_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 2)

    def draw_money(self, surface, money):
        x, y = self.hud_positions["money"]
        font = pygame.font.Font(None, 36)
        text = font.render(f"Money: ${int(money)}", True, (0, 0, 0))
        surface.blit(text, (x, y))

    def draw_score(self, surface, score):
        x, y = self.hud_positions["score"]
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {int(score)}", True, (0, 0, 0))
        surface.blit(text, (x, y))

    def draw_wave(self, surface, wave):
        x, y = self.hud_positions["wave"]
        font = pygame.font.Font(None, 72)
        text = font.render(f"Wave {int(wave)}", True, (0, 0, 0))
        text.set_alpha(self.wave_text_alpha)
        surface.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
        frame_rate = 60.0
        self.wave_text_alpha -= self.wave_fade_speed / frame_rate
        self.wave_text_alpha = max(0, self.wave_text_alpha)

    def draw_paused(self, surface):
        x, y = self.hud_positions["paused"]
        pause_font = pygame.font.Font(None, 74)
        pause_text = pause_font.render("Paused", True, (0, 0, 0))
        surface.blit(pause_text, (x, y))

    def draw_shop_menu(self, surface, shop_handler):
        x, y = self.hud_positions["shop_menu"]
        font = pygame.font.Font(None, 36)
        shop_text = font.render("Shop Menu", True, (0, 0, 0))
        surface.blit(shop_text, (x - shop_text.get_width() // 2, y))

        HP = int(shop_handler.player.max_health * 0.1)
        potion_cost_text = font.render(f"Buy {HP}HP Potion: ${int(shop_handler.potion_cost)} (Press 1)", True, (0, 0, 0))
        new_weapon_cost_text = font.render(f"Buy New Weapon: ${int(shop_handler.new_weapon_cost)} (Press 2)", True, (0, 0, 0))
        p_speed_cost_text = font.render(f"Buy Player Speed: ${int(shop_handler.player_speed_cost)} (Press 3)", True, (0, 0, 0))
        p_max_health_cost_text = font.render(f"Buy Player Max health: ${int(shop_handler.player_max_health_cost)} (Press 4)", True, (0, 0, 0))

        # Verifies all maxed out upgrades
        if shop_handler.shotgun_upgrade_level == shop_handler.shotgun_upgrade_limit:
            shotgun_upgrade_text = font.render(f"Shotgun Upgrades: Maxed", True, (128, 128, 128))
            surface.blit(shotgun_upgrade_text, (x - shotgun_upgrade_text.get_width() // 2, y + 250))
        elif isinstance(shop_handler.player.gun, Shotgun) and shop_handler.weapon_upgrade_level == 3:
            shotgun_upgrade_text = font.render(f"Buy Shotgun Upgrade: ${int(shop_handler.shotgun_cost)} (Press 5)", True, (0, 0, 0))
            surface.blit(shotgun_upgrade_text, (x - shotgun_upgrade_text.get_width() // 2, y + 250))

        if shop_handler.weapon_upgrade_level == shop_handler.gun_upgrade_limit:
            new_weapon_cost_text = font.render(f"New Weapon: Maxed", True, (128, 128, 128))

        if shop_handler.player_speed_upgrade_level == shop_handler.speed_upgrade_limit:
            p_speed_cost_text = font.render(f"Player Speed: Maxed", True, (128, 128, 128))

        if shop_handler.player.max_health == shop_handler.health_upgrade_limit:
            p_max_health_cost_text = font.render(f"Player Max health: Maxed", True, (128, 128, 128))

        # Blit all costs on the screen
        surface.blit(potion_cost_text, (x - potion_cost_text.get_width() // 2, y + 50))
        surface.blit(new_weapon_cost_text, (x - new_weapon_cost_text.get_width() // 2, y + 100))
        surface.blit(p_speed_cost_text, (x - p_speed_cost_text.get_width() // 2, y + 150))
        surface.blit(p_max_health_cost_text, (x - p_max_health_cost_text.get_width() // 2, y + 200))
