import pygame
import pygame_menu
import sys
import os
from const import *
from dragger import Dragger
from square import Square
from piece import Pawn
from config import Config
from sound import Sound


class Selection:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Electronic Chess")
        pygame.display.set_icon(
            pygame.image.load(os.path.join("..", "assets", "images", "wolf-menu.png"))
        )
        self.selected_side = None
        self.hovered_sqr = None
        self.dragger = Dragger()
        self.config = Config()
        self.config.change_theme()
        self.label = pygame_menu.widgets.Label("Choose Your Side")
        self.label.set_alignment(pygame_menu.locals.ALIGN_CENTER)
        self.label.set_font(
            pygame_menu.font.FONT_OPEN_SANS_LIGHT,
            48,
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            (255, 255, 255),
            (0, 0, 0),
            True,
        )
        self.label.set_position(50 + (WIDTH // COLS), 5 * (WIDTH // COLS))

    def fade_in(self):
        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.fill((0, 0, 0))
        for alpha in range(255, 0, -1):
            fade.set_alpha(alpha)
            self.draw_window()
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(1)

    def show_bg(self, surface):
        theme = self.config.theme

        for row, col in ((3, 3), (3, 4)):
            # color
            color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
            # rect
            rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row, col in ((3, 3), (3, 4)):

            piece = Pawn("white") if (row, col) == (3, 3) else Pawn("black")

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

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (18, 166, 60)
            # rect
            rect = (
                self.hovered_sqr.col * SQSIZE,
                self.hovered_sqr.row * SQSIZE,
                SQSIZE,
                SQSIZE,
            )
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    def set_hover(self, row, col):

        self.hovered_sqr = Square(row, col) if (row, col) in ((3, 3), (3, 4)) else None

    def show_label(self, surface):
        self.label.draw(surface)

    def draw_window(self):

        screen = self.screen

        self.show_bg(screen)
        self.show_pieces(screen)
        self.show_hover(screen)
        self.show_label(screen)

    def play_sound(self):
        selection_sound = Sound(os.path.join("..", "assets", "sounds", "click.mp3"))
        selection_sound.play()

    def mainloop(self):

        # fade into the selection screen from main menu
        self.fade_in()

        screen = self.screen
        dragger = self.dragger
        running = True

        while running:

            self.show_bg(screen)
            self.show_pieces(screen)
            self.show_hover(screen)
            self.show_label(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # if clicked square has a piece ?
                    is_white = (clicked_row, clicked_col) == (3, 3)
                    is_black = (clicked_row, clicked_col) == (3, 4)
                    has_piece = is_white or is_black
                    if has_piece:
                        piece = Pawn("white") if is_white else Pawn("black")
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)
                        # show methods
                        self.show_bg(screen)
                        self.show_pieces(screen)

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    self.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        self.show_bg(screen)
                        self.show_pieces(screen)
                        self.show_hover(screen)

                # click release
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:

                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # valid selection ?
                        is_white = (released_row, released_col) == (3, 3)
                        is_black = (released_row, released_col) == (3, 4)
                        valid_move = is_white or is_black
                        if valid_move:

                            self.selected_side = "white" if is_white else "black"

                            # sounds
                            self.play_sound()

                            # show methods
                            self.show_bg(screen)
                            self.show_pieces(screen)

                            # quit selection screen
                            running = False

                    dragger.undrag_piece()

                # key press
                elif event.type == pygame.KEYDOWN:

                    # return to main menu
                    if event.key == pygame.K_q:
                        running = False

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

        return self.selected_side


if __name__ == "__main__":
    selection = Selection()
    selection.mainloop()
