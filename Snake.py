"""
Snake Game Implementation using Pygame

This code implements a classic Snake game with the following features:
- Multiple difficulty levels (Easy, Medium, Hard)
- Pause menu with music control
- Score tracking
- Wall collisions
- Self-collision detection
- Grid-based movement
"""

import pygame
import random

# Initialize pygame modules
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Snake")

# Game constants
CELL_SIZE = 20  # Size of each grid cell
WIDTH = 800  # Game window width
HEIGHT = 600  # Game window height
SCREEN_SIZE = (WIDTH, HEIGHT)
BORDER_WIDTH = 20  # Width of the game border

# Initialize game screen
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

# Game variables
snake_length = 4  # Initial snake length
score = snake_length - 4  # Initial score
music_enabled = True  # Music toggle flag
selected_difficulty = "medium"  # Default difficulty

# Initialize food position (ensuring it spawns within borders)
food_x = random.randint(BORDER_WIDTH // CELL_SIZE,
                        (WIDTH - BORDER_WIDTH) // CELL_SIZE - 1) * CELL_SIZE
food_y = random.randint(BORDER_WIDTH // CELL_SIZE,
                        (HEIGHT - BORDER_WIDTH) // CELL_SIZE - 1) * CELL_SIZE


def music():
    """Load and play background music in loop if music is enabled"""
    if music_enabled:
        pygame.mixer.music.load("muzyka1.ogg")  # Music file
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely


def stop_music():
    """Stop the background music"""
    pygame.mixer.music.stop()


def get_move_delay(difficulty):
    """Return movement speed based on selected difficulty"""
    if difficulty == "easy":
        return 15  # Slowest speed
    elif difficulty == "medium":
        return 10  # Medium speed
    elif difficulty == "hard":
        return 5  # Fastest speed
    return 10  # Default speed


def pause_menu():
    """Display pause menu with options to resume or toggle music"""
    global music_enabled
    paused = True
    font = pygame.font.SysFont(None, 36)  # Default font

    while paused:
        # Dark background for pause menu
        screen.fill((30, 30, 30))

        # Render text surfaces
        pause_text = font.render("PAUSED", True, (255, 255, 255))
        resume_text = font.render("Press ESC to resume", True, (255, 255, 255))

        # Dynamic music status text
        music_status = "ON (Press M to turn OFF)" if music_enabled else "OFF (Press M to turn ON)"
        music_text = font.render(f"Music: {music_status}", True, (255, 255, 255))

        # Center and display all text elements
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(music_text, (WIDTH // 2 - music_text.get_width() // 2, HEIGHT // 2 + 20))

        pygame.display.flip()  # Update display

        # Event handling for pause menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False  # Resume game
                elif event.key == pygame.K_m:
                    # Toggle music state
                    music_enabled = not music_enabled
                    if music_enabled:
                        music()  # Restart music
                    else:
                        stop_music()  # Stop music


def show_game_over_screen(score):
    """Display game over screen with final score and restart options"""
    waiting = True
    font = pygame.font.SysFont(None, 36)

    while waiting:
        # Green background
        screen.fill((0, 128, 0))

        # Render text elements
        title = font.render("Game Over", True, (255, 255, 255))
        score_text = font.render(f"Your score: {score}", True, (255, 255, 255))
        restart_text = font.render("Press SPACE to restart or ESC to quit", True, (255, 255, 255))

        # Center and display text
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        # Event handling for game over screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False  # Restart game
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()  # Quit game


def show_start_screen():
    """Display start screen with difficulty options and music control"""
    global selected_difficulty, music_enabled
    font = pygame.font.SysFont(None, 36)
    waiting = True

    while waiting:
        # Green background
        screen.fill((0, 128, 0))
        # Enable key repeat for better menu navigation
        pygame.key.set_repeat(200, 20)

        # Render all text elements
        title = font.render("Welcome to Snake!", True, (255, 255, 255))
        easy_text = font.render("1 - Easy", True, (255, 255, 255))
        medium_text = font.render("2 - Medium", True, (255, 255, 255))
        hard_text = font.render("3 - Hard", True, (255, 255, 255))
        prompt_text = font.render("Select difficulty (1/2/3)", True, (255, 255, 255))

        # Dynamic music status text
        music_status = "ON (Press M to turn OFF)" if music_enabled else "OFF (Press M to turn ON)"
        music_text = font.render(f"Music: {music_status}", True, (255, 255, 255))

        # Center and display all text elements
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2))
        screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 2 + 40))
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 + 100))
        screen.blit(music_text, (WIDTH // 2 - music_text.get_width() // 2, HEIGHT // 2 + 150))

        pygame.display.flip()

        # Event handling for start screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # Difficulty selection
                if event.key == pygame.K_1:
                    selected_difficulty = "easy"
                    waiting = False
                elif event.key == pygame.K_2:
                    selected_difficulty = "medium"
                    waiting = False
                elif event.key == pygame.K_3:
                    selected_difficulty = "hard"
                    waiting = False
                # Music toggle
                elif event.key == pygame.K_m:
                    music_enabled = not music_enabled
                    if music_enabled:
                        music()
                    else:
                        stop_music()


def run_game():
    """Main game loop handling snake movement, collisions, and scoring"""
    global music_enabled, selected_difficulty

    # Initialize game state
    snake_list = []
    snake_length = 4
    snake_x = WIDTH // 2  # Start in center
    snake_y = HEIGHT // 2
    dx = CELL_SIZE  # Initial movement direction (right)
    dy = 0
    move_delay = get_move_delay(selected_difficulty)
    frame_count = 0

    # Place initial food
    food_x = random.randint(BORDER_WIDTH // CELL_SIZE,
                            (WIDTH - BORDER_WIDTH) // CELL_SIZE - 1) * CELL_SIZE
    food_y = random.randint(BORDER_WIDTH // CELL_SIZE,
                            (HEIGHT - BORDER_WIDTH) // CELL_SIZE - 1) * CELL_SIZE

    running = True
    while running:
        # Control game speed (60 FPS)
        clock.tick(60)
        screen.fill((0, 128, 0))  # Green background

        # Draw game border
        pygame.draw.rect(screen, (255, 0, 0), (0, 0, WIDTH, HEIGHT), BORDER_WIDTH)

        # Draw grid lines
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, (0, 0, 0), (0, y), (WIDTH, y))

        # Snake movement logic
        frame_count += 1
        if frame_count % move_delay == 0:
            # Update snake position
            snake_x += dx
            snake_y += dy
            snake_head = [snake_x, snake_y]
            snake_list.append(snake_head)

            # Maintain snake length
            if len(snake_list) > snake_length:
                del snake_list[0]

            # Check for self-collision
            for segment in snake_list[:-1]:
                if segment == snake_head:
                    running = False
                    break

        # Draw snake segments
        for segment in snake_list:
            pygame.draw.rect(screen, (0, 255, 0),
                             (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

        # Draw food
        pygame.draw.rect(screen, (220, 0, 0),
                         (food_x, food_y, CELL_SIZE, CELL_SIZE))

        # Display score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {snake_length - 4}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        # Check wall collision (considering border width)
        if (snake_x < BORDER_WIDTH or
                snake_x + CELL_SIZE > WIDTH - BORDER_WIDTH or
                snake_y < BORDER_WIDTH or
                snake_y + CELL_SIZE > HEIGHT - BORDER_WIDTH):
            running = False

        # Check food collision
        if snake_x == food_x and snake_y == food_y:
            # Place new food (within borders)
            food_x = random.randint(BORDER_WIDTH // CELL_SIZE,
                                    (WIDTH - BORDER_WIDTH) // CELL_SIZE - 1) * CELL_SIZE
            food_y = random.randint(BORDER_WIDTH // CELL_SIZE,
                                    (HEIGHT - BORDER_WIDTH) // CELL_SIZE - 1) * CELL_SIZE
            snake_length += 1  # Grow snake

        # Event handling during gameplay
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                # Direction controls (prevent 180-degree turns)
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -CELL_SIZE
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = CELL_SIZE
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx = 0
                    dy = -CELL_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx = 0
                    dy = CELL_SIZE
                elif event.key == pygame.K_ESCAPE:
                    pause_menu()  # Open pause menu

    return snake_length - 4  # Final score


# Start music and run main game loop
music()
while True:
    show_start_screen()
    score = run_game()
    show_game_over_screen(score)
