import chess
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

def convert_to_data(board):
    data = np.zeros((8, 8, 12))
    map = board.piece_map()
    for square in map:
        data[square // 8][square % 8][piece_to_data_values[str(map[square])]] = 1
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

def model(input_shape):
   
    X_input = K.layers.Input(input_shape, dtype = 'float32')

    # CONV -> BN -> RELU Block applied to X
    X = K.layers.Conv2D(400, (4, 4))(X_input)
    X = K.layers.BatchNormalization(axis = 3)(X)
    X = K.layers.Activation('relu')(X)

    X = K.layers.Conv2D(300, (4, 4))(X)
    X = K.layers.BatchNormalization(axis = 3)(X)
    X = K.layers.Activation('relu')(X)

    X = K.layers.Conv2D(200, (2, 2))(X)
    X = K.layers.BatchNormalization(axis = 3)(X)
    X = K.layers.Activation('relu')(X)


    # FLATTEN X (means convert it to a vector) + FULLYCONNECTED
    X = K.layers.Flatten()(X)
    X = K.layers.Dense(70, activation='sigmoid')(X)
    X = K.layers.Dropout(0.2)(X)
    X = K.layers.Dense(1, activation='sigmoid')(X)

    model = K.models.Model(inputs = X_input, outputs = X)

    return model


NN = model((8, 8, 12))
NN.compile(optimizer = 'adamax', loss = 'mean_squared_error', metrics = ['accuracy'])

for epoch in range(100):
    for i in range(10):
        X_train = create_data(data, i * 20000, (i + 1) * 20000)
        Y_train = create_labels(labels, i * 20000, (i + 1) * 20000)
        NN.fit(X_train, Y_train, 20000, epochs = 1)
        print((epoch * 10 + i))

X_test = create_data(data, 200000, 210000)
Y_test = create_labels(labels, 200000, 210000)
NN.evaluate(X_test, Y_test)


NN.save("ChessAiConv")