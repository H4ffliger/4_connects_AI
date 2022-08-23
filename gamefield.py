import numpy as np

BOARD_COLS = 7
BOARD_ROWS = 6

# Game board object
class GameField():
    def __init__(self):
        self.board = np.array([[0 for c in range(BOARD_COLS)] for r in range(BOARD_ROWS)])
        self.turns = 0
        self.last_move = [-1, -1] # [r, c]

    def print_board(self):        
        #Replace all 1 and 2 and -1
        stringed = ( [list( map(str,i) ) for i in self.board] )

        #print(stringed)

        for i in range(len(self.board)):
            for y in range(len(self.board[0])):
                if (self.board[i][y] == 0):
                    stringed[i][y] = " "
                if (self.board[i][y] == -1):
                    stringed[i][y] = "O"
                if (self.board[i][y] == 1):
                    stringed[i][y] = "X"

        print("\n")
        # Number the columns seperately to keep it cleaner
        for r in range(BOARD_COLS):
            print(f"  ({r+1}) ", end="")
        print("\n")


        # Print the slots of the game board
        for r in range(BOARD_ROWS):
            print('|', end="")
            for c in range(BOARD_COLS):
                #print("1")
                print(f"  {stringed[r][c]}  |", end="")
            print("\n")

        print(f"{'-' * 42}\n")

    def which_turn(self):
        players = [-1, 1]
        return players[self.turns % 2]
    
    def in_bounds(self, r, c):
        return (r >= 0 and r < BOARD_ROWS and c >= 0 and c < BOARD_COLS)

    def turn(self, column):
        # Search bottom up for an open slot
        for i in range(BOARD_ROWS-1, -1, -1):
            if self.board[i][column] == 0:
                self.board[i][column] = self.which_turn()
                self.last_move = [i, column]

                self.turns += 1
                return True

        return False

    def check_winner(self):
        last_row = self.last_move[0]
        last_col = self.last_move[1]
        last_letter = self.board[last_row][last_col]

        # [r, c] direction, matching letter count, locked bool
        directions = [[[-1, 0], 0, True], 
                      [[1, 0], 0, True], 
                      [[0, -1], 0, True],
                      [[0, 1], 0, True],
                      [[-1, -1], 0, True],
                      [[1, 1], 0, True],
                      [[-1, 1], 0, True],
                      [[1, -1], 0, True]]
        
        # Search outwards looking for matching pieces
        for a in range(4):
            for d in directions:
                r = last_row + (d[0][0] * (a+1))
                c = last_col + (d[0][1] * (a+1))

                if d[2] and self.in_bounds(r, c) and self.board[r][c] == last_letter:
                    d[1] += 1
                else:
                    # Stop searching in this direction
                    d[2] = False

        # Check possible direction pairs for '4 pieces in a row'
        for i in range(0, 7, 2):
            if (directions[i][1] + directions[i+1][1] >= 3):
                #self.print_board()
                #print(f"{last_letter} is the winner!")
                return last_letter   

        # Did not find any winners
        return False

def GameBoardF():
    # Initialize the game board
    game = GameField()

    game_over = False
    while not game_over:
        game.print_board()

        # Ask the user for input, but only accept valid turns
        valid_move = False
        while not valid_move:
            user_move = input(f"{game.which_turn()}'s Turn - pick a column (1-{BOARD_COLS}): ")
            try:
                valid_move = game.turn(int(user_move)-1)
            except:
                print(f"Please choose a number between 1 and {BOARD_COLS}")

        # End the game if there is a winner
        game_over = game.check_winner()
        print(game_over)
        print(game.board)

        # End the game if there is a tie
        if not any(-1 in x for x in game.board):
            print("The game is a draw..")
            return


if __name__ == '__main__':
    GameBoardF()