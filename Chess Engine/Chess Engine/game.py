import pygame

def evaluate_position_advanced(board):
    value = 0
    color = board.turn
    no_of_moves_value = len(list(board.legal_moves)) / 5
    for square in board.piece_map():
        piece = board.piece_at(square)
        if piece != None:
            piece_char = piece.symbol()
            if piece_char != "k" and piece_char != "K" and piece_char != "q" and piece_char != "Q":
                value += piece_values[piece_char] * 2 / (abs(4 - (square / 8)) + abs(4 - (square % 8)))
            elif board.has_castling_rights(color):
                value += piece_values[piece_char] / 1.1
            else:
                value += piece_values[piece_char]

    if color:
        value += no_of_moves_value
    else:
        value -= no_of_moves_value
    return value

def sign(object):
    if object > 0:
        return 1
    elif object < 0:
        return -1
    else:
        return 0

def multiply_by_i(complex):
    temp = -complex[1]
    complex[1] = complex[0]
    complex[0] = temp

# making the opening window
window = pygame.display.set_mode((1000,690)) # lol 69
pygame.display.set_caption("Chess")

# making the chess board

# defining colors
block = [(69, 69, 69), (255, 255, 255)] # lol
border = (169, 169, 169)
promotion_block = (0,200,120)
possible_move = [(35,35,35),(127,127,127)]

# defining sttributes of the board
number = 8 # number of blocks per row or column
dimension = 69 # height and width of a block (also, lol 69)
starting = (250, 50) # starting coordinate for drawing board
ending = (starting[0] + 8 * dimension, starting[1] + 8 * dimension)
border_thickness = 5 # thickness of the border
background_dimension = (number * dimension) + (2 * border_thickness) # size of the background layer behind the board

selected_piece = 0
turn = 1
death = [[8,0],[-1,0]]

#defining pieces as a class
class piece:
    def __init__(self, type, color, column, row, moved):
        type[color] = pygame.transform.scale(type[color], (dimension, dimension))
        self.type = type
        self.color = color
        self.column = column
        self.row = row
        self.moved = moved
        self.xcor = (dimension * column) + starting[0]
        self.ycor = (dimension * row) + starting[1]

    def change_coordinates(self, column, row):
        self.column = column
        self.row = row
        self.xcor = (dimension * column) + starting[0]
        self.ycor = (dimension * row) + starting[1]

    def collision(self, column, row):
        change = 0
        sign_row = sign(row - self.row)
        sign_column = sign(column - self.column)
        if self.column == column:
            change = abs(row - self.row)
        else:
            change = abs(column - self.column)
        if self.column == column or self.row == row or abs(self.column - column) == abs(self.row - row):
            for position in range(1, change):
                check_row = self.row + (position * sign_row)
                check_column = self.column + (position * sign_column)
                if check_row >= 0 and check_row <= 7 and check_column >=0 and check_column <=7: 
                    if positions[check_row][check_column]:
                        return positions[self.row + (position * sign_row)][self.column + (position * sign_column)]
        return 0

    def under_threat(self):
        
        complex_straight = [ 1, 0 ];
        complex_diagonal = [ 1, 1 ];
        
        for turns in range(4): # check for rook and queen
            threatening_piece = self.collision(self.column + 8 * complex_straight[0], self.row + 8 * complex_straight[1])
            if threatening_piece and self.color != pieces[threatening_piece - 1].color:
                if pieces[threatening_piece - 1].type == queen or pieces[threatening_piece - 1].type == rook:
                    return threatening_piece
            multiply_by_i(complex_straight)

        for turns in range(4): # check for bishop and queen
            threatening_piece = self.collision(self.column + 8 * complex_diagonal[0], self.row + 8 * complex_diagonal[1])
            if threatening_piece and self.color != pieces[threatening_piece - 1].color:
                if pieces[threatening_piece - 1].type == queen or pieces[threatening_piece - 1].type == bishop:
                    return threatening_piece
            multiply_by_i(complex_diagonal)

        for turns in range(8): #check for knight
            threatening_piece = 0
            check_row = self.row + complex_diagonal[1] * ((turns % 2) + 1)
            check_column = self.column + complex_diagonal[0] * (((turns + 1) % 2) + 1)
            if check_row >= 0 and check_row <= 7 and check_column >= 0 and check_column <= 7:
                threatening_piece = positions[check_row][check_column]
            if threatening_piece and self.color != pieces[threatening_piece - 1].color:
                if pieces[threatening_piece - 1].type == knight:
                    return threatening_piece
            if turns % 2:
                multiply_by_i(complex_diagonal)

        for turns in range(8): #check for king
            threatening_piece = 0
            if turns % 2:
                check_row = self.row + complex_diagonal[1]
                check_column = self.column + complex_diagonal[0]
                if check_row >= 0 and check_row <= 7 and check_column >= 0 and check_column <= 7:
                    threatening_piece = positions[check_row][check_column]
                multiply_by_i(complex_diagonal)
            else:
                check_row = self.row + complex_straight[1]
                check_column = self.column + complex_straight[0]
                if check_row >= 0 and check_row <= 7 and check_column >= 0 and check_column <= 7:
                    threatening_piece = positions[check_row][check_column]
                multiply_by_i(complex_straight)

            if threatening_piece and self.color != pieces[threatening_piece - 1].color:
                if pieces[threatening_piece - 1].type == king:
                    return threatening_piece

        for turns in range(2): # check for pawns
            threatening_piece = 0
            check_row = self.row - complex_diagonal[1] * (2 * self.color - 1)
            check_column = self.column - complex_diagonal[0] * (2 * self.color - 1)
            if check_row >= 0 and check_row <= 7 and check_column >= 0 and check_column <= 7:
                threatening_piece = positions[check_row][check_column]
            if threatening_piece and self.color != pieces[threatening_piece - 1].color:
                if pieces[threatening_piece - 1].type == pawn:
                    return threatening_piece
            multiply_by_i(complex_diagonal)
        return 0;

    def is_legal(self, column, row):
        
        if turn != self.color or self.collision(column, row):
            return 0
        elif positions[row][column] and self.color == pieces[positions[row][column] - 1].color:
            return 0;

        temp = positions[row][column]
        positions[row][column] = positions[self.row][self.column]
        positions[self.row][self.column] = 0
        if pieces[30 + turn].under_threat():
            positions[self.row][self.column] = positions[row][column]
            positions[row][column] = temp
            return 0
        else:
            positions[self.row][self.column] = positions[row][column]
            positions[row][column] = temp

        if self.type == pawn:
            if self.column == column:
                if positions[row][column]:
                    return 0
                elif (2 * (self.color) - 1) * (self.row - row) == 1:
                    return 1
                elif self.row == 1 + 5 * self.color and (2 * (self.color) - 1) * (self.row - row) == 2:
                    return 1
            elif (2 * (self.color) - 1) * (self.row - row) == 1 and abs(self.column - column) == 1:
                if positions[row][column]:
                    return 1

        elif self.type == rook:
            if self.row == row or self.column == column:
                return 1
        
        elif self.type == knight:
            if (abs(row - self.row) == 2 and abs(column - self.column) == 1) or (abs(row - self.row) == 1 and abs(column - self.column) == 2):
                return 1

        elif self.type == bishop:
            if abs(row - self.row) == abs(column - self.column):
                return 1

        elif self.type == queen:
            if self.row == row or self.column == column or abs(row - self.row) == abs(column - self.column):
                return 1

        elif self.type == king:
            if abs(row - self.row) <= 1 and abs(column - self.column) <= 1:
                return 1
            elif self.row == row and abs(column - self.column) == 2 and self.moved == 0:
                return 1
        return 0
    
    def promote(self):
    
        # draw the selection square
        location = (starting[0] + 3 * dimension, starting[1] + 3 * dimension)
        block_color = (250,250, 200)
        run = 1
        pygame.draw.rect(window, promotion_block, (location[0] - border_thickness , location[1] - border_thickness, 2 * (dimension + border_thickness), 2 * (dimension + border_thickness)))
        pygame.draw.rect(window, block_color, (location[0] , location[1], 2 * dimension, 2 * dimension))
        window.blit(queen[self.color], (location[0], location[1]))
        window.blit(rook[self.color], (location[0] + dimension, location[1]))
        window.blit(bishop[self.color], (location[0], location[1] + dimension))
        window.blit(knight[self.color], (location[0] + dimension, location[1] + dimension))
        pygame.display.update()

        while run:
            event = pygame.event.poll()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = int((pos[0] - starting[0]) / dimension)
                row = int((pos[1] - starting[1]) / dimension)
                if row == 3:
                    if column == 3:
                        self.type = queen
                        run = 0
                    elif column == 4:
                        self.type = rook
                        run = 0
                elif row == 4:
                    if column == 3:
                        self.type = bishop
                        run = 0
                    elif column == 4:
                        self.type = knight
                        run = 0

# loading images
pawn = [pygame.image.load('black pawn.png'), pygame.image.load('white pawn.png')]
rook = [pygame.image.load('black rook.png'), pygame.image.load('white rook.png')]
knight = [pygame.image.load('black knight.png'), pygame.image.load('white knight.png')]
bishop = [pygame.image.load('black bishop.png'), pygame.image.load('white bishop.png')]
queen = [pygame.image.load('black queen.png'), pygame.image.load('white queen.png')]
king = [pygame.image.load('black king.png'), pygame.image.load('white king.png')]

# intitializing all the pieces
pieces = [piece(pawn, 0, 0, 1, 0),
          piece(pawn, 0, 1, 1, 0),
          piece(pawn, 0, 2, 1, 0),
          piece(pawn, 0, 3, 1, 0),
          piece(pawn, 0, 4, 1, 0),
          piece(pawn, 0, 5, 1, 0),
          piece(pawn, 0, 6, 1, 0),
          piece(pawn, 0, 7, 1, 0),
          piece(pawn, 1, 0, 6, 0),
          piece(pawn, 1, 1, 6, 0),
          piece(pawn, 1, 2, 6, 0),
          piece(pawn, 1, 3, 6, 0),
          piece(pawn, 1, 4, 6, 0),
          piece(pawn, 1, 5, 6, 0),
          piece(pawn, 1, 6, 6, 0),
          piece(pawn, 1, 7, 6, 0),
          piece(rook, 0, 0, 0, 0),
          piece(rook, 0, 7, 0, 0),
          piece(rook, 1, 0, 7, 0),
          piece(rook, 1, 7, 7, 0),
          piece(knight, 0, 1, 0, 0),
          piece(knight, 0, 6, 0, 0),
          piece(knight, 1, 1, 7, 0),
          piece(knight, 1, 6, 7, 0),
          piece(bishop, 0, 2, 0, 0),
          piece(bishop, 0, 5, 0, 0),
          piece(bishop, 1, 2, 7, 0),
          piece(bishop, 1, 5, 7, 0),
          piece(queen, 0, 3, 0, 0),
          piece(queen, 1, 3, 7, 0),
          piece(king, 0, 4, 0, 0),
          piece(king, 1, 4, 7, 0),]

# initializing the positions array
positions = [[17, 21, 25, 29, 31, 26, 22, 18],
             [1, 2, 3, 4, 5, 6, 7, 8],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [9, 10, 11, 12, 13, 14, 15, 16],
             [19, 23, 27, 30, 32, 28, 24, 20]]

def change_death(color):
    if death[color][1] == 7:
        death[color][0] -= 2 * color - 1
        death[color][1] = 0
    else:
        death[color][1] += 1

while True:

    window.fill((0,0,0))

# drawing the board
    pygame.draw.rect(window, border, (starting[0] - border_thickness, starting[1] - border_thickness, background_dimension, background_dimension))
    for row in range(number):
        for column in range (number):
            color = (row + column + 1) % 2
            pygame.draw.rect(window, block[color], (starting[0] + column * dimension, starting[1] + row * dimension, dimension, dimension))
            if selected_piece and pieces[selected_piece - 1].is_legal(column, row):
                pygame.draw.circle(window, possible_move[color], (starting[0] + column * dimension + (dimension + 1) // 2, starting[1] + row * dimension + (dimension + 1) // 2), dimension // 5)

# drawing pieces
    for item in pieces:
        window.blit(item.type[item.color], (item.xcor, item.ycor))
    pygame.display.update()
       
# pick and drop of pieces
    event = pygame.event.poll()
    if selected_piece:

        if event.type == pygame.MOUSEBUTTONDOWN: # leaving the piece
            
            position = pygame.mouse.get_pos() # getting the current location of the mouse
            column = int((position[0] - starting[0]) / dimension)
            row = int((position[1] - starting[1]) / dimension)
            
            if pieces[selected_piece - 1].is_legal(column, row): # if it is legal to move the selected piece to where the mouse is pointing

                turn += 1
                turn = turn % 2
                if positions[row][column] and positions[row][column] != selected_piece: # capture if necessary
                    pieces[positions[row][column] - 1].change_coordinates(death[pieces[positions[row][column] - 1].color][0], death[pieces[positions[row][column] - 1].color][1])
                    change_death(pieces[positions[row][column] - 1].color)

                positions[pieces[selected_piece - 1].row][pieces[selected_piece - 1].column] = 0 # update positions
                positions[row][column] = selected_piece
                pieces[selected_piece - 1].change_coordinates(column, row)
                pieces[selected_piece - 1].moved = 1
            
                if selected_piece >= 1 and selected_piece <= 16: # if selected piece is a pawn
                    if pieces[selected_piece - 1].row == 7 * ((pieces[selected_piece - 1].color + 1) % 2): # if at the edge of the board
                        pieces[selected_piece - 1].promote()
            
            else:
                pieces[selected_piece - 1].change_coordinates(pieces[selected_piece - 1].column, pieces[selected_piece - 1].row)

            selected_piece = 0

        elif event.type == pygame.MOUSEMOTION: # moving the piece
            pieces[selected_piece - 1].xcor, pieces[selected_piece - 1].ycor = pygame.mouse.get_pos()
            pieces[selected_piece - 1].xcor -= dimension / 2
            pieces[selected_piece - 1].ycor -= dimension / 2

    elif event.type == pygame.MOUSEBUTTONDOWN: # selecting the piece
        position = pygame.mouse.get_pos()
        column = int((position[0] - starting[0]) / dimension)
        row = int((position[1] - starting[1]) / dimension)
        if positions[row][column]:
            selected_piece = positions[row][column]
