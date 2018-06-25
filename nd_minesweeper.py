import os
import re
import argparse

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
                print_game_over(board, counts)
                input('You lose! Press ENTER to play again. ')
                break
            elif np.sum(known == -1) == mines:
                print_game_over(board, counts)
                input('You win! Press ENTER to play again. ')
                break
        except Exception:
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Plays minesweeper on arbitray n-dimensional grids")
    parser.add_argument('-d', '--dims', nargs='+', help='List of dimensions')
    parser.add_argument('-m', '--mines', help='Number of mines')

    args = parser.parse_args()
    dims = tuple(map(int, args.dims)) if args.dims is not None else [16, 30]
    mines = int(args.mines) if args.mines is not None else 99

    while True:
        play_game(dims, mines)
