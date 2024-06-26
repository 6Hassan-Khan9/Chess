import chess
import chess.engine
from chess import Move
from const import *


class AI:

    def __init__(self, AI_state):
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish.exe")
        self.is_active = AI_state

    def play_move(self, initial_row, initial_col, released_row, released_col):
        # get the initial and released squares of the best move
        best_move = self._get_best_move().uci()
        initial = best_move[:2]
        released = best_move[2:]

        # get the initial and released rows & columns
        initial_col = chess.FILE_NAMES.index(str(initial[Dims.COL.value]))
        initial_row = 7 - chess.RANK_NAMES.index(str(initial[Dims.ROW.value]))
        released_col = chess.FILE_NAMES.index(str(released[Dims.COL.value]))
        released_row = 7 - chess.RANK_NAMES.index(str(released[Dims.ROW.value]))

        return (initial_row, initial_col, released_row, released_col)

    def update_AI_board(self, initial_row, initial_col, final_row, final_col):
        # create move
        initial_chess_square = chess.square(initial_col, 7 - initial_row)
        final_chess_square = chess.square(final_col, 7 - final_row)
        move = Move(initial_chess_square, final_chess_square)

        castling_moves = {
            "e1g1": "e1h1",
            "e8g8": "e8h8",
            "e1c1": "e1a1",
            "e8c8": "e8a8",
        }

        if move.uci() in list(castling_moves.keys()):
            if self.board.turn == chess.WHITE and self.board.has_castling_rights(
                chess.WHITE
            ):
                move = Move.from_uci(castling_moves[move.uci()])
            elif self.board.turn == chess.BLACK and self.board.has_castling_rights(
                chess.BLACK
            ):
                move = Move.from_uci(castling_moves[move.uci()])

        # update AI board
        self.board.push(move)

        # print("\n")
        # print(self.board)
        # print("\n")

    def _get_best_move(self):
        move = self.engine.play(self.board, chess.engine.Limit(time=0.1)).move

        castling_moves = {
            "e1g1": "e1h1",
            "e8g8": "e8h8",
            "e1c1": "e1a1",
            "e8c8": "e8a8",
        }

        # in case castling occurs
        uci = move.uci()

        if move.uci() in list(castling_moves.keys()):
            if self.board.turn == chess.WHITE and self.board.has_castling_rights(
                chess.WHITE
            ):
                move = Move.from_uci(castling_moves[move.uci()])
            elif self.board.turn == chess.BLACK and self.board.has_castling_rights(
                chess.BLACK
            ):
                move = Move.from_uci(castling_moves[move.uci()])

        # update AI board
        self.board.push(move)

        return Move.from_uci(uci)

    def quit_engine(self):
        self.engine.quit()

    def get_player_turn(self):
        if self.turn:
            turn = "white" if self.board.turn else "black"
            return turn
        else:
            turn = 1
            return "white"