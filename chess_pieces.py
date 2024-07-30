from abc import ABC, abstractmethod
import format_conversions as fc


def directional_moves(starting_position, depth, directions, board):
    """Generates the possible moves a piece can make on the board.

    :param starting_position: a tuple representing the coordinates of the piece on the board
    :param depth: the amount of spaces a piece can move
    :param directions: a list of tuples representing the directions a piece can make
    :param board: the chess board as a 2D list
    :return: a list of tuples representing the coordinates a piece can move on the board
    """
    moves = []

    for direction in directions:
        for iterations in range(1, depth + 1):
            possible_move = tuple(x + y * iterations for x, y in zip(starting_position, direction))

            if not all(0 <= x <= 7 for x in possible_move):
                break

            if board[possible_move[0]][possible_move[1]] is not None:
                if fc.Pieces[board[starting_position[0]][starting_position[1]]].value.color != fc.Pieces[board[possible_move[0]][possible_move[1]]].value.color:
                    moves.append(possible_move)

                break

            moves.append(possible_move)

    return moves


def pawn_directional_moves(starting_position, directions, board, attacking=False):
    """Generate the moves a pawn can make on the board.

    :param starting_position: a tuple representing the coordinates of the pawn on the board
    :param directions: a list of tuples representing the directions the pawn can make
    :param board: the chess board as a 2D list
    :param attacking: rather or not we are the generating the attacking moves the pawn can make or the up moves
    :return: a list of tuples representing the coordinates a piece can move on the board
    """
    moves = []

    for direction in directions:
        possible_move = tuple(x + y for x, y in zip(starting_position, direction))

        if not all(0 <= x <= 7 for x in possible_move):
            continue

        if attacking is False:
            if board[possible_move[0]][possible_move[1]] is not None:
                break

        if attacking is True:
            if board[possible_move[0]][possible_move[1]] is None:
                continue

            if fc.Pieces[board[starting_position[0]][starting_position[1]]].value.color == fc.Pieces[board[possible_move[0]][possible_move[1]]].value.color:
                continue

        moves.append(possible_move)

    return moves


def check_blank_spaces(board, rank, files):
    """Check if the tiles on the rank and the files are empty

    :param board: the chess board
    :param rank: the rank to check at
    :param files: the list of files to check at
    :return: if all the tiles are empty or not
    """
    blank_spaces = [(rank, file) for file in files]

    if all(board[x[0]][x[1]] is None for x in blank_spaces):
        return True

    return False


class ChessPiece(ABC):
    """Abstract class representing a chess piece."""
    def __init__(self, color):
        """Initializes a chess piece.

        :param color: the color of the chess piece
        """
        self.color = color

    @abstractmethod
    def get_valid_moves(self, board, position):
        """Abstract method for getting the available moves of a piece

        :param board: the chess board
        :param position: a tuple representing the coordinates of the piece on the board
        :return: a list of tuples that contains the moves that the piece can make
        """
        pass


class Pawn(ChessPiece):
    """Class representing a pawn"""
    def __init__(self, color):
        """Initializes a pawn piece.

        :param color: the color of the pawn
        """
        self.en_passant = None
        super().__init__(color)

    def get_up_moves(self, board, position):
        """Get any moves in the relative up direction based on the color that the pawn can make.

        :param board: the chess board
        :param position: a tuple representing the coordinates of the pawn on the board
        :return: a list of tuples that contains the castle moves that the pawn can make
        """
        directions = []

        if self.color is fc.Colors.Black:
            directions.append((1, 0))

            if position[0] == 1:
                directions.append((2, 0))
        else:
            directions.append((-1, 0))

            if position[0] == 6:
                directions.append((-2, 0))

        return pawn_directional_moves(position, directions, board)

    def get_attacking_moves(self, board, position):
        """Get any attacking moves that the pawn can make.

        :param board: the chess board
        :param position: a tuple representing the coordinates of the pawn on the board
        :return: a list of tuples that contains the attacking moves that the pawn can make
        """
        directions = [(1, x) for x in [1, -1]] if self.color is fc.Colors.Black else [(-1, x) for x in [1, -1]]

        return pawn_directional_moves(position, directions, board, True)

    def get_en_passant_moves(self, position):
        """Get the en_passant moves that the pawn can make.

        :param position: a tuple representing the coordinates of the pawn on the board
        :return: a list of tuples that contains the en_passant moves that the pawn can make
        """
        en_passant_move = []

        if self.en_passant is None:
            return en_passant_move

        if any(x == self.en_passant for x in [(position[0], position[1] + x) for x in [-1, 1]]):
            en_passant_move = [(self.en_passant[0] - 1 if self.color is fc.Colors.White else self.en_passant[0] + 1, self.en_passant[1])]

        return en_passant_move

    def get_valid_moves(self, board, position):
        """Gets the available moves of a pawn piece.

        :param board: the chess board
        :param position: a tuple representing the coordinates of the pawn on the board
        :return: a list of tuples that contains the moves that the pawn can make
        """
        return self.get_up_moves(board, position) + self.get_attacking_moves(board, position) + self.get_en_passant_moves(position)


class Bishop(ChessPiece):
    """Class representing a bishop"""
    def get_valid_moves(self, board, position):
        """Gets the available moves of a bishop piece.

        :param board: the chess board
        :param position: a tuple representing the coordinates of the bishop on the board
        :return: a list of tuples that contains the moves that the bishop can make
        """
        bishop_directions = [(x, y) for x in [-1, 1] for y in [-1, 1]]

        return directional_moves(position, 7, bishop_directions, board)


class Knight(ChessPiece):
    """Class representing a knight"""
    def get_valid_moves(self, board, position):
        """Gets the available moves of a knight piece.

        :param board: the chess board
        :param position: a tuple representing the coordinates of the knight on the board
        :return: a list of tuples that contains the moves that the knight can make
        """
        knight_directions = [(x, y) for x in [-2, 2] for y in [-1, 1]] + [(y, x) for x in [-2, 2] for y in [-1, 1]]

        return directional_moves(position, 1, knight_directions, board)


class Rook(ChessPiece):
    """Class representing a rook"""
    def get_valid_moves(self, board, position):
        """Gets the available moves of a rook piece.

        :param board: the chess board
        :param position: a tuple representing the coordinates of the rook on the board
        :return: a list of tuples that contains the moves that the rook can make
        """
        rook_directions = [(x, 0) for x in [-1, 1]] + [(0, x) for x in [-1, 1]]

        return directional_moves(position, 7, rook_directions, board)


class Queen(ChessPiece):
    """Class representing a queen"""
    def get_valid_moves(self, board, position):
        """Gets the available moves of a queen piece.

        :param board: the chess board
        :param position: a tuple representing the coordinates of the queen on the board
        :return: a list of tuples that contains the moves that the queen can make
        """
        queen_directions = [(x, 0) for x in [-1, 1]] + [(0, x) for x in [-1, 1]]
        queen_directions += [(x, y) for x in [-1, 1] for y in [-1, 1]]

        return directional_moves(position, 7, queen_directions, board)


class King(ChessPiece):
    """Class representing a king"""
    def __init__(self, color):
        """Initializes a king piece.

        :param color: the color of the king
        """
        self.castles = None
        super().__init__(color)

    def castle_moves(self, board, position):
        """Get any castle moves that the king can make.

        :param board: the chess board
        :param position: a tuple representing the coordinates of the king on the board
        :return: a list of tuples that contains the castle moves that the king can make
        """
        castle_moves = []

        if self.castles is None:
            return castle_moves

        if self.color is fc.Colors.White:
            if self.castles.white_king_castle:
                if check_blank_spaces(board, position[0], [5, 6]):
                    castle_moves.append((position[0], position[1] + 2))

            if self.castles.white_queen_castle:
                if check_blank_spaces(board, position[0], [1, 2, 3]):
                    castle_moves.append((position[0], position[1] - 2))
        else:
            if self.castles.black_king_castle:
                if check_blank_spaces(board, position[0], [5, 6]):
                    castle_moves.append((position[0], position[1] + 2))

            if self.castles.black_queen_castle:
                if check_blank_spaces(board, position[0], [1, 2, 3]):
                    castle_moves.append((position[0], position[1] - 2))

        self.castles = None

        return castle_moves

    def get_valid_moves(self, board, position):
        """Gets the available moves of a king.

        :param board: the chess board
        :param position: a tuple representing the coordinates of the king on the board
        :return: a list of tuples that contains the moves that the king can make
        """
        king_directions = [(x, 0) for x in [-1, 1]] + [(0, x) for x in [-1, 1]]
        king_directions += [(x, y) for x in [-1, 1] for y in [-1, 1]]

        return directional_moves(position, 1, king_directions, board) + self.castle_moves(board, position)
