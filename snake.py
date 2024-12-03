import pygame
import sys
import random

width = 64
height = 48
cell_size = 15

head_color = pygame.Color(0, 255, 0)
body_color = pygame.Color(0, 255, 0)
apple_color = pygame.Color(255, 0, 0)
text_color = pygame.Color(255, 255, 255)
bg_color = pygame.Color(0, 0, 0)

reset = True

pygame.init()
font = pygame.font.Font(None, 60)
clock = pygame.time.Clock()


icon = pygame.image.load("snake.png")
pygame.display.set_icon(icon)

window = pygame.display.set_mode((width * cell_size, height * cell_size))
pygame.display.set_caption("Snake")

direction_stack = []

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_n:
                reset = True

            if not game_over:

                new_direction = None
                if event.key == pygame.K_UP:
                    new_direction = (0, -1)
                if event.key == pygame.K_DOWN:
                    new_direction = (0, 1)
                if event.key == pygame.K_LEFT:
                    new_direction = (-1, 0)
                if event.key == pygame.K_RIGHT:
                    new_direction = (1, 0)

                if not new_direction is None:
                    direction_stack.append(new_direction)

    if len(direction_stack):
        new_direction = direction_stack.pop(0)
        if direction[0] + new_direction[0] != 0 or direction[1] + new_direction[1] != 0:
            direction = new_direction

    if reset:
        player = [width // 2, height // 2]
        body = []
        apple = None
        direction = (0, 0)
        score = 0
        game_over = False
        reset = False
        direction_stack.clear()

    if apple is None:
        while True:
            apple = [
                random.randint(0, width - 1),
                random.randint(0, height - 1),
            ]

            apple_collide = False
            if apple[0] == player[0] and apple[1] == player[1]:
                apple_collide = True

            for body_part in body:
                if apple[0] == body_part[0] and apple[1] == body_part[1]:
                    apple_collide = True
                    break

            if apple_collide:
                continue
            break

    new_pos = player[:]
    if not game_over:

        new_pos[0] += direction[0]
        new_pos[1] += direction[1]

        if new_pos[0] < 0 or new_pos[0] >= width:
            game_over = True
        if new_pos[1] < 0 or new_pos[1] >= height:
            game_over = True

        for body_part in body:
            if new_pos[0] == body_part[0] and new_pos[1] == body_part[1]:
                game_over = True
                break

    if not game_over:

        body.insert(0, player[:])
        while len(body) > score:
            body.pop()

        player[0], player[1] = new_pos[0], new_pos[1]
        if player[0] == apple[0] and player[1] == apple[1]:
            score += 1
            apple = None

    window.fill(bg_color)

    pygame.draw.rect(
        window,
        head_color,
        pygame.Rect(player[0] * cell_size, player[1] * cell_size, cell_size, cell_size),
    )

    for body_part in body:
        pygame.draw.rect(
            window,
            body_color,
            pygame.Rect(
                body_part[0] * cell_size, body_part[1] * cell_size, cell_size, cell_size
            ),
        )

    if not apple is None:
        pygame.draw.rect(
            window,
            apple_color,
            pygame.Rect(
                apple[0] * cell_size, apple[1] * cell_size, cell_size, cell_size
            ),
        )

    text = font.render(f"Score: {score}", True, text_color)
    text_pos = text.get_rect(x=15, y=15)
    window.blit(text, text_pos)

    if game_over:
        text = font.render("Game Over", True, text_color)
        text_pos = text.get_rect(
            centerx=window.get_width() // 2, centery=window.get_height() // 2
        )
        window.blit(text, text_pos)

    pygame.display.update()
    clock.tick(15)
