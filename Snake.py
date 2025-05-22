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

size = (width, height)
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

food_x = random.randint(0, (width - cell_size) // cell_size) * cell_size
food_y = random.randint(0, (height - cell_size) // cell_size) * cell_size


running = True
while running:
    clock.tick(10)
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
        food_x = random.randint(0, (width - cell_size) // cell_size) * cell_size
        food_y = random.randint(0, (height - cell_size) // cell_size) * cell_size
        snake_lenght += 1

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -cell_size
                dy = 0
            elif event.key == pygame.K_RIGHT:
                dx = cell_size
                dy = 0
            elif event.key == pygame.K_UP:
                dx = 0
                dy = -cell_size
            elif event.key == pygame.K_DOWN:
                dx = 0
                dy = cell_size

        if event.type == pygame.QUIT:
            running = False

pygame.quit()
