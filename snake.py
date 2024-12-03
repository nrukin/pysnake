import pygame
import sys
import random

__version__ = "0.0.3.dev"

def start_game():
    pygame.init()
    
    g = Game()

    icon = pygame.image.load("snake.png")
    pygame.display.set_icon(icon)
    
    window = pygame.display.set_mode((g.width * cell_size, g.height * cell_size))
    pygame.display.set_caption(f"Snake ({__version__})")
''
    while True:
        g.update()
        if g.quit:
            pygame.quit()
            sys.exit()
            

class Game:

    def __init__(self):

        self.width = 32
        self.height = 24
        self.cell_size = 20
        
        self.player = None
        self.body = None
        self.apple = None

        self.head_color = pygame.Color(0, 255, 0)
        self.body_color = pygame.Color(0, 255, 0)
        self.apple_color = pygame.Color(255, 0, 0)
        self.text_color = pygame.Color(255, 255, 255)
        self.bg_color = pygame.Color(0, 0, 0)

        self.reset = True

        self.font = pygame.font.Font(None, cell_size * 3)
        self.clock = pygame.time.Clock()

        self.direction_stack = []
        self.pause = False

        self.game_over = False

        self.quit = False

        self.direction_by_key = {}
        self.direction_by_key[pygame.K_UP] = (0, -1)
        self.direction_by_key[pygame.K_DOWN] = (0, 1)
        self.direction_by_key[pygame.K_LEFT] = (-1, 0)
        self.direction_by_key[pygame.K_RIGHT] = (1, 0)

    def active(self):
        return not (self.game_over or self.pause)

    def handle_event(self, event):

        if event.type == pygame.QUIT:
                self.quit = True
                return

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_q:
                self.quit = True
                return

            if event.key == pygame.K_n:
                self.reset = True
                return

            if event.key == pygame.K_p:
                self.pause = not self.pause
                return

            if self.active:
                new_direction = self.direction_by_key[event.key]
                if new_direction:
                    direction_stack.append(new_direction)

    def update(self):
        
        for event in pygame.event.get():
            self.handle_event(event)
            
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
        if not (game_over or pause):

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

        if not (game_over or pause):

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

        center_x = window.get_width() // 2
        center_y = window.get_height() // 2

        if pause:
            text = font.render(f"Pause", True, text_color)
            text_pos = text.get_rect(
                centerx=center_x, centery=center_y
            )
            window.blit(text, text_pos)

        elif game_over:

            text = font.render(f"Game Over", True, text_color)
            text_pos = text.get_rect(
                centerx=center_x, bottom=center_y
            )
            window.blit(text, text_pos)

            text = font.render(f"Total Score: {score}", True, text_color)
            text_pos = text.get_rect(
                centerx=center_x, top=center_y
            )
            window.blit(text, text_pos)

        pygame.display.update()
        clock.tick(15)

if __name__ == "__main__":
    start_game()
