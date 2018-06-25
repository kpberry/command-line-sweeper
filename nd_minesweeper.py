import os
import re

import numpy as np
from minesweeping import get_mine_counts, gen_board, select


def print_known(known):
    unknown_mask = known == -1
    zero_mask = known == 0
    array_string = known.astype('U1')
    array_string[unknown_mask] = '■'
    array_string[zero_mask] = ' '
    array_string = np.array2string(array_string, max_line_width=1000)
    print(re.sub(r'\'| *\[+|\]+', '', array_string))


def print_game_over(board, counts):
    zero_mask = counts == 0
    array_string = counts.astype('U1')
    array_string[zero_mask] = ' '
    array_string[board > 0] = 'X'
    array_string = np.array2string(array_string, max_line_width=1000)
    print(re.sub(r'\'| *\[+|\]+', '', array_string))


def play_game(dims, mines):
    board = gen_board(dims, mines)
    counts = get_mine_counts(board)
    known = np.ones(dims) * -1

    while True:
        os.system('clear')
        print_known(known)
        indices = input(
            'Enter {} indices (space separated): '.format(len(dims)))
        try:
            indices = map(int, indices.split())
            safe = select(indices, board, counts, known)
            if not safe:
                print('You lose!')
                print_game_over(board, counts)
                break
            elif np.sum(known == -1) == mines:
                print('You win!')
                print_game_over(board, counts)
                break
        except:
            pass


if __name__ == '__main__':
    play_game([16, 30, 2], 10)
