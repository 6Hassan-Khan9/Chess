import pygame
import pygame_menu
import pygame_menu.widgets
from pygame_menu.widgets import ScrollBar
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

        # adding header label 
        self.heading_surface = pygame.Surface((150, 100))
        self.move_list_title = pygame_menu.widgets.Label("Move List").set_font(font=pygame_menu.font.FONT_OPEN_SANS_LIGHT, font_size=25, color=(255, 255, 255), selected_color=(255, 255, 255), readonly_color=(255, 255, 255), readonly_selected_color=(255, 255, 255), background_color=(0, 0, 0)).set_position(10, 10)
        self.move_list_title.draw(self.heading_surface)

        # adding scroll guide label (first line)
        self.scroll_guide_surface = pygame.Surface((200, 150))
        self.scroll_guide_title = pygame_menu.widgets.Label("Press the arrow").set_font(font=pygame_menu.font.FONT_OPEN_SANS_LIGHT, font_size=15, color=(255, 255, 255), selected_color=(255, 255, 255), readonly_color=(255, 255, 255), readonly_selected_color=(255, 255, 255), background_color=(26, 7, 14)).set_position(5, 0)
        self.scroll_guide_title.draw(self.scroll_guide_surface)
        # adding scroll guide label (second line)
        self.scroll_guide_title = pygame_menu.widgets.Label("keys to scroll.").set_font(font=pygame_menu.font.FONT_OPEN_SANS_LIGHT, font_size=15, color=(255, 255, 255), selected_color=(255, 255, 255), readonly_color=(255, 255, 255), readonly_selected_color=(255, 255, 255), background_color=(26, 7, 14)).set_position(15, 20)
        self.scroll_guide_title.draw(self.scroll_guide_surface)

        # adding control labels
        self.reset_label = pygame_menu.widgets.Label("Press 'r' to reset.").set_font(font=pygame_menu.font.FONT_OPEN_SANS_ITALIC, font_size=15, color=(255, 255, 255), selected_color=(255, 255, 255), readonly_color=(255, 255, 255), readonly_selected_color=(255, 255, 255), background_color=(0, 0, 0)).set_position(5, 0).set_position(WIDTH+10, 400)

        self.theme_label = pygame_menu.widgets.Label("Press 't' to change theme.").set_font(font=pygame_menu.font.FONT_OPEN_SANS_ITALIC, font_size=15, color=(255, 255, 255), selected_color=(255, 255, 255), readonly_color=(255, 255, 255), readonly_selected_color=(255, 255, 255), background_color=(0, 0, 0)).set_position(15, 20).set_position(WIDTH+10, 430)
        
        self.quit_label = pygame_menu.widgets.Label("Press 'q' to escape to menu.").set_font(font=pygame_menu.font.FONT_OPEN_SANS_ITALIC, font_size=15, color=(255, 255, 255), selected_color=(255, 255, 255), readonly_color=(255, 255, 255), readonly_selected_color=(255, 255, 255), background_color=(0, 0, 0)).set_position(15, 20).set_position(WIDTH+10, 460)
        

        # creating move list surface 
        self.move_list_actual_size = (150, HEIGHT * 100)
        self.move_list_size = (150, 220)
        self.move_list_surface = pygame.Surface(self.move_list_actual_size)

        # current move
        self.current_move = pygame_menu.widgets.Label("").set_font(font=pygame_menu.font.FONT_OPEN_SANS_LIGHT, font_size=15, color=(255, 255, 255), selected_color=(255, 255, 255), readonly_color=(255, 255, 255), readonly_selected_color=(255, 255, 255), background_color=(0, 0, 0)).set_position(0, 0)

        # shifting move list
        self.count_moves = 0
        self.factor = 0
        self.show_scroll_guide = False
        
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
                

        self.reset_label.draw(surface)
        self.theme_label.draw(surface)
        self.quit_label.draw(surface)           

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

    def show_moves_list(self, surface, move=None, event=None):
        current_move = self.current_move
        heading_surface = self.heading_surface
        move_list_surface = self.move_list_surface
        scroll_guide_surface = self.scroll_guide_surface
        push_next_move = False

        if move:
            if self.turn % 2 == 0:
                offset = 20 if (self.count_moves) else 0
                current_move.set_title(f"{self.curr_idx+1}. {move.ljust(6, ' ')}").set_position(current_move.get_position()[0], current_move.get_position()[1]+offset)
                self.prev_move = move.ljust(6, ' ')

                # switch to full move
                self.turn += 1

            else:
                current_move.set_title(f"{self.curr_idx+1}. {self.prev_move}\t{move.rjust(6, ' ')}")
                self.curr_idx += 1
                self.prev_move = None
                self.count_moves += 1

                if (self.count_moves >= 11):
                    push_next_move = True
                    self.show_scroll_guide = True

                # switch to half move
                self.turn += 1
        
        if (push_next_move):
            self.factor += 20
        if (self.show_scroll_guide):
            surface.blit(scroll_guide_surface, (WIDTH+160, 100))
        
        surface.blit(heading_surface, (WIDTH, 0))
        current_move.draw(move_list_surface)
        surface.blit(move_list_surface, (WIDTH+10, 50), pygame.Rect((0, self.factor), self.move_list_size))

    def scroll_moves_list(self, surface, direction=1, move=None, event=None):
        move_list_surface = self.move_list_surface
        count_moves = self.count_moves
        min_scroll_size = 0
        max_scroll_size = (count_moves-11) * 20

        if (count_moves < 11):
            return
        elif (self.factor == min_scroll_size and direction == 1):
            self.factor += 20
        elif (self.factor == max_scroll_size and direction == -1):
            self.factor -= 20
        elif (self.factor > min_scroll_size and self.factor > max_scroll_size and direction == -1):
            self.factor -= 20 
        elif (self.factor < min_scroll_size and self.factor < max_scroll_size and direction == 1):
            self.factor += 20 
        elif (self.factor > min_scroll_size and self.factor < max_scroll_size):
            self.factor += 20 * direction

        # print(max_scroll_size, self.factor)

        surface.blit(move_list_surface, (WIDTH+10, 50), pygame.Rect((0, self.factor), self.move_list_size))

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
