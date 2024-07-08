import pygame
import pygame_menu
import pygame_menu.widgets
from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square


class Game:

    def __init__(self):
        self.next_player = "white"
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

        # creating theme
        self.my_theme = pygame_menu.themes.THEME_DARK.copy()
        self.my_theme.background_color = (0, 0, 0)
        self.my_theme.title_background_color = (47, 50, 54)
        self.my_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY
        self.my_theme.title_font = pygame_menu.font.FONT_OPEN_SANS_LIGHT
        self.my_theme.widget_font_color = (255, 255, 255)
        self.my_theme.widget_font_background_color = (0, 0, 0)
        self.my_theme.widget_font_size = 20
        self.my_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT

        # creating menu
        self.menu = pygame_menu.Menu(
            "Moves List", 250, HEIGHT // 2, position=(95, 10), theme=self.my_theme
        )

        # id of each label
        self.curr_idx = 0

        # half or full move
        self.turn = 0

        # previous move
        self.prev_move = None

    # blit methods

    def show_bg(self, surface):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(str(ROWS - row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)

                # col coordinates
                if row == 7:
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    # blit
                    surface.blit(lbl, lbl_pos)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.transform.smoothscale(
                            pygame.image.load(piece.texture), (50, 50)
                        )
                        img_center = (
                            col * SQSIZE + SQSIZE // 2,
                            row * SQSIZE + SQSIZE // 2,
                        )
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                # color
                color = (
                    theme.moves.light
                    if (move.final.row + move.final.col) % 2 == 0
                    else theme.moves.dark
                )
                # rect
                rect = (
                    move.final.col * SQSIZE,
                    move.final.row * SQSIZE,
                    SQSIZE,
                    SQSIZE,
                )
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = (
                    theme.trace.light
                    if (pos.row + pos.col) % 2 == 0
                    else theme.trace.dark
                )
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = (
                self.hovered_sqr.col * SQSIZE,
                self.hovered_sqr.row * SQSIZE,
                SQSIZE,
                SQSIZE,
            )
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    def show_moves_list(self, surface, move=None):
        menu = self.menu

        if move:
            if self.turn % 2 == 0:
                menu.add.label(
                    f"{self.curr_idx+1}. {move}", max_char=0, label_id=str(self.curr_idx)
                ).set_position(0, -100)
                self.prev_move = move

                # switch to full move
                self.turn += 1

            else:
                label = menu.get_widget(str(self.curr_idx))
                label.set_title(f"{self.curr_idx+1}. {self.prev_move}\t\t\t\t\t{move}")
                self.curr_idx += 1
                self.prev_move = None

                # switch to half move
                self.turn += 1

        menu.draw(surface)
        

    # other methods

    def next_turn(self):
        self.next_player = "white" if self.next_player == "black" else "black"

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()
