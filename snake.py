import pygame
import sys
import random
from vector import vector

__version__ = "0.0.3.dev"


def start_game():

    pygame.init()
    icon = pygame.image.load("snake.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption(f"Snake ({__version__})")

    g = Game(width=32, height=24, speed=12)

    while True:
        g.update()
        if g.do_exit:
            pygame.quit()
            sys.exit()


class Game:

    def __init__(self, width=32, height=24, cell_size=20, speed=12):

        # size and gameplay
        self.speed = speed
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.border = 10

        # objects
        self.player = None
        self.body = None
        self.apple = None

        # colors and view
        self.head_color = pygame.Color(0, 255, 0)
        self.body_color = pygame.Color(0, 255, 0)
        self.apple_color = pygame.Color(255, 0, 0)
        self.text_color = pygame.Color(255, 255, 255)
        self.bg_color = pygame.Color(0, 0, 0)

        self.font = pygame.font.Font(None, self.cell_size * 3)

        # state
        self.game_over = False
        self.pause = False
        self.do_exit = False
        self.do_reset = False
        self.score = 0
        self.body_len = 0

        # player direction
        self.direction = None
        self.direction_stack = []

        # direction by keys
        self.direction_by_key = {}
        self.direction_by_key[pygame.K_UP] = vector.up()
        self.direction_by_key[pygame.K_DOWN] = vector.down()
        self.direction_by_key[pygame.K_LEFT] = vector.left()
        self.direction_by_key[pygame.K_RIGHT] = vector.right()

        # clock
        self.clock = pygame.time.Clock()

        # main window
        total_width = self.border * 2 + self.width * self.cell_size
        total_height = self.border * 2 + self.height * self.cell_size + 3 * self.cell_size
        self.window = pygame.display.set_mode((total_width, total_height))

        # reset gameplay
        self.reset()

    def draw_borders(self):

        def draw_border(left, top, width, height):
            r = pygame.Rect(left, top, width, height)
            border_color = pygame.Color(0, 0, 255)
            pygame.draw.rect(self.window, border_color, r)

        border_width = self.width * self.cell_size + self.border * 2
        border_height = self.height * self.cell_size
            
        draw_border(0, 3 * self.cell_size, border_width, self.border)                                                        # top
        draw_border(0, 3 * self.cell_size + self.height * self.cell_size + self.border, border_width, self.border)           # bottom
        draw_border(0, 3 * self.cell_size + self.border, self.border, border_height)                                         # left
        draw_border(self.width * self.cell_size + self.border, 3 * self.cell_size + self.border, self.border, border_height) # right

    def draw_pt_as_rect(self, color, point):
        pygame.draw.rect(
            self.window,
            color,
            pygame.Rect(
                point.x * self.cell_size + self.border,
                3 * self.cell_size + point.y * self.cell_size + self.border,
                self.cell_size,
                self.cell_size,
            ),
        )

    def random_empty_pos(self):
        while True:
            rnd_pos = vector(
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1),
            )
            if rnd_pos == self.player:
                continue
            if rnd_pos in self.body:
                continue
            return rnd_pos

    def reset(self):

        # objects
        self.player = vector(self.width // 2, self.height // 2)
        self.body = []
        self.apple = None

        # player direction
        self.direction = vector.zero()
        self.direction_stack.clear()

        # state
        self.game_over = False
        self.pause = False
        self.do_exit = False
        self.do_reset = False
        self.score = 0
        self.body_len = 3

    def is_active(self):
        return not (self.game_over or self.pause)

    def handle_event(self, event):

        if event.type == pygame.QUIT:
            self.do_exit = True
            return

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_q:
                self.do_exit = True
                return

            if event.key == pygame.K_n:
                self.do_reset = True
                return

            if event.key == pygame.K_p:
                self.pause = not self.pause
                return

            if self.is_active():
                new_direction = self.direction_by_key.get(event.key)
                if new_direction:
                    self.direction_stack.append(new_direction)

    def draw_game_over(self):

        if not self.game_over:
            return

        center_x = self.window.get_width() // 2
        center_y = self.window.get_height() // 2

        text = self.font.render(f"Game Over", True, self.text_color)
        text_pos = text.get_rect(centerx=center_x, bottom=center_y)
        self.window.blit(text, text_pos)

        text = self.font.render(f"Total Score: {self.score}", True, self.text_color)
        text_pos = text.get_rect(centerx=center_x, top=center_y)
        self.window.blit(text, text_pos)

    def draw_pause(self):

        if not self.pause:
            return

        center_x = self.window.get_width() // 2
        center_y = self.window.get_height() // 2

        text = self.font.render(f"Pause", True, self.text_color)
        text_pos = text.get_rect(centerx=center_x, centery=center_y)
        self.window.blit(text, text_pos)

    def draw_score(self):
        text = self.font.render(f"Score: {self.score}", True, self.text_color)
        text_pos = text.get_rect(x=self.cell_size // 2, y=self.cell_size // 2)
        self.window.blit(text, text_pos)

    def update(self):

        # handle incoming events
        for event in pygame.event.get():
            self.handle_event(event)

        # change direction by direction stack
        if self.direction_stack:
            new_direction = self.direction_stack.pop(0)
            if not (self.direction + new_direction).is_zero():
                self.direction = new_direction

        # reset
        if self.do_reset:
            self.reset()
            return

        # create apple
        if self.apple is None:
            self.apple = self.random_empty_pos()

        new_pos = self.player.copy()

        # check game-over collide
        if self.is_active() and not self.direction.is_zero():
            new_pos.add(self.direction)
            if new_pos.x < 0 or new_pos.x >= self.width:
                self.game_over = True
            if new_pos.y < 0 or new_pos.y >= self.height:
                self.game_over = True
            if new_pos in self.body:
                self.game_over = True

        if self.is_active():
            self.body.insert(0, self.player.copy())
            while len(self.body) > self.body_len:
                self.body.pop()
            self.player = new_pos
            if self.player == self.apple:
                self.score += 1
                self.body_len += 3
                self.apple = None

        self.window.fill(self.bg_color)
        self.draw_borders()

        self.draw_pt_as_rect(self.head_color, self.player)

        for body_part in self.body:
            self.draw_pt_as_rect(self.body_color, body_part)

        if not self.apple is None:
            self.draw_pt_as_rect(self.apple_color, self.apple)

        self.draw_game_over()
        self.draw_pause()
        self.draw_score()

        pygame.display.update()
        self.clock.tick(self.speed)


if __name__ == "__main__":
    start_game()
