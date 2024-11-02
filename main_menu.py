import pygame
from game_screen import GameScreen


class MainMenu:
    BACKGROUND_COLOR = (54, 224, 91)
    SCREEN_SIZE = (800, 650)

    def __init__(self):
        self.selected_difficulty = None

    def display_menu(self):
        pygame.init()

        # Set up the game window
        screen = pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_caption("Placeholder Title")

        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 36)

        # Define options for difficulty
        difficulty_options = ['Easy', 'Medium', 'Hard']

        # Initialize selected index for difficulty
        selected_difficulty_index = 0

        while True:
            # Fill the screen with the background color
            screen.fill(self.BACKGROUND_COLOR)

            # Render and display title text
            title_text = font.render("Placeholder Title", True, (255, 255, 255))
            screen.blit(title_text, (self.SCREEN_SIZE[0] // 2 - title_text.get_width() // 2, 50))

            # Render and display difficulty options
            difficulty_text = font.render(f"Difficulty: {difficulty_options[selected_difficulty_index]}", True, (255, 255, 255))
            difficulty_helper = font.render(f"Change with: A/D", True, (255, 255, 255))
            screen.blit(difficulty_text, (self.SCREEN_SIZE[0] // 2 - difficulty_text.get_width() // 2, 200))
            screen.blit(difficulty_helper, (self.SCREEN_SIZE[0] // 2 - difficulty_helper.get_width() // 2, 230))

            # Render and display confirmation text
            confirm_text = font.render(f"Press SPACE to start", True, (255, 255, 255))
            screen.blit(confirm_text, (self.SCREEN_SIZE[0] // 2 - confirm_text.get_width() // 2, 370))

            # Render and display controller instructions
            controller_helper_movement = font.render(f"Movement: W/A/S/D", True, (255, 255, 255))
            controller_helper_shoot = font.render(f"Shoot: Left click", True, (255, 255, 255))
            controller_helper_dash = font.render(f"Dash: SPACE", True, (255, 255, 255))
            controller_helper_shop = font.render(f"Shop: V", True, (255, 255, 255))
            controller_helper_pause = font.render(f"Pause: ESC", True, (255, 255, 255))
            screen.blit(controller_helper_movement, (self.SCREEN_SIZE[0] // 2 - controller_helper_movement.get_width() // 2, 460))
            screen.blit(controller_helper_shoot, (self.SCREEN_SIZE[0] // 2 - controller_helper_shoot.get_width() // 2, 490))
            screen.blit(controller_helper_dash, (self.SCREEN_SIZE[0] // 2 - controller_helper_dash.get_width() // 2, 520))
            screen.blit(controller_helper_shop, (self.SCREEN_SIZE[0] // 2 - controller_helper_shop.get_width() // 2, 550))
            screen.blit(controller_helper_pause, (self.SCREEN_SIZE[0] // 2 - controller_helper_pause.get_width() // 2, 580))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    # Handle key presses
                    if event.key == pygame.K_a:
                        selected_difficulty_index = (selected_difficulty_index - 1) % len(difficulty_options)
                    elif event.key == pygame.K_d:
                        selected_difficulty_index = (selected_difficulty_index + 1) % len(difficulty_options)
                    elif event.key == pygame.K_SPACE:
                        # Set selected difficulty and exit the loop
                        self.selected_difficulty = difficulty_options[selected_difficulty_index]
                        pygame.quit()
                        return

            clock.tick(10)

# Create an instance of MainMenu and display the menu
main_menu = MainMenu()
main_menu.display_menu()

# Create an instance of GameScreen with the selected difficulty, then run the game
game_screen = GameScreen(main_menu.selected_difficulty)
game_screen.run()
