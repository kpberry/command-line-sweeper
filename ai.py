from minesweeping import gen_board, get_mine_counts, select
from nd_minesweeper import print_known
import numpy as np
from random import choice


def select_random_unknown_index(known, marked):
    unknown = (known < 0) & (marked < 1)
    return choice(np.transpose(np.nonzero(unknown)).tolist())


def select_safe_indices(known, marked):
    marked_counts = get_mine_counts(marked)
    satisfied = (marked_counts == known) & (known > 0)
    safe_indices = get_mine_counts(satisfied) * (known < 0) * (marked < 1)
    return np.transpose(np.nonzero(safe_indices))


def mark_mines(known, marked):
    unknown = get_mine_counts(known < 0)
    satisfied = (unknown == known) & (known > 0)
    new_marked = np.round(get_mine_counts(satisfied) * (known < 0))
    marked[(marked + new_marked) > 0] = 1


def solve(board, counts, known):
    marked = np.zeros(known.shape)
    prev_known, prev_marked = None, None
    while True:
        if np.sum(prev_known) == np.sum(known)\
                and np.sum(prev_marked) == np.sum(marked):
            index = select_random_unknown_index(known, marked)
            safe = select(index, board, counts, known)
            if not safe:
                print('You lose! (random selection)')
                break
        prev_known = known.copy()
        prev_marked = marked.copy()
        mark_mines(known, marked)
        indices = select_safe_indices(known, marked)
        for index in indices[:1]:
            safe = select(index, board, counts, known)
            if not safe:
                print('You lose! (assertion fail)')
                break
        print(known)
        assert np.sum((known > 0) * board) == 0
        print(np.sum(marked))
        if np.sum(board) == np.sum(marked):
            assert np.sum(board * marked) == np.sum(board)
            print('You win!')
            break


if __name__ == "__main__":
    # Figure out why it works (okay) for 20x25, but totally breaks for 20x26
    dims = [20, 20]
    board = gen_board(dims, 50)
    counts = get_mine_counts(board)
    known = np.ones(dims) * -1

    solve(board, counts, known)
