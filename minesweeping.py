import numpy as np
from scipy.ndimage.measurements import label
from scipy.signal import convolve

# Check out how many loops this code doesn't have


def gen_board(dims, mines):
    # Randomly places mines on a board by shuffling a list of mines and not
    # mines
    board = np.concatenate([np.zeros(np.prod(dims) - mines), np.ones(mines)])
    np.random.shuffle(board)
    return board.reshape(dims)


def get_mine_counts(board):
    # Gets the count of mines in all cells' neighbors by using an n-dimensional
    # convolution with a unit tensor in the appropriate dimension
    kernel = np.ones([3] * len(board.shape))
    # For trimming the excess 2 rows/columns off the result of the convolution
    dims = list(map(lambda d: slice(1, d + 1), board.shape))
    counts = convolve(kernel, board, mode='full')[dims]
    return np.round(np.abs(counts))


def select(index, board, counts, known):
    index = tuple(index)
    if board[index] > 0:
        return False  # game over
    elif counts[index] > 0:
        known[index] = counts[index]
        return True
    else:
        # Flood fill algorithm; detect connected components in n-dimensions and
        # expose any cells neighboring the connected component of the selected
        # index
        kernel = np.ones([3] * len(board.shape))
        connected_components = label(1 - (counts > 0), structure=kernel)[0]
        empty_mask = connected_components == connected_components[index]
        dims = list(map(lambda d: slice(1, d + 1), board.shape))
        full_mask = convolve(kernel, 1 * empty_mask)[dims] > 0
        known[full_mask] = counts[full_mask]
        return True
