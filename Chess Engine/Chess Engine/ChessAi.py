import chess
import pygame
import numpy as np
import keras as K
import random

data_file = open("chessDataset.txt", "r")
label_file = open("chessDatasetLabels.txt", "r")
data = data_file.readlines()
labels = label_file.readlines()
data_file.close()
label_file.close()

map_index_position = list(zip(data, labels))
random.shuffle(map_index_position)
data, labels = zip(*map_index_position)

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
    data = np.zeros((67, 1))
    map = board.piece_map()
    for square in map:
        data[square] = piece_to_data_values[str(map[square])]
    data = np.divide(data, 6)
    data[64] = board.has_castling_rights(True) * 1
    data[65] = board.has_castling_rights(False) * 1
    data[66] = board.has_legal_en_passant() * 1
    return data

def create_data(complete_list, range_from, range_to):
    data = []
    for i in range(range_from, range_to):
        data.append(convert_to_data(chess.Board(complete_list[i])))
    data = np.asarray(data)
    return data

def create_labels(complete_list, range_from, range_to):
    labels = []
    for i in range(range_from, range_to):
        labels.append(int(complete_list[i]))
    labels = np.asarray(labels)
    return labels

def model(input_shape = (67, 1)):
    
    input = K.layers.Input(input_shape, dtype = 'float32')

    X = K.layers.Flatten()(input)
    X = K.layers.Dense(773, activation = 'relu')(X)
    X = K.layers.Dense(600, activation = 'relu')(X)
    X = K.layers.Dense(400, activation = 'relu')(X)
    X = K.layers.Dense(200, activation = 'relu')(X)
    X = K.layers.Dense(100, activation = 'relu')(X)
    X = K.layers.Dense(1, activation = 'sigmoid')(X)
    
    model = K.models.Model(inputs = input, outputs = X)

    return model

NN = model()
NN.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics = ['accuracy'])

for epoch in range(100):
    for i in range(10):
        X_train = create_data(data, i * 20000, (i + 1) * 20000)
        Y_train = create_labels(labels, i * 20000, (i + 1) * 20000)
        NN.fit(X_train, Y_train, 20000, epochs = 1)
        print((epoch * 10 + i))

X_test = create_data(data, 200000, 210000)
Y_test = create_labels(labels, 200000, 210000)
NN.evaluate(X_test, Y_test)

NN.save("ChessAi")

"""
for epoch in range(10):
    for i in range(40):
        range_from = i * 100
        range_to = (i + 1) * 100"""