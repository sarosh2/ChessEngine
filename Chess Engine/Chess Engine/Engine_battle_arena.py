import chess
import numpy as np
import pygame
import time
import math
import random
import keras as K

# making the opening window
window = pygame.display.set_mode((1000,720)) # lol 69
pygame.display.set_caption("Chess")

# making the chess board
board = chess.Board()

# defining colors
block = [(69, 69, 69), (255, 255, 255)] # lol
border = (169, 169, 169)

# defining sttributes of the board
dimension = 80 # height and width of a block (also, lol 69)
starting = (250, 50) # starting coordinate for drawing board
border_thickness = 5 # thickness of the border
background_dimension = (8 * dimension) + (2 * border_thickness) # size of the background layer behind the board

#loading the Ai
NN_white = K.models.load_model("ChessAiConv")
NN_black = K.models.load_model("ChessAiReg")

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

#assigning values to each individual piece
piece_to_data_values_white = {
    "p" : 0,
    "P" : 1,
    "n" : 2,
    "N" : 3,
    "b" : 4,
    "B" : 5,
    "r" : 6,
    "R" : 7,
    "q" : 8,
    "Q" : 9,
    "k" : 10,
    "K" : 11}

piece_to_data_values_black = {
    "p" : -1,
    "P" : 1,
    "n" : -2,
    "N" : 2,
    "b" : -3,
    "B" : 3,
    "r" : -4,
    "R" : 4,
    "q" : -5,
    "Q" : 5,
    "k" : -6,
    "K" : 6}

def convert_to_data_white(board):
    data = np.zeros((8, 8, 12))
    map = board.piece_map()
    for square in map:
        data[square // 8][square % 8][piece_to_data_values_white[str(map[square])]] = 1
    return data

def convert_to_data_black(board):
    data = np.zeros((67, 1))
    map = board.piece_map()
    for square in map:
        data[square] = piece_to_data_values_black[str(map[square])]
    data = np.divide(data, 6)
    data[64] = board.has_castling_rights(True) * 1
    data[65] = board.has_castling_rights(False) * 1
    data[66] = board.has_legal_en_passant() * 1
    return data

def evaluate_position_white(board):
    evaluation = NN_white.predict(np.reshape(convert_to_data_white(board), (1, 8, 8, 12)))
    if board.can_claim_draw():
        evaluation /= 1.3
    return evaluation

def evaluate_position_black(board):
    evaluation = NN_black.predict(np.reshape(convert_to_data_black(board), (1, 67, 1)))
    if board.can_claim_draw():
        evaluation /= 1.3
    return evaluation

def minimax_ab_pruning_white(board, depth, alpha, beta):

    color = board.turn
    moves = list(board.legal_moves)
    best_move = (None, 1000 * int(math.pow(-1, color)))

    if len(moves) == 0:
        if board.is_checkmate():
            return (None, 100 * int(math.pow(-1, color)))
        else:
            return (None, 0)
    elif depth == 0:
        return (None, evaluate_position_white(board))
    elif color:
        for move in moves:
            board.push(move)
            evaluation = minimax_ab_pruning_white(board, depth - 1, alpha, beta)[1]
            if evaluation > best_move[1]:
                best_move = (move, evaluation)
                if evaluation > alpha:
                    alpha = evaluation
                if evaluation > beta:
                    board.pop()
                    break
            board.pop()

    else:
        for move in moves:
            board.push(move)
            evaluation = minimax_ab_pruning_white(board, depth - 1, alpha, beta)[1]
            if evaluation < best_move[1]:
                best_move = (move, evaluation)
                if evaluation < beta:
                    beta = evaluation
                if evaluation < alpha:
                    board.pop()
                    break
            board.pop()

    return best_move

def minimax_ab_pruning_black(board, depth, alpha, beta):

    color = board.turn
    moves = list(board.legal_moves)
    best_move = (None, 1000 * int(math.pow(-1, color)))

    if len(moves) == 0:
        if board.is_checkmate():
            return (None, 100 * int(math.pow(-1, color)))
        else:
            return (None, 0)
    elif depth == 0:
        return (None, evaluate_position_black(board))
    elif color:
        for move in moves:
            board.push(move)
            evaluation = minimax_ab_pruning_black(board, depth - 1, alpha, beta)[1]
            if evaluation > best_move[1]:
                best_move = (move, evaluation)
                if evaluation > alpha:
                    alpha = evaluation
                if evaluation > beta:
                    board.pop()
                    break
            board.pop()

    else:
        for move in moves:
            board.push(move)
            evaluation = minimax_ab_pruning_black(board, depth - 1, alpha, beta)[1]
            if evaluation < best_move[1]:
                best_move = (move, evaluation)
                if evaluation < beta:
                    beta = evaluation
                if evaluation < alpha:
                    board.pop()
                    break
            board.pop()

    return best_move


while True:

    window.fill((0,0,0))

#drawing the board
    pygame.draw.rect(window, border, (starting[0] - border_thickness, starting[1] - border_thickness, background_dimension, background_dimension))
    for row in range(8):
       for column in range (8):
            color = (row + column + 1) % 2
            pygame.draw.rect(window, block[color], (starting[0] + column * dimension, starting[1] + row * dimension, dimension, dimension))
            piece = board.piece_at(((7 - row) * 8) + column)
            if piece != None:
                window.blit(piece_images[str(piece)], ((dimension * column) + starting[0], (dimension * row) + starting[1]))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    if len(list(board.legal_moves)) > 0 and not board.can_claim_draw():
        if board.turn:
            board.push(chess.Move.from_uci(input("Move Pls: ")))
        else:
            board.push(minimax_ab_pruning_black(board, 1, -1000, 1000)[0])
