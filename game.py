import random

class Board:

    state = []

    def __init__(self, state=[]):
        if state:
            self.state=state
        else:
            self.state = [0 for i in range(16)]
            #the game starts with 2 tiles on the board
            self.assign_tile_to_board()
            self.assign_tile_to_board()

    def print_board(self):
        rows = self.rows()
        # a cell is 8 units wide and 1 units high
        divider = '+-------' * 4 + '+'
        print(divider)  # header
        for row in rows:
            row_str = ''
            for tile in row:
                row_str += '| '
                row_str += str(tile).ljust(5, ' ')
                row_str += ' '
            row_str += '|'
            print(row_str)
            print(divider)

    #def __repr__(self):
        #self.print_board()


    def rows(self):
        rows = []
        for i in range(4):
            start = i*4
            row = self.state[start:start + 4]
            rows.append(row)
        return rows

    def cols(self):
        cols = []
        for i in range(4):
            col = []
            for j in range(len(self.state)):
                if j % 4-i == 0:
                    col.append(self.state[j])
            cols.append(col)
        return cols

    def generate_new_tile(self):
        # 90% of new tiles are a 2.  10% are 4.
        return random.choice([2,2,2,2,2,2,2,2,2,4])

    def get_empty_spaces(self):
        '''all the spaces that don't have a value of zero.'''
        empty_spaces = []
        for idx, val in enumerate(self.state):
            if val == 0:
                empty_spaces.append(idx)
        return empty_spaces

    def assign_tile_to_board(self):
        #get the indexes of the empty tiles
        tile = self.generate_new_tile()
        empty_spaces = self.get_empty_spaces()
        space = random.choice(empty_spaces)
        self.state[space] = tile

    def update_state_with_rows(self, rows):
        new_state = []
        for r in rows:
            new_state += r
        self.state = new_state

    def update_state_with_cols(self, cols):
        new_state = []
        for i in range(4):
            for c in cols:
                new_state.append(c[i])
        self.state = new_state


def slide_tiles(tiles):
    new_tiles = []

    for t in tiles:
        if t != 0:
            new_tiles.append(t)

    tile_count = len(new_tiles)
    while tile_count < 4:
        new_tiles.append(0)
        tile_count = len(new_tiles)

    return new_tiles

def merge_tiles(tiles):
    new_tiles = []

    # there are 3 possible merges: 1&2, 2&3, 3&4
    # you can only merge 2&3 if you don't merge 1&2
    # you can only merge 3&4 if you don't merge 2&3

    first_pair  = tiles[0] == tiles[1] and tiles[0] != 0 and tiles[1] != 0
    second_pair = tiles[1] == tiles[2] and tiles[1] != 0 and tiles[2] != 0 and not first_pair
    third_pair  = tiles[2] == tiles[3] and tiles[2] != 0 and tiles[3] != 0 and not second_pair

    if first_pair:
        new_tiles.append(tiles[0] + tiles[1])
    else:
        new_tiles.append(tiles[0])
        new_tiles.append(tiles[1])

    if second_pair:
        new_tiles.pop()
        new_tiles.append(tiles[1] + tiles[2])
    else:
        # tile 1 was added above
        new_tiles.append(tiles[2])

    if third_pair:
        new_tiles.pop()
        new_tiles.append(tiles[2] + tiles[3])
    else:
        # tile 2 was added above
        new_tiles.append(tiles[3])

    tile_count = len(new_tiles)
    while tile_count < 4:
        new_tiles.append(0)
        tile_count = len(new_tiles)

    return new_tiles

def move(board):
    '''this is a general move function that 
    is the foundation for all four move functions. 
    It assumes the data is organized from left to right
    so you have to restructure the data before calling.'''
    new_board = []
    for b in board:
        b1 = slide_tiles(b)
        b2 = merge_tiles(b1)
        new_board.append(b2)
    return new_board

def left(board):
    rows = board.rows()
    new_rows = move(rows)
    board.update_state_with_rows(new_rows)


def right(board):
    '''the trick is to reverse the rows so the 
    move logic works correctly.'''
    rows = board.rows()
    #flip the rows before we process them
    flipped_rows = [list(reversed(r)) for r in rows]
    new_rows = move(flipped_rows)
    #flip them back
    out_rows = [list(reversed(r)) for r in new_rows]
    board.update_state_with_rows(out_rows)


def up(board):
    cols = board.cols()
    new_cols = move(cols)
    board.update_state_with_cols(new_cols)


def down(board):
    '''the trick is to reverse the columns so the 
    move logic works correctly.'''
    cols = board.cols()
    # flip the cols before we process them
    flipped_cols = [list(reversed(r)) for r in cols]
    new_cols = move(flipped_cols)
    # flip them back
    out_cols = [list(reversed(r)) for r in new_cols]
    board.update_state_with_cols(out_cols)

def game_state(board):
    state = 'PLAYING'
    if 2048 in board.state:
        state =  'WON'
    elif not board.get_empty_spaces():
        state = 'LOST'
    
    return state


def main():
    board = Board()
    game_over = False
    while game_over == False:
        board.print_board()

        #get the mover from the user
        move = input("Make a move [(l)eft, (r)ight, (u)p, (d)own, (q)uit]:  ")
        if move in ['l', 'r', 'u', 'd', 'q']:
            if move == 'l':
                left(board)
            if move == 'r':
                right(board)
            if move == 'u':
                up(board)
            if move == 'd':
                down(board)
            if move == 'q':
                print('Bye.')
                game_over = True

        # check the game state
        game = game_state(board)
        if game == 'WON':
            game_over = True
            print('You won :-)')
        elif game == 'LOST':
            game_over = True
            print('You lost :-(')
        else:
            board.assign_tile_to_board()            


if __name__ == "__main__":
    main()

