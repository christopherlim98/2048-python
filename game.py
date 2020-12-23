import sys
def main():
    board = initialise_board()
    print_board(board)

    while True:
        # Checks if game over
        if game_over(board):
            print('here')
            play_new_game()

        # Get player's move
        key = get_key_press()
        direction = check_direction(key)
        if direction == 'invalid': continue
        if check_move_possible(board, direction):
            board = move(board, direction)
        else:
            continue

        # Player's move is successful. Add new random piece.
        clear()
        add_random(board)
        print_board(board)

def initialise_board():
    """Initialise a 4 x 4 board"""
    board = make_board(4)
    # Add the start of the game, there will be 2 random squares
    for _ in range(2):
        add_random(board)
    return board

def check_direction(key):
    """Check direction of getch key press"""
    if (key == 68 or key == 97): #left
        return 'left'
    elif (key == 67 or key == 100): #right
        return 'right'
    elif (key == 65 or key == 119): #up
        return 'up'
    elif (key == 66 or key == 115): #down
        return 'down'
    else:
        return 'invalid'

def play_new_game():
    """Prints game over and asks player if they want to continue"""
    clear()
    print('''Game over.
            Press 'enter' to continue.
            Press 'q' to quit ''')
    while True:
        key = get_key_press()
        if key == 10: #enter
            main()
        if key == 113: #q
            print('Thank you for playing!')
            sys.exit()


def move(board, direction):
    """Move the board pieces in the desired direction"""
    if direction == 'left' or direction == 'right':
        rows = get_nonempty_rows(board) #for left and right
        if direction == 'left':
            return move_up(rows)
        elif direction == 'right':
            return move_down(rows)
    else:
        cols = get_nonempty_cols(board) #for up and down
        if direction == 'up':
            board = move_up(cols)
        elif direction == 'down':
            board = move_down(cols)
        return transpose_board(board)
    return board

def move_up(board):
    """Handle movement: up/left"""
    N = len(board)
    # Perform additions
    for x in range(N):
        offset = 0
        for y in range(len(board[x])-1):
            a = int(board[x][y + offset])
            b = int(board[x][y + 1 + offset])
            if a == b:
                board[x][y + offset] = str(a + b)
                board[x].pop(y+1 + offset)
                offset = offset -1
    for x in range(N):
        row_buffer = N - len(board[x])
        for _ in range(row_buffer):
            board[x].append('x')
    return board

def move_down(board):
    """Handle movement: right/down"""
    N = len(board)
    #Perform additions
    for x in range(N):
        offset = 0
        for y in range(len(board[x])-1, -1 , -1):
            if y - offset <= 0: break
            a = int(board[x][y - offset])
            b = int(board[x][y - 1 - offset])
            if a == b:
                board[x][y - offset] = str(a + b)
                board[x].pop(y - 1 - offset)
                offset = offset + 1
    for x in range(N):
        col_buffer = N - len(board[x])
        for _ in range(col_buffer):
            board[x].insert(0,'x')
    return board

def transpose_board(board):
    """
    Handle transpose operations,
    typically for the 'up' and 'down' directions.
    """
    N = len(board)
    transposed_board = [['']*N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            transposed_board[x][y] = board[y][x]
    return transposed_board


from utils import *

if __name__ == "__main__":
    clear()
    main()

