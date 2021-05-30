"""Four-in-a-Row
A tile-dropping game to get four-in-a-row, similar to Connect Four."""

import sys
EMPTY_SPACE = '.'  # period is easier to count than space
PLAYER_O = "O"
PLAYER_X = "X"

# Note: Update BOARD_TEMPLATE & COLUMN_LABELS if BOARD_WIDTH is changed.
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
COLLUMN_LABELS = "1", "2", "3", "4", "5", "6", "7"

# The template string for displaying the board:
BOARD_TEMPLATE = """1234567
+-------+
|{}{}{}{}{}{}{}|
|{}{}{}{}{}{}{}|
|{}{}{}{}{}{}{}|
|{}{}{}{}{}{}{}|
|{}{}{}{}{}{}{}|
|{}{}{}{}{}{}{}|
+-------+"""


def get_new_board():
    """"""
    pass


def is_winner():
    """"""
    pass


def is_full():
    """"""
    pass


def display_board():
    """"""
    pass


def get_player_move():
    """"""
    pass


def main():
    """Runs a single game of Four-in-a-Row"""
    print("""
    Two players take turns dropping tiles into one of seven columns, trying
    to make Four-in-a-Row horizontally, vertically, or diagonally
    """)

    # Set up a new game
    game_board = get_new_board()
    player = PLAYER_X

    while True:
        display_board()
        player_move = get_player_move()
        game_board[player_move] = player

        # Check if win or tie
        if is_winner():
            print()
            sys.exit()
        elif is_full():
            print()
            sys.exit()

        # Switch turns
        if player == PLAYER_X:
            player = PLAYER_O
        elif player == PLAYER_O:
            player = PLAYER_X


if __name__ == "__main__":
    main()
