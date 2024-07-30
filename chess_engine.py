import copy
import random

import format_conversions as fc
import constants as const
import chess_pieces as cp


def get_board_from_fen(fen):
    """Initializes a chess board from a FEN string.

    :param fen: a string represented in the FEN notation
    :return: a chess board with elements as color_PIECE
    """
    board_files = []

    for fen_rank in fen.split("/"):
        board_rank = []

        for character in fen_rank:
            if character.isdigit():
                board_rank.extend([None] * int(character))
                continue

            board_rank.append(fc.FenToPiece[character].value)

        board_files.append(board_rank)

    return board_files


class Castles:
    """Class representing the castle moves for a chess game."""
    def __init__(self):
        self.black_king_castle = True
        self.black_queen_castle = True
        self.white_king_castle = True
        self.white_queen_castle = True


class ChessBoard:
    """Class responsible with the logic and management of a chess game."""
    def __init__(self, player_type, fen=const.STARTING_FEN):
        self.board = get_board_from_fen(fen)
        self.previous_board = None
        self.white_turn = True
        self.castles = Castles()
        self.en_passant = None
        self.game_ended = None
        self.ai_color = None if player_type == "player" else random.choice(list(fc.Colors))

    def check_for_promotions(self):
        """Checks if there is any pawns on the last ranks and makes them into queen pieces"""
        for last_ranks_index in [0, 7]:
            for file_index in range(const.FILES):
                if self.board[last_ranks_index][file_index] is None:
                    continue

                if self.board[last_ranks_index][file_index].endswith("P"):
                    self.board[last_ranks_index][file_index] = self.board[last_ranks_index][file_index][:-1] + "Q"

    def update_castles(self, starting_position):
        """Updates the castle moves that can no longer be made"""
        if starting_position == (7, 4):
            self.castles.white_king_castle = False
            self.castles.white_queen_castle = False

        if starting_position == (0, 4):
            self.castles.black_king_castle = False
            self.castles.black_queen_castle = False

        if starting_position == (7, 0):
            self.castles.white_queen_castle = False

        if starting_position == (7, 7):
            self.castles.white_king_castle = False

        if starting_position == (0, 0):
            self.castles.black_queen_castle = False

        if starting_position == (0, 7):
            self.castles.black_king_castle = False

    def update_en_passant(self, starting_position, desired_position):
        """Updates the possibility of an en_passant move for the next turn if a pawn is moved 2 ranks up"""
        if self.board[desired_position[0]][desired_position[1]] is None:
            self.en_passant = None

            return

        if isinstance(fc.Pieces[self.board[desired_position[0]][desired_position[1]]].value, cp.Pawn):
            if abs(starting_position[0] - desired_position[0]) == 2:
                self.en_passant = desired_position

                return

        self.en_passant = None

    def verify_checkmate_stalemate(self, verify_checkmate=True):
        """Verifies if the current player is checkmated or is in stalemate.

        :param verify_checkmate: if it's looking for checkmate or stalemate
        :return: if the current player is in checkmate/stalemate or not
        """
        current_player_color = fc.Colors.White if self.white_turn else fc.Colors.Black

        self.previous_board = copy.deepcopy(self.board)

        if verify_checkmate:
            if not self.king_in_check():
                return False
        else:
            if self.king_in_check():
                return False

        for rank_index in range(const.RANKS):
            for file_index in range(const.FILES):
                if self.board[rank_index][file_index] is None:
                    continue

                current_piece_color = fc.Colors.White if self.board[rank_index][file_index][0] == 'w' else fc.Colors.Black

                if current_piece_color is current_player_color:
                    starting_position = rank_index, file_index

                    current_piece_possible_moves = self.get_possible_moves(starting_position, verify_checkmate)

                    for current_piece_possible_move in current_piece_possible_moves:
                        self.simulate_move(starting_position, current_piece_possible_move)

                        if not self.king_in_check():
                            self.board = copy.deepcopy(self.previous_board)

                            return False

                        self.board = copy.deepcopy(self.previous_board)

        return True

    def get_king_position(self, color):
        """Gets the position of the king.

        :param color: the color of the king to look for
        :return: a tuple representing the coordinates of the king on the board
        """
        king_notation = "w_K" if color is fc.Colors.White else "b_K"

        for rank_index, rank in enumerate(self.board):
            for file_index, file in enumerate(rank):
                if file is king_notation:
                    return rank_index, file_index

    def king_in_check(self):
        """Checks rather or not the king is being in check.

        :return: if the king is checked or not
        """
        current_player_color = fc.Colors.White if self.white_turn else fc.Colors.Black

        king_position = self.get_king_position(current_player_color)

        attacking_moves = set()

        for rank_index in range(const.RANKS):
            for file_index in range(const.FILES):
                if self.board[rank_index][file_index] is None:
                    continue

                current_piece_color = fc.Colors.White if self.board[rank_index][file_index][0] == 'w' else fc.Colors.Black

                if current_piece_color is not current_player_color:
                    attacking_moves |= set(self.get_possible_moves((rank_index, file_index), True))

        return king_position in attacking_moves

    def choose_random_piece(self, color):
        """Chooses a random piece from all available pieces on the table of a color.

        :param color: the color of pieces to look for
        :return: a tuple representing the coordinates of the piece randomly choose
        """
        possible_pieces = []

        for rank_index in range(const.RANKS):
            for file_index in range(const.FILES):
                if self.board[rank_index][file_index] is None:
                    continue

                current_piece_color = fc.Colors.White if self.board[rank_index][file_index][0] == 'w' else fc.Colors.Black

                if current_piece_color is color:
                    possible_pieces.append((rank_index, file_index))

        return random.choice(possible_pieces)

    def make_ai_move(self):
        """The AI that makes random correct moves."""
        while (self.ai_color is fc.Colors.White and self.white_turn) or (self.ai_color is fc.Colors.Black and not self.white_turn):
            starting_position = self.choose_random_piece(self.ai_color)

            possible_moves = self.get_possible_moves(starting_position, self.king_in_check())

            if not possible_moves:
                continue

            random_desired_move = random.choice(possible_moves)

            self.game_logic(starting_position, random_desired_move)

    def simulate_move(self, starting_position, desired_position):
        """Makes a move on the board. It also checks if the move is en_passant or castle, so it can be made accordingly

        :param starting_position: a tuple of the coordinates that the piece is on
        :param desired_position: a tuple of the coordinates to the position that the piece will end up on
        """
        if isinstance(fc.Pieces[self.board[starting_position[0]][starting_position[1]]].value, cp.Pawn):
            if self.board[desired_position[0]][desired_position[1]] is None and abs(
                    starting_position[1] - desired_position[1]) == 1:
                self.board[starting_position[0]][desired_position[1]] = None

        if isinstance(fc.Pieces[self.board[starting_position[0]][starting_position[1]]].value, cp.King):
            if abs(starting_position[1] - desired_position[1]) == 2:
                file_changes = (0, desired_position[1] + 1) if desired_position[1] < 4 else (7, desired_position[1] - 1)

                self.simulate_move((starting_position[0], file_changes[0]), (desired_position[0], file_changes[1]))

        self.board[desired_position[0]][desired_position[1]] = self.board[starting_position[0]][starting_position[1]]
        self.board[starting_position[0]][starting_position[1]] = None

    def get_possible_moves(self, position, king_is_checked):
        """Gets the possible moves of a certain piece.

        :param position: the position on the board of the piece
        :param king_is_checked: if the current player is in checked at the moment or not
        :return: a list of tuples that represents the coordinates on the board of the possibles moves that can be made
        """
        piece_type = self.board[position[0]][position[1]]

        if isinstance(fc.Pieces[piece_type].value, cp.Pawn):
            fc.Pieces[piece_type].value.en_passant = self.en_passant

        if isinstance(fc.Pieces[piece_type].value, cp.King):
            if not king_is_checked:
                fc.Pieces[piece_type].value.castles = self.castles

        return fc.Pieces[piece_type].value.get_valid_moves(self.board, position)

    def game_logic(self, starting_position, desired_position):
        """The logic of the chess engine"""
        self.previous_board = copy.deepcopy(self.board)

        possible_moves = self.get_possible_moves(starting_position, self.king_in_check())

        if desired_position not in possible_moves:
            return

        self.simulate_move(starting_position, desired_position)

        if self.king_in_check():
            self.board = copy.deepcopy(self.previous_board)
            return

        self.check_for_promotions()

        self.update_castles(starting_position)

        self.update_en_passant(starting_position, desired_position)

        self.white_turn = not self.white_turn

        if self.verify_checkmate_stalemate():
            self.game_ended = "Checkmate"
            return

        if self.verify_checkmate_stalemate(verify_checkmate=False):
            self.game_ended = "Draw"
            return


class ClicksManager:
    """Class responsible with managing the clicks that the players are making"""
    def __init__(self, chess_game):
        self.chess_game = chess_game
        self.starting_move = None

    def process_click(self, click):
        """Process a player's click on the chessboard and sends it to the game engine.

        :param click: a tuple of coordinates of the clicked position
        """
        click_y_coord, click_x_coord = tuple(value // const.SQUARE_DIMENSION for value in click)

        clicked_piece_color = None

        if self.chess_game.board[click_x_coord][click_y_coord] is not None:
            clicked_piece_color = fc.Colors.White if self.chess_game.board[click_x_coord][click_y_coord].startswith("w") else fc.Colors.Black

        player_to_move_color = fc.Colors.White if self.chess_game.white_turn else fc.Colors.Black

        if self.starting_move is None:
            if self.chess_game.board[click_x_coord][click_y_coord] is None:
                return

            if clicked_piece_color is not player_to_move_color:
                return

            self.starting_move = (click_x_coord, click_y_coord)
        else:
            if clicked_piece_color is player_to_move_color:
                self.starting_move = (click_x_coord, click_y_coord)
                return

            self.chess_game.game_logic(self.starting_move, (click_x_coord, click_y_coord))
            self.starting_move = None
