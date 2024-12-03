import pygame
import sys
import random
from vector import vector

__version__ = "0.0.3.dev"

def draw_pt_as_rect(window, color, point, cell_size):
        pygame.draw.rect(
            window,
            color,
            pygame.Rect(point.x * cell_size, point.y * cell_size, cell_size, cell_size),
        )    

def start_game():

    pygame.init()
    
    g = Game()

    icon = pygame.image.load("snake.png")
    pygame.display.set_icon(icon)
    
    window = pygame.display.set_mode((g.width * g.cell_size, g.height * g.cell_size))
    pygame.display.set_caption(f"Snake ({__version__})")

    while True:
        g.update(window)
        if g.do_exit:
            pygame.quit()
            sys.exit()

class Game:

    def __init__(self):

        # size
        self.width = 32
        self.height = 24
        self.cell_size = 20

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

        # reset gameplay
        self.reset()

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
                new_direction = self.direction_by_key[event.key]
                if new_direction:
                    self.direction_stack.append(new_direction)

    def update(self, window):

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

        # create apple
        if self.apple is None:
            self.apple = self.random_empty_pos()

        new_pos = self.player.copy()
        
        # check game-over collide
        if self.is_active():
            new_pos.add(self.direction)            
            if new_pos.x < 0 or new_pos.x >= self.width:
                self.game_over = True
            if new_pos.y < 0 or new_pos.y >= self.height:
                self.game_over = True
            if new_pos in self.body:
                self.game_over = True
        
        if self.is_active():
            self.body.insert(0, self.player.copy())
            while len(self.body) > self.score:
                self.body.pop()                
            self.player = new_pos
            if self.player == self.apple:
                self.score += 1
                self.apple = None

        window.fill(self.bg_color)

        draw_pt_as_rect(window, self.head_color, self.player, self.cell_size)
        
        for body_part in self.body:
            draw_pt_as_rect(window, self.body_color, body_part, self.cell_size)

        if not self.apple is None:
            draw_pt_as_rect(window, self.apple_color, self.apple, self.cell_size)

        # text = font.render(f"Score: {score}", True, text_color)
        # text_pos = text.get_rect(x=15, y=15)
        # window.blit(text, text_pos)

        # center_x = window.get_width() // 2
        # center_y = window.get_height() // 2

        # if pause:
        #     text = font.render(f"Pause", True, text_color)
        #     text_pos = text.get_rect(
        #         centerx=center_x, centery=center_y
        #     )
        #     window.blit(text, text_pos)

        # elif game_over:

        #     text = font.render(f"Game Over", True, text_color)
        #     text_pos = text.get_rect(
        #         centerx=center_x, bottom=center_y
        #     )
        #     window.blit(text, text_pos)

        #     text = font.render(f"Total Score: {score}", True, text_color)
        #     text_pos = text.get_rect(
        #         centerx=center_x, top=center_y
        #     )
        #     window.blit(text, text_pos)

        pygame.display.update()
        self.clock.tick(15)

if __name__ == "__main__":
    start_game()
