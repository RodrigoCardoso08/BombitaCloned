import pygame
import sys
import os
from constants import *
from player import *
from block import *
from enemy import *
import math


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
        self.walls = []
        self.single_background = None
        self.menu_background = None
        self.gameover_background = None
        self.dir_audios = None
        self.load_files()
        self.cell_width = WIDTH//X_CELLS
        self.cell_height = HEIGHT//Y_CELLS
        self.player1 = Player(self, PLAYER_START_POS)
        self.player2 = Player(self, PLAYER_START_POS)
        self.enemy = Enemy(self, ENEMY_START_POS)
        self.blocks = [None]*BLOCKS_NUMBER
        for i in range(len(self.blocks)):
            self.blocks[i] = Block(self)
        self.all_sprites = pygame.sprite.Group()
        for i in range(len(self.blocks)):
            self.all_sprites.add(self.blocks[i])
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)
        self.all_sprites.add(self.enemy)
        self.collision_sprites = pygame.sprite.Group()
        self.collision_sprites.add(self.enemy)
        self.collision_sprites_bomb_player = pygame.sprite.Group()
        self.collision_sprites_bomb_player.add(self.player1.bomb)
        self.collision_sprites_bomb_player.add(self.player2.bomb)
        self.collision_sprites_bomb = pygame.sprite.Group()
        self.collision_sprites_bomb.add(self.enemy)
        self.collision_sprites_bomb_block = pygame.sprite.Group()
        for i in range(len(self.blocks)):
            self.collision_sprites_bomb_block.add(self.blocks[i])
        self.bool1 = False
        self.collisions1 = None
        self.collisions_bomb1 = None
        self.collisions_bomb_block1 = None
        self.collisions_bomb_player1 = None
        self.bool2 = False
        self.collisions2 = None
        self.collisions_bomb2 = None
        self.collisions_bomb_block2 = None
        self.collisions_bomb_player2 = None

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
            if self.state == 'gameover':
                self.gameover_events()
                self.gameover_update()
                self.gameover_draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

# ---------------------------- GENERAL FUNCTIONS -----------------------------------------

    def load_files(self):
        """"""
        dir_images = os.path.join(os.getcwd(), 'images')
        self.dir_audios = os.path.join(os.getcwd(), 'audios')
        self.menu_background = os.path.join(dir_images, MENU_BACKGROUND)
        self.menu_background = pygame.image.load(self.menu_background).convert()
        self.menu_background = pygame.transform.scale(self.menu_background,
                                                      (WIDTH, HEIGHT))
        self.single_background = os.path.join(dir_images, SINGLE_BACKGROUND)
        self.single_background = pygame.image.load(self.single_background).convert()
        self.single_background = pygame.transform.scale(self.single_background,
                                                        (WIDTH, HEIGHT))

        self.gameover_background = os.path.join(dir_images, GAME_OVER_BACKGROUND)
        self.gameover_background = pygame.image.load(self.gameover_background).convert()
        self.gameover_background = pygame.transform.scale(self.gameover_background,
                                                      (WIDTH, HEIGHT))
        # Creating list with the grid positions that have walls
        with open(os.path.join(os.getcwd(), 'walls.txt'), 'r') as file:
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vector(x, y))

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player1.drop_bomb()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                self.player2.drop_bomb()


        if pygame.key.get_pressed()[pygame.K_w]:
            self.player1.move(vector(0, -1), 0)
        elif pygame.key.get_pressed()[pygame.K_s]:
            self.player1.move(vector(0, 1), 2)
        elif pygame.key.get_pressed()[pygame.K_a]:
            self.player1.move(vector(-1, 0), 3)
        elif pygame.key.get_pressed()[pygame.K_d]:
            self.player1.move(vector(1, 0), 1)
        else:
            self.player1.move(vector(0, 0), 0)

        if pygame.key.get_pressed()[pygame.K_UP]:
            self.player2.move(vector(0, -1), 0)
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            self.player2.move(vector(0, 1), 2)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            self.player2.move(vector(-1, 0), 3)
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.player2.move(vector(1, 0), 1)
        else:
            self.player2.move(vector(0, 0), 0)

        self.bool1 = False
        for wall in self.walls:
            dist_x = abs((wall.x + 1/2) * self.cell_width - self.player1.pix_pos.x)
            dist_y = abs((wall.y + 1/2) * self.cell_height - (self.player1.pix_pos.y + 20))

            if dist_x < self.cell_width*3/5 and dist_y < self.cell_height*3/5:
                self.player1.ban_direction()
                self.player1.blocked = True
                self.bool1 = True

        if not self.bool1:
            self.player1.blocked = False
            self.player1.banned_direction = vector(1, 1)

        self.bool2 = False
        for wall in self.walls:
            dist_x = abs((wall.x + 1 / 2) * self.cell_width - self.player2.pix_pos.x)
            dist_y = abs((wall.y + 1 / 2) * self.cell_height - (self.player2.pix_pos.y + 20))

            if dist_x < self.cell_width * 3 / 5 and dist_y < self.cell_height * 3 / 5:
                self.player2.ban_direction()
                self.player2.blocked = True
                self.bool2 = True

        if not self.bool2:
            self.player2.blocked = False
            self.player2.banned_direction = vector(1, 1)

    def single_update(self):
        if self.collisions1 or self.collisions2:
            self.state = 'gameover'
        else:
            self.enemy.update()
            for i in range(len(self.blocks)):
                self.blocks[i].update()
            self.player1.update()
            self.player2.update()
        if self.collisions_bomb1 or self.collisions_bomb2:
            self.all_sprites.remove(self.enemy)
            self.enemy.destroy()
        if self.collisions_bomb_player1:
            self.all_sprites.remove(self.player1)
            self.player1.destroy()
        if self.collisions_bomb_player2:
            self.all_sprites.remove(self.player2)
            self.player2.destroy()

        self.collisions1 = pygame.sprite.spritecollide(self.player1,
                                                       self.collision_sprites, False
                                                       , pygame.sprite.collide_mask)
        if self.player1.bomb.exploded:
            self.collisions_bomb1 = pygame.sprite.spritecollide(self.player1.bomb,
                                                                self.collision_sprites_bomb
                                                                , False
                                                                , pygame.sprite.collide_mask)
            self.collisions_bomb_player1 = pygame.sprite.spritecollide(self.player1,
                                                                self.collision_sprites_bomb_player
                                                                , False
                                                                , pygame.sprite.collide_mask)
            self.collisions_bomb_player2 = pygame.sprite.spritecollide(self.player2,
                                                                self.collision_sprites_bomb_player
                                                                , False
                                                                , pygame.sprite.collide_mask)
        self.collisions_bomb_block1 = pygame.sprite.spritecollide(self.player1.bomb,
                                                                  self.collision_sprites_bomb_block,
                                                                  False
                                                                  , pygame.sprite.collide_mask)

        self.collisions2 = pygame.sprite.spritecollide(self.player2,
                                                       self.collision_sprites, False
                                                     , pygame.sprite.collide_mask)
        if self.player2.bomb.exploded:
            self.collisions_bomb2 = pygame.sprite.spritecollide(self.player2.bomb,
                                                                self.collision_sprites_bomb
                                                                , False
                                                                , pygame.sprite.collide_mask)
            self.collisions_bomb_player1 = pygame.sprite.spritecollide(self.player1,
                                                                self.collision_sprites_bomb_player
                                                                , False
                                                                , pygame.sprite.collide_mask)
            self.collisions_bomb_player2 = pygame.sprite.spritecollide(self.player2,
                                                                self.collision_sprites_bomb_player
                                                                , False
                                                                , pygame.sprite.collide_mask)
        self.collisions_bomb_block2 = pygame.sprite.spritecollide(self.player2.bomb,
                                                                  self.collision_sprites_bomb_block,
                                                                  False
                                                                  , pygame.sprite.collide_mask)
        # print(self.collisions1)
        # print(self.collisions_bomb1)
        # print(self.collisions_bomb_block1)
        # print(self.clock.get_fps())

    def single_draw(self):
        """"""
        self.window.blit(self.single_background, (0, 0))
        self.draw_grid()
        self.player1.draw()
        self.player2.draw()
        self.all_sprites.draw(self.window)
        pygame.display.update()

# ---------------------------- GAME OVER FUNCTIONS ---------------------------------------

    def gameover_events(self):
        """"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                self.state = 'menu'
                self.is_running = False

        pass

    def gameover_update(self):
        """"""
        pass

    def gameover_draw(self):
        """"""
        self.window.blit(self.gameover_background, (0, 0))
        self.write_text(self.window, MENU_TEXT_SIZE, WHITE,
                        MENU_TEXT_FONT, 'PRESS ANY KEY TO QUIT', [400, 170])
        pygame.display.update()