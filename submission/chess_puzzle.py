from typing import Union
import copy
import random
import os.path

def location2index(loc: str) -> tuple[int, int]:
    '''converts chess location to corresponding x and y coordinates
    
    Parameters:
        loc (str): string of coordinates x,y in plain configuration
    Returns:
        tuple[int, int]: tuple of coordinates in index form x,y
    '''
    column = ord(loc[0]) - ord('a') + 1
    row = int(loc[1:])
    return (column, row)
	
def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location
    
    Parameters:
        x (int): position x of coordinates
        y (int): position y of coordinates
    Returns:
        str: string of coordinates x,y in plain configuration
    '''
    column = chr(x + ord('a') - 1)
    row = str(y)
    return str(column + row)

Board = tuple[int, list['Piece']]

class Piece:
    pos_x : int	
    pos_y : int
    side : bool #True for White and False for Black
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values'''
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side_
    
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this piece can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule1] and [Rule3] of specification

        Parameters:
            pos_X (int): position x of coordinates
            pos_Y (int): position y of coordinates
            B (Board): board configuration
        Returns:
            bool: True if piece can reach coordinates x,y or False if not  
        '''
        # to be implemented in subclass
        pass

    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if piece can move to coordinates pos_X, pos_Y on board B according to all chess rules

        Parameters:
            pos_X (int): position x of coordinates
            pos_Y (int): position y of coordinates
            B (Board): board configuration
        Returns:
            bool: True if piece can move to coordinates x,y or False if not   
        '''
        B2 = copy.deepcopy(B)
        for item in B2[1]:
            if item.pos_x == self.pos_x and item.pos_y == self.pos_y and item.side == self.side:
                piece = item
                break
        if piece.can_reach(pos_X, pos_Y, B2):
            if is_piece_at(pos_X, pos_Y, B2):
                target = piece_at(pos_X, pos_Y, B2)
                if target.side != piece.side:
                    B2 = piece.move_to(pos_X, pos_Y, B2)
                    if is_check(self.side, B2):
                        return False
                    else:
                        return True
                else:
                    return False
            else:
                B2 = piece.move_to(pos_X, pos_Y, B2)
                if is_check(self.side, B2):
                    return False
                else:
                    return True
        else:
            return False

    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''returns new board resulting from move of this piece to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules

        Parameters:
            pos_X (int): position x of coordinates
            pos_Y (int): position y of coordinates
            B (Board): board configuration        
        Returns:
            Board: new board resulting from move of the piece to coordinates x,y
        '''
        target = None
        if is_piece_at(pos_X, pos_Y, B):
            target = piece_at(pos_X, pos_Y, B)
        for item in B[1]:
            if item == target:
                B[1].remove(item)
        self.pos_x = pos_X
        self.pos_y = pos_Y
        return B

Board = tuple[int, list[Piece]]

def is_piece_at(pos_X : int, pos_Y : int, B: Board) -> bool:
    '''checks if there is piece at coordinates pos_X, pos_Y of board B
    
    Parameters:
        pos_X (int): position x of coordinates
        pos_Y (int): position y of coordinates
        B (Board): board configuration
    Returns:
        bool: True if piece is present at coordinate x,y or False if not    
    '''
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            return True
    return False     
	
def piece_at(pos_X : int, pos_Y : int, B: Board) -> Piece:
    '''returns the piece at coordinates pos_X, pos_Y of board B 
    assumes some piece at coordinates pos_X, pos_Y of board B is present

    Parameters:
        pos_X (int): position x of coordinates
        pos_Y (int): position y of coordinates
        B (Board): board configuration
    Returns:
        Piece: the piece found at coordinates x,y
    '''
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            return piece

class Bishop(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)
	
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this bishop can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule1] and [Rule3] of specification

        Parameters:
            pos_X (int): position x of coordinates
            pos_Y (int): position y of coordinates
            B (Board): board configuration
        Returns:
            bool: True if can reach coordinates x,y or False if not
        '''
        size = B[0]
        reachable_ords = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for direction in directions:
            dx, dy = direction
            x, y = self.pos_x + dx, self.pos_y + dy
            while 1 <= x <= size and 1 <= y <= size:
                if is_piece_at(x, y, B):
                    piece = piece_at(x, y, B)
                    if piece.side == self.side:
                        break
                    else:
                        reachable_ords.append((x, y))
                        break
                else:
                    reachable_ords.append((x, y))
                x += dx
                y += dy
        return (pos_X, pos_Y) in reachable_ords

class King(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)

    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule2] and [Rule3] of specification
        
        Parameters:
            pos_X (int): position x of coordinates
            pos_Y (int): position y of coordinates
            B (Board): board configuration
        Returns:
            bool: True if can reach coordinates x,y or False if not
        '''
        size = B[0]
        reachable_ords = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for direction in directions:
            dx, dy = direction
            x, y = self.pos_x + dx, self.pos_y + dy
            if 1 <= x <= size and 1 <= y <= size:
                if not is_piece_at(x, y, B) or piece_at(x, y, B).side != self.side:
                    reachable_ords.append((x, y))
        return (pos_X, pos_Y) in reachable_ords

def is_check(side: bool, B: Board) -> bool:
    '''checks if configuration of B is check for side

    Parameters:
        side (bool): True if white and False if black
        B (Board): a board configuration
    Returns: True if check or False if not
    '''
    for piece in B[1]:
        if isinstance(piece, King) and piece.side == side:
            king = piece
            break
    for piece in B[1]:
        if piece.side != side and piece.can_reach(king.pos_x, king.pos_y, B):
                return True
    return False        

def is_checkmate(side: bool, B: Board) -> bool:
    '''checks if configuration of B is checkmate for side

    Parameters:
        side (bool): True if white and False if black
        B (Board): a board configuration
    Returns:
        bool: True if checkmate or False if not
    '''
    if is_check(side, B):
        for piece in B[1]:
            if piece.side == side:
                for x in range(1, B[0] + 1):
                    for y in range(1, B[0] + 1):
                        if piece.can_move_to(x, y, B):
                            B2 = copy.deepcopy(B)
                            for item in B2[1]:
                                if item.pos_x == piece.pos_x and item.pos_y == piece.pos_y and item.side == piece.side:
                                    piece2 = item
                                    break
                            B2 = piece2.move_to(x, y, B2)
                            if not is_check(piece2.side, B2):
                                return False
        return True
    else:
        return False

def is_stalemate(side: bool, B: Board) -> bool:
    '''checks if configuration of B is stalemate for side

    Parameters:
        side (bool): True if white and False if black
        B (Board): a board configuration
    Returns:
        bool: True if stalemate or False if not
    '''
    if not is_check(side, B):
        for piece in B[1]:
            if piece.side == side:
                for x in range(1, B[0] + 1):
                    for y in range(1, B[0] + 1):
                        if piece.can_move_to(x, y, B):
                            return False
        return True
    else:
        return False

piece_map = {'K': King,
            'B': Bishop
            }

def read_pieces(pieces: list[str], side: bool) -> list[Piece]:
    '''reads individual pieces in plain configuration
    converts coordinates into numerical form and letter into piece class object

    Parameters:
        pieces (list[str]): list of string locations of pieces
        side (bool): True if white and False if black
    Returns:
        list[Piece]: list of piece objects
    '''
    objs = []
    for piece in pieces:
        piece_class = piece_map[piece[0]]
        coordinates = location2index(piece[1:])
        obj = piece_class(coordinates[0], coordinates[1], side)
        #print(f"{obj.pos_x, obj.pos_y, obj.side, obj}")
        objs.append(obj)
    return objs

def read_board(filename: str) -> tuple[int, list[Piece]]:
    '''reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)

    Parameters:
        filename (str): filename to open in currnet directory
    Returns:
        tuple[int, list[Piece]]: returns a tuple with size of board and a list of pieces, to be used as a Board
    '''
    try:
        with open(filename, 'r') as file:
            size = int(file.readline().strip())
            if size < 1 or size > 26:
                raise IOError # invalid file is size outside specification
            w_objs = read_pieces(file.readline().strip().split(', '), True)
            b_objs = read_pieces(file.readline().strip().split(', '), False)
            w_king = sum(isinstance(piece, King) and piece.side for piece in w_objs)
            b_king = sum(isinstance(piece, King) and not piece.side for piece in b_objs)
            if any(line.strip() for line in file):
                raise IOError # invalid file if unexpected text is found
            if w_king != 1 or b_king != 1:
                raise IOError # invalid file if side does not have 1 king
            objs = []
            objs.extend(w_objs + b_objs)
            positions = set((piece.pos_x, piece.pos_y) for piece in objs)
            if len(positions) != len(objs):
                raise IOError # invalid file if different pieces in same location
            for piece in objs:
                if piece.pos_x < 1 or piece.pos_x > size or piece.pos_y < 1 or piece.pos_y > size:
                    raise IOError # invalid file if piece outside board configuration
        return (size, objs)
    except IOError as error:
        print('This is not a valid file.')

def save_board(filename: str, B: Board) -> None:
    '''saves board configuration into file in current directory in plain format
    
    Parameters:
        filename (str): a filename to save the file as
        B (Board): board configuration to save
    Returns:
        None
    '''
    size = str(B[0])
    w_pieces = [
        key + index2location(piece.pos_x, piece.pos_y)
        for key, value in piece_map.items()
        for piece in B[1]
        if isinstance(piece, value) and piece.side
    ]
    b_pieces = [
        key + index2location(piece.pos_x, piece.pos_y)
        for key, value in piece_map.items()
        for piece in B[1]
        if isinstance(piece, value) and not piece.side
    ]
    with open(filename, 'w') as file:
        file.write(size + '\n')
        file.write(', '.join(w_pieces) + '\n')
        file.write(', '.join(b_pieces) + '\n')   

def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules 
    assumes there is at least one black piece that can move somewhere

    Parameters:
        B (Board): board configuration
    Returns:
        tuple[Piece, int, int]: a Black piece with a move to coordinates x and y
    '''
    for piece in B[1]:
        if piece.side == False:
            for wpiece in B[1]:
                if wpiece.side == True:
                    if piece.can_move_to(wpiece.pos_x, wpiece.pos_y, B):
                        return (piece, wpiece.pos_x, wpiece.pos_y)
    for piece in B[1]:
        if piece.side == False:
            for pos_X in range(1, B[0] + 1):
                for pos_Y in range(1, B[0] + 1):
                    if piece.can_move_to(pos_X, pos_Y, B):
                        B2 = copy.deepcopy(B)
                        for item in B2[1]:
                            if item.pos_x == piece.pos_x and item.pos_y == piece.pos_y and item.side == piece.side:
                                piece2 = item
                                break
                        B2 = piece2.move_to(pos_X, pos_Y, B2)
                        if is_checkmate(True, B2) or is_check(True, B2):
                            return (piece, pos_X, pos_Y)
    for piece in B[1]:        
        if piece.side == False:
            pos_X = random.randint(1, B[0])
            pos_Y = random.randint(1, B[0])
            max_attempts = B[0] * B[0]
            attempts = 0
            while not piece.can_move_to(pos_X, pos_Y, B) and attempts < max_attempts:
                pos_X = random.randint(1, B[0])
                pos_Y = random.randint(1, B[0])
                attempts += 1
            if piece.can_move_to(pos_X, pos_Y, B):
                return (piece, pos_X, pos_Y)

unicode_map = {
                (True, King): '♔',
                (True, Bishop): '♗',
                (False, King): '♚',
                (False, Bishop): '♝',
                0: ' '
                }

def conf2unicode(B: Board) -> str: 
    '''converts board cofiguration B to unicode format string (see section Unicode board configurations)
    
    Parameters:
        B (Board): board configuration
    Returns:
        str: a string of the board configuration in unicode format
    '''
    size = B[0]
    matrix = [[0] * size for _ in range(size)]
    for piece in B[1]:
        matrix[size - piece.pos_y][piece.pos_x - 1] = piece
    unicode_matrix = []
    for row in matrix:
        unicode_row = []
        for square in row:
            if square == 0:
                unicode_row.append(unicode_map[square])
            else:
                unicode_row.append(unicode_map[(square.side, square.__class__)])
        unicode_matrix.append(unicode_row)   
    unicode_string = '\n'.join([' '.join(row) for row in unicode_matrix])
    return unicode_string

def run_play(B: Board) -> None:
    '''Function to run the play between white and black pieces based on counter
    stops play if checkmate or stalemate
    
    Parameters:
        B (Board): Initial board configuration
    Returns:
        None
    '''
    cont_play = True
    counter = 2
    print('The initial configuration is:')
    while cont_play:
        print(conf2unicode(B))
        if is_checkmate(False, B):
            print('Game over. White wins.')
            cont_play = False
        elif is_checkmate(True, B):
            print('Game over. Black wins.')
            cont_play = False
        elif is_stalemate(False, B) and counter % 2 != 0:
            print('Game over. Stalemate.') # stalemate for black
            cont_play = False
        elif is_stalemate(True, B) and counter % 2 == 0:
            print('Game over. Stalemate.') #stalemate for white
            cont_play = False
        else:
            if counter % 2 == 0: # white plays
                try:
                    move = input('Next move of White: ')
                    if move != 'QUIT':
                        start = location2index(move[0:2])
                        end = location2index(move[2:4])
                        piece = piece_at(start[0], start[1], B)
                        if piece.can_move_to(end[0], end[1], B):
                            piece.move_to(end[0], end[1], B)
                            print('The configuration after White\'s move is:')
                        else:
                            print('This is not a valid move.')
                            counter -= 1
                    else: # quit program
                        filename = input('File name to store the configuration: ')
                        save_board(filename, B)
                        print('The game configuration saved')
                        cont_play = False
                except:
                    print('This is not a valid move.')
                    counter -= 1 # reduce counter if invalid move to request new move
            else: # black plays
                move = find_black_move(B)
                piece = move[0]
                move_from = index2location(piece.pos_x, piece.pos_y)
                move_to = index2location(move[1], move[2])
                print(f'Next move of Black is {move_from + move_to}.')
                piece.move_to(move[1], move[2], B)
                print('The configuration after Black\'s move is:')
            counter += 1

def main() -> None:
    '''main function to execute application
    
    Stops game if user inputs 'QUIT'
    Reads input text file and executes run_play with Board B
    '''
    stop_game = False
    while stop_game == False:
        filename = input("File name for initial configuration: ")
        if filename == 'QUIT':
            break
        elif os.path.isfile(filename):
            try:
                B = read_board(filename)
                run_play(B)
                stop_game = True
            except:
                stop_game = False
        else:
            print('This is not a valid file')
            stop_game = False

if __name__ == '__main__': #keep this in
   main()
