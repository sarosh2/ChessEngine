import chess.pgn

pgn = open("tactics.pgn", 'r')
data_count = 0

for i in range(191240):
    game = chess.pgn.read_game(pgn)
    board = game.board()
    moves = list(game.mainline_moves())
    if len(moves) > 0:
        board.push(moves[0])
        dataset_X = open("chessDataset.txt", "a")
        dataset_Y = open("chessDatasetLabels.txt", "a")
        dataset_X.write(board.fen() + '\n')
        dataset_Y.write(str(board.turn * 1) + '\n')
        dataset_X.close()
        dataset_Y.close()
        data_count += 1
        print(data_count)

pgn.close()