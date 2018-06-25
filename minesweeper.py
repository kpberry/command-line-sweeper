from minesweeping import gen_board, get_mine_counts, select
import numpy as np
import curses
import re


def get_known_string(known, flags):
    unknown_mask = known == -1
    zero_mask = known == 0
    flag_mask = flags == 1
    array_string = known.astype('U1')
    array_string[unknown_mask] = '■'
    array_string[zero_mask] = ' '
    array_string[flag_mask] = '*'
    array_string = np.array2string(array_string, max_line_width=1000)
    return re.sub(r'\'| *\[+|\]+', '', array_string)


def get_game_over_string(board, counts):
    zero_mask = counts == 0
    array_string = counts.astype('U1')
    array_string[zero_mask] = ' '
    array_string[board > 0] = 'X'
    array_string = np.array2string(array_string, max_line_width=1000)
    return re.sub(r'\'| *\[+|\]+', '', array_string)


def display_screen(screen_string, screen, colors, offset_x=0, offset_y=0):
    cur_x, cur_y = offset_x, offset_y
    for line in screen_string.split('\n'):
        for c in line:
            if c in colors:
                screen.addch(cur_y, cur_x, ord(c), colors[c] | curses.A_BOLD)
            else:
                screen.addch(cur_y, cur_x, c)
            cur_x += 1
        cur_y += 1
        cur_x = offset_x


def play_game(dims, mines):
    board = gen_board(dims, mines)
    counts = get_mine_counts(board)
    known = np.ones(dims) * -1
    flags = np.zeros(dims)

    screen = curses.initscr()
    screen.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_RED)
    colors = {
        '1': curses.color_pair(1),
        '2': curses.color_pair(2),
        '3': curses.color_pair(3),
        '4': curses.color_pair(4),
        '5': curses.color_pair(5),
        '6': curses.color_pair(6),
        '7': curses.color_pair(7),
        '8': curses.color_pair(8),
        '*': curses.color_pair(9),
        'X': curses.color_pair(10)
    }
    screen_dims = screen.getmaxyx()
    offset = [
        int((screen_dims[1] - dims[1] * 2) / 2),
        int((screen_dims[0] - dims[0]) / 2)
    ]
    x, y = 0, 0
    key = ''
    while key != 'q':
        screen.clear()
        display_screen(get_known_string(known, flags), screen,
                       colors, offset[0], offset[1])
        screen.addstr(0, 0,
                      'Press q to quit, ENTER to select a square, and f to flag a mine.',
                      curses.A_BOLD)
        screen.move(y + offset[1], x + offset[0])
        key = chr(screen.getch())
        if (key == 'w' or ord(key) == curses.KEY_UP) and y > 0:
            y -= 1
        elif (key == 's' or ord(key) == curses.KEY_DOWN) and y < dims[0] - 1:
            y += 1
        elif (key == 'a' or ord(key) == curses.KEY_LEFT) and x > 0:
            x -= 2
        elif (key == 'd' or ord(key) == curses.KEY_RIGHT) and x < (dims[1] - 1) * 2:
            x += 2
        elif key == 'f' and (known[y, int(x / 2)] < 0 or flags[y, int(x / 2)] > 0):
            flags[y, int(x / 2)] = 1 - flags[y, int(x / 2)]
        elif key == '\n' and not flags[y, int(x / 2)]:
            safe = select([int(y), int(x / 2)], board, counts, known)
            if not safe:
                screen.clear()
                display_screen(get_game_over_string(
                    board, counts), screen, colors, offset[0], offset[1])
                screen.addstr(
                    0, 0, 'You lose! Press ENTER to play again.', curses.A_BOLD)
                screen.getch()
                break
            elif np.sum(known == -1) == mines:
                screen.clear()
                display_screen(get_game_over_string(
                    board, counts), screen, colors, offset[0], offset[1])
                screen.addstr(
                    0, 0, 'You win! Press ENTER to play again.', curses.A_BOLD)
                screen.getch()
                break
        screen.refresh()
    curses.endwin()
    return key


if __name__ == '__main__':
    key = ''
    while key != 'q':
        key = play_game([16, 30], 99)
