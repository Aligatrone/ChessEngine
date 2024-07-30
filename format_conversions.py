from enum import Enum
import chess_pieces as cp


class Colors(Enum):
    """Enumeration representing the possible chess colors."""
    Black = 'b'
    White = 'w'


class Pieces(Enum):
    """Enumeration mapping pieces on the chessboard to the corresponding chess piece classes."""
    b_B = cp.Bishop(Colors.Black)
    b_K = cp.King(Colors.Black)
    b_N = cp.Knight(Colors.Black)
    b_P = cp.Pawn(Colors.Black)
    b_Q = cp.Queen(Colors.Black)
    b_R = cp.Rook(Colors.Black)
    w_B = cp.Bishop(Colors.White)
    w_K = cp.King(Colors.White)
    w_N = cp.Knight(Colors.White)
    w_P = cp.Pawn(Colors.White)
    w_Q = cp.Queen(Colors.White)
    w_R = cp.Rook(Colors.White)


class FenToPiece(Enum):
    """Enumeration mapping FEN notation to corresponding color_PIECE notation."""
    b = 'b_B'
    k = 'b_K'
    n = 'b_N'
    p = 'b_P'
    q = 'b_Q'
    r = 'b_R'
    B = 'w_B'
    K = 'w_K'
    N = 'w_N'
    P = 'w_P'
    Q = 'w_Q'
    R = 'w_R'
