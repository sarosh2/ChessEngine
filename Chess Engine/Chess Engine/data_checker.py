import chess
import pygame

data_file = open("chessDataset.txt", "r")
data = data_file.readlines()
data_file.close()

board = chess.Board(data[0])
print(board.turn)

# making the opening window
window = pygame.display.set_mode((1000,720)) # lol 69
pygame.display.set_caption("Chess")

# defining colors
block = [(69, 69, 69), (255, 255, 255)] # lol
border = (169, 169, 169)

# defining sttributes of the board
dimension = 80 # height and width of a block (also, lol 69)
starting = (250, 50) # starting coordinate for drawing board
border_thickness = 5 # thickness of the border
background_dimension = (8 * dimension) + (2 * border_thickness) # size of the background layer behind the board

# loading images
piece_images = {
"p" : pygame.image.load('black pawn.png'),
"P" : pygame.image.load('white pawn.png'),
"r" : pygame.image.load('black rook.png'),
"R" : pygame.image.load('white rook.png'),
"n" : pygame.image.load('black knight.png'),
"N" : pygame.image.load('white knight.png'),
"b" : pygame.image.load('black bishop.png'),
"B" : pygame.image.load('white bishop.png'),
"q" : pygame.image.load('black queen.png'),
"Q" : pygame.image.load('white queen.png'),
"k" : pygame.image.load('black king.png'), 
"K" : pygame.image.load('white king.png')}

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((0,0,0))

# drawing the board
    pygame.draw.rect(window, border, (starting[0] - border_thickness, starting[1] - border_thickness, background_dimension, background_dimension))
    for row in range(8):
       for column in range (8):
            color = (row + column + 1) % 2
            pygame.draw.rect(window, block[color], (starting[0] + column * dimension, starting[1] + row * dimension, dimension, dimension))
            piece = board.piece_at(((7 - row) * 8) + column)
            if piece != None:
                window.blit(piece_images[str(piece)], ((dimension * column) + starting[0], (dimension * row) + starting[1]))
    pygame.display.update()
