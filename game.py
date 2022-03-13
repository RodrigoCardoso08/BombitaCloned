import pygame
import sys
import os
from constants import *
import sprites


class Game:
    def __init__(self):
        """"""
        pygame.init()
        pygame.mixer.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.state = 'menu'
        self.menu_options = 0
        self.load_files()
        self.cell_width = WIDTH//X_CELLS
        self.cell_height = HEIGHT//Y_CELLS

    def run(self):
        """"""
        while self.is_running:
            if self.state == 'menu':
                self.menu_events()
                self.menu_update()
                self.menu_draw()
            if self.state == 'singleplayer':
                self.single_events()
                self.single_update()
                self.single_draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

# ---------------------------- GENERAL FUNCTIONS -----------------------------------------

    def load_files(self):
        """"""
        dir_images = os.path.join(os.getcwd(), 'images')
        self.dir_audios = os.path.join(os.getcwd(), 'audios')
        # self.spritesheet = os.path.join(dir_images, constantes.SPRITESHEET)
        self.menu_background = os.path.join(dir_images, MENU_BACKGROUND)
        self.menu_background = pygame.image.load(self.menu_background).convert()
        self.menu_background = pygame.transform.scale(self.menu_background,
                                                      (WIDTH, HEIGHT))
        self.single_background = os.path.join(dir_images, SINGLE_BACKGROUND)
        self.single_background = pygame.image.load(self.single_background).convert()
        self.single_background = pygame.transform.scale(self.single_background,
                                                        (WIDTH, HEIGHT))

    def write_text(self, window, size, color, font_name, msg, position):
        """"""
        font = pygame.font.SysFont(font_name, size)
        text = font.render(msg, False, color)
        text_size = text.get_size()
        position[0] = position[0] - text_size[0]//2
        position[1] = position[1] - text_size[1]//2
        window.blit(text, position)

    def draw_grid(self):
        for x in range(X_CELLS):
            pygame.draw.line(self.window, GREY, (x*self.cell_width, 0),
                             (x*self.cell_width, HEIGHT))
        for y in range(Y_CELLS):
            pygame.draw.line(self.window, GREY, (0, y * self.cell_height),
                             (WIDTH, y * self.cell_height))

# ----------------------------- INTRO FUNCTIONS ------------------------------------------

    def menu_events(self):
        """"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.menu_options -= 1
                    if self.menu_options < 0:
                        self.menu_options = 2
                if event.key == pygame.K_DOWN:
                    self.menu_options += 1
                    if self.menu_options > 2:
                        self.menu_options = 0
                if event.key == pygame.K_SPACE:
                    if self.menu_options == 0:
                        self.state = 'singleplayer'
                    elif self.menu_options == 1:
                        self.state = 'multiplayer'
                    elif self.menu_options == 2:
                        self.state = 'challenge'

    def menu_update(self):
        """"""
        pass

    def menu_draw(self):
        """"""
        single_color = BLACK
        multi_color = BLACK
        challenge_color = BLACK
        if self.menu_options == 0:
            single_color = WHITE
        elif self.menu_options == 1:
            multi_color = WHITE
        elif self.menu_options == 2:
            challenge_color = WHITE
        self.window.blit(self.menu_background, (0, 0))
        self.write_text(self.window, MENU_TEXT_SIZE, single_color,
                        MENU_TEXT_FONT, 'Single Player', [150, 230])
        self.write_text(self.window, MENU_TEXT_SIZE, multi_color,
                        MENU_TEXT_FONT, 'Multi Player', [150, 280])
        self.write_text(self.window, MENU_TEXT_SIZE, challenge_color,
                        MENU_TEXT_FONT, 'Challenge', [150, 330])
        pygame.display.update()

# ------------------------- SINGLEPLAYER FUNCTIONS ---------------------------------------

    def single_events(self):
        """"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def single_update(self):
        """"""
        pass

    def single_draw(self):
        """"""
        self.window.blit(self.single_background, (0, 0))
        self.draw_grid()
        pygame.display.update()
