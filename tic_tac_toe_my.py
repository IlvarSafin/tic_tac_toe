from math import inf as infinity
from random import choice
import time
from os import system
 
HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
 
 
def evaluate(state):
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0
 
    return score
 
 
def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False
 
 
def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)
 
 
def empty_cells(state):
    cells = []
 
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
 
    return cells
 
 
def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False
 
 
def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False
 
 
def minimax(state, depth, player):
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]
 
    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]
 
    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y
 
        if player == COMP:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score
 
    return best
 
 
def clean():
    system('cls')
 
 
def render(state, c_choice, h_choice):
    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'
 
    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)
 
def random_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return
 
    clean()
    print(f'Бот ходит с [{c_choice}]')
    render(board, c_choice, h_choice)
    move = choice(empty_cells(board))
    x = move[0]
    y = move[1]
       
 
    set_move(x, y, COMP)
    #time.sleep(1)
 
def ai_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return
 
    clean()
    print(f'Бот ходит с [{c_choice}]')
    render(board, c_choice, h_choice)
 
    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]
 
    set_move(x, y, COMP)
    #time.sleep(1)
 
 
def human_turn(c_choice, h_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return
 
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }
 
    clean()
    print(f'Ты ходишь с [{h_choice}]')
    render(board, c_choice, h_choice)
 
    while move < 1 or move > 9:
        move = input('Нажми на (1..9): ')
        if str(move) < '1' or str(move) > '9':
            move = 0
            continue
        move = int(move)
        coord = moves[move]
        can_move = set_move(coord[0], coord[1], HUMAN)
 
        if not can_move:
            print('Плохой ход!')
            move = -1
 
def main():
    clean()
    h_choice = ''
    c_choice = ''
    first = ''
    mode = 0
 
    while mode != 1 and mode != 2:
        mode = int(input("Режим:\n1: Randomm\n2: Smart\nВыберите:"))
    while h_choice != 'O' and h_choice != 'X':
        print('')
        h_choice = input('Выбери X или O\nВыбор: ').upper()
 
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'
 
    clean()
    while first != 'Y' and first != 'N':
        first = input('Начнешь первым?[y/n]: ').upper()
 
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            if mode == 2:
                ai_turn(c_choice, h_choice)
            else:
                random_turn(c_choice, h_choice)
            first = ''
 
        human_turn(c_choice, h_choice)
        if mode == 2:
            ai_turn(c_choice, h_choice)
        else:
            random_turn(c_choice, h_choice)
 
 
    if wins(board, HUMAN):
        clean()
        print(f'Ты ходишь с [{h_choice}]')
        render(board, c_choice, h_choice)
        print('Ты выграл!')
    elif wins(board, COMP):
        clean()
        print(f'Бот ходит с [{c_choice}]')
        render(board, c_choice, h_choice)
        print('Ты проиграл!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('Ничья!')
 
    exit()
 
main()
