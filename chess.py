import sys
import time

import pygame as py
import constants as const
import chess_engine as ce
import chess_ui as ui
import format_conversions as fc


def get_player_type():
    """Gets the type of chess player you will be against.

    :return: return which type of player (human or AI)
    """
    try:
        valid_player_types = ['player', 'ai']

        type_of_player = sys.argv[1]

        if type_of_player not in valid_player_types:
            raise ValueError("invalid player type")

        return type_of_player

    except Exception as e:
        print(f"error: {e}")

        return 'player'


def initialize_game_window():
    """Initializes the game window using pygame.

    :return: the game window
    """
    py.init()

    game_screen = py.display.set_mode((const.WIGHT, const.HEIGHT))

    py.display.set_caption("Chess")

    icon = py.image.load('images\\chess_icon.png')
    py.display.set_icon(icon)

    return game_screen


if __name__ == '__main__':
    """The main loop of the chess game"""

    screen = initialize_game_window()

    piece_images = {piece.name: py.transform.scale(py.image.load('images\\chess_pieces\\' + piece.name + ".png"),
                                                   (const.SQUARE_DIMENSION, const.SQUARE_DIMENSION)) for piece in fc.Pieces}

    clock = py.time.Clock()

    player_type = get_player_type()

    chess_game = ce.ChessBoard(player_type)
    clicks_manager = ce.ClicksManager(chess_game)

    running = True
    while running:
        if player_type == "ai":
            if (chess_game.ai_color is fc.Colors.White and chess_game.white_turn) or (chess_game.ai_color is fc.Colors.Black and not chess_game.white_turn):
                chess_game.make_ai_move()

        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            elif event.type == py.MOUSEBUTTONDOWN:
                clicks_manager.process_click(py.mouse.get_pos())

        ui.draw_game(chess_game, piece_images, screen)

        if chess_game.game_ended:
            time.sleep(1)

            running = False

        clock.tick(const.FRAME_RATE)
