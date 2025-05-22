import pygame
import random

pygame.init()

pygame.display.set_caption("Snake")
snake_list = []
snake_lenght = 4
cell_size = 20
width = 600
height = 400
snake_x = width // 2
snake_y = height // 2
snake_size = cell_size
dx = cell_size
dy = 0
move_delay = 10   # co ile klatek wąż ma się ruszać (im większa liczba, tym wolniej)
frame_count = 0  # licznik klatek


size = (width, height)
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

food_x = random.randint(20 // cell_size, (width - 20) // cell_size - 1) * cell_size
food_y = random.randint(20 // cell_size, (height - 20) // cell_size - 1) * cell_size



running = True
while running:
    clock.tick(60)
    screen.fill((0, 128, 0))
    # obramowanie czerwone
    pygame.draw.rect(screen, (255, 0, 0), (0, 0, width, height), 20)

    # pionowe linie
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, height))

    # poziome linie
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, (0, 0, 0), (0, y), (width, y))

    # Wąż
    frame_count += 1
    if frame_count % move_delay == 0:
        snake_x += dx
        snake_y += dy
        snake_head = [snake_x, snake_y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_lenght:
            del snake_list[0]
    for segment_x, segment_y in snake_list:
        pygame.draw.rect(screen, (0, 255, 0), (segment_x, segment_y, snake_size, snake_size))

    # Jedzenie - rysowanie
    pygame.draw.rect(screen, (220, 0, 0), (food_x, food_y, cell_size, cell_size))

    # Wynik
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {snake_lenght - 4}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


    pygame.display.flip()


    # Sprawdzenie kolizji ze ścianami
    if (
            snake_x < 0 or
            snake_x + snake_size > width or
            snake_y < 0 or
            snake_y + snake_size > height
    ):
        running = False
    for segment in snake_list[:-1]:
        if segment == snake_head:
            running = False
            break
    #Sprawdzanie kolizji z jedzeniem
    if snake_x == food_x and snake_y == food_y:
        food_x = random.randint(20 // cell_size, (width - 20) // cell_size - 1) * cell_size
        food_y = random.randint(20 // cell_size, (height - 20) // cell_size - 1) * cell_size

        snake_lenght += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and dx == 0:
                dx = -cell_size
                dy = 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx = cell_size
                dy = 0
            elif event.key == pygame.K_UP and dy == 0:
                dx = 0
                dy = -cell_size
            elif event.key == pygame.K_DOWN and dy == 0:
                dx = 0
                dy = cell_size

        if event.type == pygame.QUIT:
            running = False

pygame.quit()
