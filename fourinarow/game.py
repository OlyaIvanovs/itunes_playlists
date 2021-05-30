"""Four-in-a-Row
A tile-dropping game to get four-in-a-row, similar to Connect Four."""

from icecream import ic  # debugging
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
    """Returns a dictionary that represents a Four-in-a-Row board.
    The keys are (column_index, row_index) and the values are one of the "X", "O" or "."(empty)
    """
    board = {}
    for row_index in range(BOARD_HEIGHT):
        for column_index in range(BOARD_WIDTH):
            board[(column_index, row_index)] = EMPTY_SPACE
    return board


def display_board(board):
    """Display board and its tiles on the screen."""
    # List holds all tiles going left to right, top to bottom
    tile_chars = []
    for row_index in range(BOARD_HEIGHT):
        for column_index in range(BOARD_WIDTH):
            tile_chars.append(board[(column_index, row_index)])

    # Display the board
    print(BOARD_TEMPLATE.format(*tile_chars))


def is_winner(player, board):
    """Returns True if player has 4 tiles in a row."""
    # Check for four-in-a-row going across to the right:
    for column_index in range(BOARD_WIDTH-3):
        for row_index in range(BOARD_HEIGHT):
            tile = board[(column_index, row_index)]
            if tile == player:
                for i in range(1, 4):
                    next_tile = board[column_index + i, row_index]
                    if next_tile != tile:
                        break
                    if i == 3:
                        return True

    # Check for four-in-a-row going down
    for column_index in range(BOARD_WIDTH):
        for row_index in range(BOARD_HEIGHT-3):
            tile = board[(column_index, row_index)]
            if tile == player:
                for i in range(1, 4):
                    next_tile = board[column_index, row_index+i]
                    if next_tile != tile:
                        break
                    if i == 3:
                        return True

    # Check for four-in-a-row going right-down
    for column_index in range(BOARD_WIDTH-3):
        for row_index in range(BOARD_HEIGHT-3):
            tile = board[(column_index, row_index)]
            if tile == player:
                for i in range(1, 4):
                    next_tile = board[column_index+i, row_index+i]
                    if next_tile != tile:
                        break
                    if i == 3:
                        return True

    # Check for four-in-a-row going left-down
    for column_index in range(BOARD_WIDTH - 3):
        for row_index in range(BOARD_HEIGHT - 3):
            tile1 = board[(column_index + 3, row_index)]
            tile2 = board[(column_index + 2, row_index + 1)]
            tile3 = board[(column_index + 1, row_index + 2)]
            tile4 = board[(column_index, row_index + 3)]
            if tile1 == tile2 == tile3 == tile4 == player:
                return True


def is_full(board):
    """Return True if the board has no space."""
    for row_index in range(BOARD_HEIGHT):
        for column_index in range(BOARD_WIDTH):
            if board[(row_index, column_index)] == EMPTY_SPACE:
                return False  # Found an empty spaces
    return True  # All spaces are full.


def get_player_move(player_tile, board):
    """Let a player select a column on the board to drop a tile into.
        Returns a tuple of the (column, row) that the tile falls into.
    """
    while True:
        print(f"Player {player_tile}, enter 1 to {BOARD_WIDTH} or QUIT.")
        response = input("> ").upper().strip()

        if response == "QUIT":
            print("Thanks for playing!")
            sys.exit()

        if response not in COLLUMN_LABELS:
            print(f"Enter a number from 1 to {BOARD_WIDTH}")
            continue  # Ask players again for their moves.

        column_index = int(response) - 1  # -1 for 0-based column indexes

        # If the column is full, ask for move again
        if board[(column_index, 0)] != EMPTY_SPACE:
            print("That column is full, select another one.")
            continue

        # Starting from the bottom, find the first empty space
        for row_index in range(BOARD_HEIGHT-1, -1, -1):
            if board[(column_index, row_index)] == EMPTY_SPACE:
                return (column_index, row_index)


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
        display_board(game_board)
        player_move = get_player_move(player, game_board)
        game_board[player_move] = player

        # Check if win or tie
        if is_winner(player, game_board):
            display_board(game_board)  # Display the board one last time
            print(f"Player {player} has won!")
            sys.exit()
        elif is_full(game_board):
            display_board(game_board)  # Display the board one last time
            print("There is a tie!")
            sys.exit()

        # Switch turns
        if player == PLAYER_X:
            player = PLAYER_O
        elif player == PLAYER_O:
            player = PLAYER_X


if __name__ == "__main__":
    main()
