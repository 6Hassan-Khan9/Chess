import pygame
import sys
import os
from const import *
from game import Game
from square import Square
from move import Move
from AI import AI


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        pygame.display.set_icon(
            pygame.image.load(os.path.join("..", "assets", "chess.png"))
        )
        self.game = Game()
        self.AI = AI()

    def mainloop(self):

        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        AI = self.AI

        while True:
            # show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # if clicked square has a piece ?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                # click release
                elif event.type == pygame.MOUSEBUTTONUP:

                    valid_move = False
                    initial_row, initial_col, released_row, released_col = [None] * 4

                    if dragger.dragging:

                        dragger.update_mouse(event.pos)

                        initial_row = dragger.initial_row
                        initial_col = dragger.initial_col
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # create possible move
                        initial = Square(initial_row, initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valid move ?
                        valid_move = board.valid_move(dragger.piece, move)
                        if valid_move:
                            # normal capture
                            captured = board.squares[released_row][
                                released_col
                            ].has_piece()
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)

                            # update AI board
                            AI.update_AI_board(
                                initial_row,
                                initial_col,
                                released_row,
                                released_col,
                            )

                            print(game.next_player, "Player", move, dragger.piece.name)

                            # sounds
                            game.play_sound(captured)

                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            # next turn
                            game.next_turn()

                    dragger.undrag_piece()

                    # play next move with AI
                    if AI.is_active and valid_move:

                        initial_row, initial_col, released_row, released_col = (
                            AI.play_move(
                                initial_row,
                                initial_col,
                                released_row,
                                released_col,
                            )
                        )
                       
                        # render AI move
                        initial = Square(initial_row, initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # calculate moves for the piece on initial sqaure
                        best_piece = board.squares[initial_row][initial_col].piece
                        board.calc_moves(best_piece, initial_row, initial_col, bool=True)

                        # normal capture
                        captured = board.squares[released_row][released_col].has_piece()
                        board.move(best_piece, move)

                        board.set_true_en_passant(best_piece)

                        # sounds
                        game.play_sound(captured)

                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_pieces(screen)

                        # next turn
                        game.next_turn()

                # key press
                elif event.type == pygame.KEYDOWN:

                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # game reset
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    AI.engine.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.mainloop()
