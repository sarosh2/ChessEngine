import random
import chess
import numpy as np
import pygame
import math
import pickle
import time

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

piece_to_data_values = {
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


def convert_to_data(board):
    data = np.zeros((68, 1))
    map = board.piece_map()
    for square in map:
        data[square] = piece_to_data_values[str(map[square])]
    data = np.divide(data, 6)
    data[64] = board.turn * 1
    data[65] = board.has_castling_rights(True) * 1
    data[66] = board.has_castling_rights(False) * 1
    data[67] = board.has_legal_en_passant() * 1
    return data

def activation(Z, function):
    if function == "sigmoid":
        try:
            return 1 / (1 + math.exp(-Z))
        except OverflowError:
            return 0
    elif function == "relu":
        return Z * (Z > 0)
    else:
        return None

class Model:
    def __init__(self, setup):
        self.setup = setup
        self.input_size = setup[0]
        self.weights = []
        self.biases = []
        for layer in range(1, len(setup)):
            self.weights.append(np.random.randn(setup[layer][0], setup[layer - 1][0]))
        for layer in range(1, len(setup)):
            self.biases.append(np.random.randn(setup[layer][0], 1))

    def __init__(self, setup, base_model):
        self.setup = setup
        self.input_size = setup[0]
        self.weights = []
        self.biases = []
        for layer in range(1, len(setup)):
            self.weights.append(base_model.weights[layer - 1] + (np.random.randn(setup[layer][0], setup[layer - 1][0]) / 2))
        for layer in range(1, len(setup)):
            self.biases.append(base_model.biases[layer - 1] + (np.random.randn(setup[layer][0], 1) / 2))

    def forward_prop(self, input):
        for layer in range(len(self.weights)):
            Z = np.dot(self.weights[layer], input) + self.biases[layer]
            input = activation(Z, self.setup[layer + 1][1])
        return input

def evaluate_position(board, model):
    evaluation = model.forward_prop(convert_to_data(board))
    if board.can_claim_draw():
        evaluation /= 1.3
    return evaluation

def minimax_ab_pruning(board, depth, alpha, beta, model):

    color = board.turn
    moves = list(board.legal_moves)
    best_move = (None, 1000 * int(math.pow(-1, color)))

    if len(moves) == 0:
        if board.is_checkmate():
            return (None, 100 * int(math.pow(-1, color)))
        else:
            return (None, 0)
    elif depth == 0:
        return (None, evaluate_position(board, model))
    elif color:
        for move in moves:
            board.push(move)
            evaluation = minimax_ab_pruning(board, depth - 1, alpha, beta, model)[1]
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
            evaluation = minimax_ab_pruning(board, depth - 1, alpha, beta, model)[1]
            if evaluation < best_move[1]:
                best_move = (move, evaluation)
                if evaluation < beta:
                    beta = evaluation
                if evaluation < alpha:
                    board.pop()
                    break
            board.pop()

    return best_move

def max(board, model):
    moves = list(board.legal_moves)
    best_move = (None, -1000)
    for move in moves:
        board.push(move)
        evaluation = None
        if board.is_variant_draw() or board.can_claim_draw():
            evaluation = -100
        else:
            evaluation = model.forward_prop(convert_to_data(board))
        if evaluation > best_move[1]:
            best_move = (move, evaluation)
        board.pop()
    return best_move[0]

def min(board, model):
    moves = list(board.legal_moves)
    best_move = (None, 1000)
    for move in moves:
        board.push(move)
        evaluation = None
        if board.is_variant_draw() or board.can_claim_draw():
            evaluation = 100
        else:
            evaluation = model.forward_prop(convert_to_data(board))
        if evaluation < best_move[1]:
            best_move = (move, evaluation)
        board.pop()
    return best_move[0]

def play_game(model1, model2):

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
        time.sleep(0.5)

        moves = list(board.legal_moves)
        if len(moves) > 0 and not board.can_claim_draw():
            if board.turn:
                board.push(minimax_ab_pruning(board, 2, -1000, 1000, model1)[0])
            else:
                board.push(minimax_ab_pruning(board, 2, -1000, 1000, model2)[0])
        else:
            winner = None
            if board.is_checkmate():
                if board.turn:
                    winner = model2
                    print("Black Won")
                else:
                    winner = model1
                    print("White won")
            board.reset()
            return winner

setup = [(68, None), (32, "relu"), (16, "relu"), (4, "relu"), (1, "sigmoid")]
setup1 = [(68, None), (15, "relu"), (10, "relu"), (5, "relu"), (3, "relu"), (1, "sigmoid")]

generation = 5
match = 1

while True:
    model = None
    with open("evolveAi", "rb") as load_file:
        model = pickle.load(load_file)
        load_file.close()
    test = Model(setup1, model)

    print("Generation: " + str(generation) + " Match: " + str(match))
    winner = None
    if match % 2 == 0:
        winner = play_game(model, test)
    else:
        winner = play_game(test, model)
    match += 1

    if winner == test:
        with open("evolveAi", "wb") as save_file:
            pickle.dump(test, save_file)
            save_file.close()
        with open("history", "a") as history_file:
            history_file.write("Generation " + str(generation) + " took " + str(match - 1) + " matches" + '\n')
            history_file.close()
        generation += 1
        match = 1

"""
while True:
    models = []
    with open("evolveAi", "rb") as load_file:
        models.append(pickle.load(load_file))

    for i in range (255):
        models.append(Model(setup, models[0]))

    for round in range(8):
        no_of_models = len(models)
        winners = []
        for match in range(no_of_models // 2):
            print("Generation: " + str(generation) + " Round: " + str(round + 1) + " Match: " + str(match + 1))
            winners.append(play_game(models[match], models[no_of_models - 1 - match]))
        models = winners

    with open("evolveAi", "wb") as save_file:
        pickle.dump(models[0], save_file)
    generation += 1
"""

"""model = K.models.load_model("ChessAi")

save_model = Model(setup1)

for layer_no in range(len(save_model.weights)):
    save_model.weights[layer_no] = K.backend.get_value(model.weights[layer_no * 2]).transpose()
    save_model.biases[layer_no] = K.backend.get_value(model.weights[(layer_no * 2) + 1]).reshape((model.weights[(layer_no * 2) + 1].shape[0], 1))
    print(save_model.weights[layer_no].shape)
    print(save_model.biases[layer_no].shape)


with open("evolveAi", "wb") as save_file:
    pickle.dump(save_model, save_file)
    save_file.close()"""
