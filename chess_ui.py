import constants as const
import pygame as py


def draw_board(screen):
    """Draws the tiles of the chessboard.

    :param screen: the game screen to draw on
    """
    board_colors = [py.Color('floralwhite'), py.Color('chartreuse4')]

    for rank in range(const.RANKS):
        for file in range(const.FILES):
            py.draw.rect(screen, board_colors[(file + rank) % 2],
                         (file * const.SQUARE_DIMENSION, rank * const.SQUARE_DIMENSION, const.SQUARE_DIMENSION, const.SQUARE_DIMENSION))


def draw_pieces(board, images, screen):
    """Draws the chess pieces on the board.

    :param screen: the game screen to draw on
    :param board: the current chess board with the pieces notated as color_PIECE
    :param images: a map containing the chess pieces notated as color_PIECE with their corresponding image
    """
    for rank in range(const.RANKS):
        for file in range(const.FILES):
            if board[rank][file] is not None:
                screen.blit(images[board[rank][file]],
                            py.Rect(file * const.SQUARE_DIMENSION, rank * const.SQUARE_DIMENSION, const.SQUARE_DIMENSION, const.SQUARE_DIMENSION))


def draw_end_screen(game, screen):
    """Draws a corresponding massage if the game ended.

    :param screen: the game screen to draw on
    :param game: the current game
    """
    if game.game_ended == "Draw":
        text = game.game_ended
    else:
        text = "Black" if game.white_turn else "White"
        text += " Won"

    font = py.font.Font("freesansbold.ttf", 48)

    text_to_draw = font.render(text, True, py.Color('black'), py.Color('white'))

    text_rect = text_to_draw.get_rect()

    text_rect.center = (const.WIGHT // 2, const.HEIGHT // 2)

    screen.blit(text_to_draw, text_rect)


def draw_game(game, images, screen):
    """Draws the current chess game.

    :param screen: the game screen to draw on
    :param game: the current game
    :param images: a map containing the chess pieces notated as color_PIECE with their corresponding image
    """
    draw_board(screen)
    draw_pieces(game.board, images, screen)

    if game.game_ended:
        draw_end_screen(game, screen)

    py.display.flip()
