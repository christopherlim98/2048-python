import sys
def main():
    # Initialise game
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
    board = make_board(4)
    for _ in range(2):
        add_random(board)
    return board

def check_direction(key):
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
    if direction == 'left' or direction == 'right':
        rows = get_nonempty_rows(board)
        if direction == 'left':
            board = move_left(rows)
        elif direction == 'right':
            board = move_right(rows)
    else:
        cols = get_nonempty_cols(board) #for up and down
        if direction == 'up':
            board = move_up(cols)
        elif direction == 'down':
            board = move_down(cols)
    return board


def move_right(rows):
    N = len(rows)
    #Perform additions
    for x in range(N):
        offset = 0
        for y in range(len(rows[x])-1, -1 , -1):
            if y - offset <= 0: break
            a = int(rows[x][y - offset])
            b = int(rows[x][y - 1 - offset])
            if a == b:
                rows[x][y - offset] = str(a + b)
                rows[x].pop(y - 1 - offset)
                offset = offset + 1
    for x in range(N):
        row_buffer = N - len(rows[x])
        for _ in range(row_buffer):
            rows[x].insert(0,'x')
    return rows

def move_left(rows):
    N = len(rows)
    # Perform additions
    for x in range(N):
        offset = 0
        for y in range(len(rows[x])-1):
            a = int(rows[x][y + offset])
            b = int(rows[x][y + 1 + offset])
            if a == b:
                rows[x][y + offset] = str(a + b)
                rows[x].pop(y+1 + offset)
                offset = offset -1
    for x in range(N):
        row_buffer = N - len(rows[x])
        for _ in range(row_buffer):
            rows[x].append('x')
    return rows

def move_up(cols):
    N = len(cols)
    #Perform additions
    for x in range(N):
        offset = 0
        for y in range(len(cols[x])-1):
            a = int(cols[x][y + offset])
            b = int(cols[x][y + 1 + offset])
            if a == b:
                cols[x][y + offset] = str(a + b)
                cols[x].pop(y + 1 + offset)
                offset = offset - 1

    for x in range(N):
        col_buffer = N - len(cols[x])
        for _ in range(col_buffer):
            cols[x].append('x')
    transposed_cols = [['']*N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            transposed_cols[x][y] = cols[y][x]
    return transposed_cols

def move_down(cols):
    N = len(cols)
    #Perform additions
    for x in range(N):
        offset = 0
        for y in range(len(cols[x])-1, -1 , -1):
            if y - offset <= 0: break
            a = int(cols[x][y - offset])
            b = int(cols[x][y - 1 - offset])
            if a == b:
                cols[x][y - offset] = str(a + b)
                cols[x].pop(y - 1 - offset)
                offset = offset + 1
    for x in range(N):
        col_buffer = N - len(cols[x])
        for _ in range(col_buffer):
            cols[x].insert(0,'x')
    transposed_cols = [['']*N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            transposed_cols[x][y] = cols[y][x]
    return transposed_cols



from utils import *

if __name__ == "__main__":
    clear()
    main()

