from minesweeping import gen_board, get_neighbor_counts, select
from nd_minesweeper import print_known
import numpy as np
from random import choice
import argparse


def get_random_unknown_index(known, marked):
    unknown = (known < 0) & (marked < 1)
    return choice(np.transpose(np.nonzero(unknown)).tolist())


def get_safe_indices(known, marked):
    marked_counts = get_neighbor_counts(marked)
    satisfied = (marked_counts == known) & (known > 0)
    safe_indices = get_neighbor_counts(satisfied) * (known < 0) * (marked < 1)
    return np.transpose(np.nonzero(safe_indices))


def mark_mines(known, marked):
    unknown = get_neighbor_counts(known < 0)
    satisfied = (unknown == known) & (known > 0)
    new_marked = np.round(get_neighbor_counts(satisfied) * (known < 0))
    marked[(marked + new_marked) > 0] = 1


def solve(board, serial=False):
    counts = get_neighbor_counts(board)
    known = np.ones(dims) * -1
    marked = np.zeros(known.shape)

    turns = 0
    while True:
        turns += 1

        indices = get_safe_indices(known, marked)
        if len(indices) > 0:
            if serial:
                safe = select(indices[0], board, counts, known)
                assert safe
            else:
                for index in indices:
                    safe = select(index, board, counts, known)
                    assert safe
        else:
            index = get_random_unknown_index(known, marked)
            safe = select(index, board, counts, known)
            if not safe:
                print('You lose! (random selection)')
                return False

        mark_mines(known, marked)

        print_known(known, marked=marked)
        print(np.sum(marked))
        print('-' * 80)
        assert np.sum((known > 0) * board) == 0

        if np.sum(board) == np.sum(marked):
            assert np.sum(board * marked) == np.sum(board)
            print('Game won in {} turns!'.format(turns))
            return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Plays minesweeper on arbitray n-dimensional grids")
    parser.add_argument('-d', '--dims', nargs='+', help='List of dimensions')
    parser.add_argument('-m', '--mines', help='Number of mines')
    parser.add_argument('-u', '--until_win', help='Play until a win')
    parser.add_argument('-s', '--serial', help='Take one turn at a time')

    args = parser.parse_args()
    dims = tuple(map(int, args.dims)) if args.dims else [16, 30]
    mines = int(args.mines) if args.mines else 99
    until_win = True if args.until_win in ['True', 'true', '1'] else False
    serial = True if args.serial in ['True', 'true', '1'] else False

    if until_win:
        tries = 1
        while not solve(gen_board(dims, mines), serial=serial):
            print('=' * 80)
            tries += 1
        print('Game won in {} tries.'.format(tries))
    else:
        solve(gen_board(dims, mines), serial=serial)
