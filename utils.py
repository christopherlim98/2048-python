import os
import random

try:
    from tkinter import *
    #Assigned to None because import was successful but $DISPLAY may not be set
    gui, GUI_runnable, = None, None
except ImportError:
    gui, GUI_runnable, = False, False

try:
    import getch
except ImportError:
    getch = None

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def make_board(N):
    """Initialise game board that is N * N"""
    assert N >= 1
    return [['x'] * N for _ in range(N)]

def print_board(board):
    N = len(board)
    final = ""
    for x in range(N):
        row = ""
        for y in range(N):
            row += board[x][y] + "\t"
        final +=  row + "\n"
    print(final)
    if GUI_runnable:
        gui.update_grid(board)
        gui.update()

def game_over(board):
    """Checks if there are any valid moves left """
    cols = get_cols(board)
    rows = get_rows(board)
    if check_merge_possible(rows) or check_merge_possible(cols) or check_empty_board(board) :
        return False
    else:
        return True


def get_key_press():
    """
    Get user's move and returns direction
    Valid moves include 'wasd' keys and arrow keys
    """
    return ord(getch.getch())

def add_random(board):
    """
    Add random piece to the board.
    Probability of each piece: 2 (64%), 4 (36%)
    """
    empty = get_empty_cells(board)
    x,y = random.choice(empty)
    board[x][y] = '2'

def get_empty_cells(board):
    empty = []
    N = len(board)
    for x in range(N):
        for y in range(N):
            if board[x][y] == 'x':
                empty.append((x,y))
    return empty

def get_total_score(board):
    """Get the sum of all the pieces on board"""
    N = len(board)
    total = 0
    for x in range(N):
        for y in range(N):
            if board[x][y] != 'x':
                total = total + board[x][y]
    return total

def get_nonempty_cols(board):
    N = len(board)
    cols = []
    for x in range(N):
        col = []
        for y in range(N):
            if board[y][x] != 'x':
                col.append(board[y][x])
        cols.append(col)
    return cols

def get_nonempty_rows(board):
    rows = []
    N = len(board)
    for x in range(N):
        row = []
        for y in range(N):
            if board[x][y] != 'x':
                row.append(board[x][y])
        rows.append(row)
    return rows

def get_cols(board):
    N = len(board)
    cols = []
    for x in range(N):
        col = []
        for y in range(N):
            col.append(board[y][x])
        cols.append(col)
    return cols

def get_rows(board):
    rows = []
    N = len(board)
    for x in range(N):
        row = []
        for y in range(N):
            row.append(board[x][y])
        rows.append(row)
    return rows

def check_move_possible(board, direction):
    """
    A valid move occurs in two scenarios
    1. There is space in the direction of movement
    2. There is something that can be merged.
    """
    if direction == 'up' or direction == 'down':
       return check_cols(board, direction)
    if direction == 'left' or direction == 'right':
        return check_rows(board, direction)
    return False

def check_merge_possible(board):
    N = len(board)
    # Check if merge is possible
    for x in range(N):
        for y in range(N-1):
            if board[x][y]!='x' and board[x][y] == board[x][y+1]: return True
    return False

def check_cols(board, direction):
    cols = get_cols(board)
    # Check for possible merge
    if check_merge_possible(cols): return True
    # Check if there is an empty space
    if direction == 'down':
        return check_down(cols)
    elif direction == 'up':
        return check_up(cols)

def check_rows(board, direction):
    rows = get_rows(board)
    # Check for possible merge
    if check_merge_possible(rows): return True
    # Check if there is an empty space
    if direction == 'right':
        return check_down(rows)
    elif direction == 'left':
        return check_up(rows)

def check_down(cols):
    N = len(cols)
    for x in range(N):
        for y in range(N):
            if cols[x][y] != 'x':
                for i in range(y+1, N, 1):
                    if cols[x][i] == 'x': return True
    return False

def check_up(cols):
    N = len(cols)
    for x in range(N):
        for y in range(N):
            if cols[x][y] != 'x':
                for i in range(y, -1, -1):
                    if cols[x][i] == 'x': return True
    return False

def check_empty_board(board):
    N = len(board)
    for x in range(N):
        for y in range(N):
            if board[x][y] == 'x': return True
    return False

class gui_2048(Frame):
    """
    Taken from https://github.com/kmishra9/2048-Starter/blob/master/utils.py
    """

    def __init__(self,master = None):
        Frame.__init__(self,master)

        #Background and font colors for each number upto 8192.
        self.background_color = {'2':'#EBE1D7','4':'#ECE0CA','8':'#F4B176','16':'#F7975C','32':'#FA7961','64':'#F2613C','128':'#EBE899','256':'#F0D069','512':'#EBE544','1024':'#EAC80D','2048':'#F4FC08','4096':'#A4FC0D','8192':'#FC0D64'}
        self.foreground_color = {'2':'#857865','4':'#857865','8':'#FDF5E9','16':'#FDF5E9','32':'#FDF5E9','64':'#FDF5E9','128':'#FDF5E9','256':'#FDF5E9','512':'#FDF5E9','1024':'#FDF5E9','2048':'#FDF5E9','4096':'#FDF5E9','8192':'#FDF5E9'}

        #support window resizing
        self.grid(sticky = N+S+E+W)

        #Adding the size of the board to create. This may be changed anytime to get a different sized board
        self.board_size = 4

        #matrix_numbers is a list of frames (N x N frames) where N is board_size
        self.matrix_numbers = list()

        #initializing the GUI without any numbers (Starting point)
        self.create_grid(self.board_size)


    def create_grid(self,board_size):

        #creating one frame for the whole window
        f = Frame(self,width = 600,height = 600, bg = '#BBADA0',borderwidth = 5)

        #support window resizing each frame
        f.grid(sticky = N+S+E+W)

        #Adding frames inside the main frame f for each grid point along with its background and font color
        for i in range(int(board_size)):
            label_row = []
            for j in range(int(board_size)):
                frames = Frame(f, bg = '#EEE4DA',height = 150, width = 150,relief = SUNKEN)
                frames.grid(row=i, column=j,padx = 5, pady = 5,sticky = N+S+E+W)
                each_label = Label(f, text = "",background = "#EEE4DA",font = ("Arial",55),justify = CENTER)
                each_label.grid(row=i, column=j,padx = 5, pady = 5, sticky = N+S+E+W)
                label_row.append(each_label)
            self.matrix_numbers.append(label_row)

    #update function that updates the number matrix after every loop in the main function
    def update_grid(self,board):
        assert len(board) == self.board_size
        for x in range(len(board)):
            for y in range(len(board)):
                if board[x][y] == 'x':
                    self.matrix_numbers[x][y].configure(text = '',bg = '#EEE4DA')
                else:
                    self.matrix_numbers[x][y].configure(text = str(board[x][y]),bg = self.background_color[board[x][y]
                    ],fg = self.foreground_color[board[x][y]])


class _Getch:
    """
    Taken from https://code.activestate.com/recipes/134892/
    Gets a single character from standard input.  Does not echo to the screen.
    """
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

if GUI_runnable == None:
    try:
        root = Tk()
        gui = gui_2048(root)
        GUI_runnable = True
    except:
        GUI_runnable = False

if getch == None:
    getch = _Getch()