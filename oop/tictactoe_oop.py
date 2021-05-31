# tictactoe_oop.py, an object-oriented tic-tac-toe game.

ALL_SPACES = list('123456789')  # The keys for a TTT board dictionary
X, O, BLANK = 'X', 'O', ' '  # Constants for string values


class TTTBoard:
    def __init__(self, usePrettyBoard=False, useLogging=False):
        """Create a new blanc tic-tac-toe board"""
        self.board = {}
        for space in ALL_SPACES:
            self.board[space] = BLANK

    def get_board_str(self):
        """Return text-represantation of board."""
        return f'''
        {self.board['1']}|{self.board['2']}|{self.board['3']} 1 2 3
        -+-+-
        {self.board['4']}|{self.board['5']}|{self.board['6']} 4 5 6
        -+-+-
        {self.board['7']}|{self.board['8']}|{self.board['9']} 7 8 9
        '''

    def update(self, space, player_mark):
        """Sets the space on the board to mark."""
        self.board[space] = player_mark

    def is_valid_space(self, space):
        """Return True if the space is valid and it is blank."""
        if space in ALL_SPACES and self.board[space] == BLANK:
            return True

    def is_full(self):
        """Return True if no fre space on a board."""
        for space in ALL_SPACES:
            if self.board[space] != BLANK:
                return False
        return True

    def is_winner(self, player):
        """Return True if player is a winner."""
        b, p = self.board, player  # Shorter names as "syntactic sugar".
        # Check for 3 marks across the 3 rows, 3 columns, and 2 diagonals.
        return ((b['1'] == b['2'] == b['3'] == p) or  # Across the top
                (b['4'] == b['5'] == b['6'] == p) or  # Across the middle
                (b['7'] == b['8'] == b['9'] == p) or  # Across the bottom
                (b['1'] == b['4'] == b['7'] == p) or  # Down the left
                (b['2'] == b['5'] == b['8'] == p) or  # Down the middle
                (b['3'] == b['6'] == b['9'] == p) or  # Down the right
                (b['3'] == b['5'] == b['7'] == p) or  # Diagonal
                (b['1'] == b['5'] == b['9'] == p))  # Diagonal


def main():
    """Run tic-tac-toe game"""
    print("Welcome to tic-tac-toe game!")
    game_board = TTTBoard()  # Create a TTT board object.
    current_player, next_player = X, O  # X goes first

    while True:
        print(game_board.get_board_str())  # Display board

        # Keep asking the player until they enter a number 1-9
        move = None
        while not game_board.is_valid_space(move):
            print(f'What is {current_player}\'s move? (1-9)')
            move = input()

        game_board.update(move, current_player)  # Make the move

        # Check if game is over
        if game_board.is_winner(current_player):
            print(game_board.get_board_str())  # Display board
            print(f"{current_player} has won the game!")
            break
        elif game_board.is_full():
            print(game_board.get_board_str)  # Display board
            print("The game is tie!")
            break
        # Switch turns
        current_player, next_player = next_player, current_player
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
