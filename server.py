import random

from engine import Engine
from ui_networkx import UINetworkx


def board_factory():
    board_graph = {}
    for i in range(1, max_i + 1):
        for j in range(1, i + 1):
            num = sum_to(i - 1) + j
            toAdd = []
            if j > 1:
                toAdd.append(num - i)
                toAdd.append(num - 1)
            if j < i:
                toAdd.append(num - i + 1)
                toAdd.append(num + 1)
            if i <= max_i - 1:
                toAdd.append(num + i)
                toAdd.append(num + i + 1)
            board_graph[num] = toAdd

    board = {}
    board['GRAPH'] = board_graph
    board['FILLED'] = {}
    return board


def conv(board_filled, tot):
    x = []
    trans = {0: 'g', 1: 'b', -1: 'r'}
    for i in range(1, tot + 1):
        try:
            x.append(trans[board_filled[i][0]])
        except KeyError:
            x.append('y')
    return x


# board_graph = {}
# board_graph[1] = [2, 3]
# board_graph[2] = [1, 3, 4, 5]
# board_graph[3] = [1, 2, 5, 6]
# board_graph[4] = [2, 5]
# board_graph[5] = [2, 3, 4, 6]
# board_graph[6] = [3, 5]
max_i = 3


def sum_to(n):
    return (n * (n + 1)) // 2


def make_pos(max_n):
    pos = {}
    for i in range(1, max_n + 1):
        for j in range(1, i + 1):
            num = sum_to(i - 1) + j
            pos[num] = (-(i - 1) + 2 * (j - 1), -i)
    return pos


# pos = {1: (0, 0), 2: (-1, -1), 3: (1, -1), 4: (-2, -2), 5: (0, -2), 6: (2, -2)}
pos = make_pos(max_i)
ui = UINetworkx(board=board_factory(), pos=pos)


def get_move(board):
    s = input('Enter Move -> number:bet\n')
    number = s.split(':')[0]
    bet = s.split(':')[1]
    return int(number), int(bet)


# player = 0
# while not eng.has_winner():
#     ui.update_board(board=board, colors=conv(board["FILLED"], sum_to(max_i)))
#     number, bet = get_move(eng.get_board_representation())
#     eng.make_move(node_id=number, player=player, points=bet)
#     player = 1 - player
# # eng.undo_move()
# print(eng.has_winner())
# print(eng.get_winners())


def random_agent(board):
    return random.choice(eng.get_valid_moves())


def reflex_agent(board):
    for move in eng.get_valid_moves():
        eng.make_move(*move)
        b = eng.has_winner()
        eng.undo_move()
        if b:
            return move
    return random.choice(eng.get_valid_moves())


player = 0
scores = {0: 0, 1: 0, -1: 0}
num_games = 1000
for i in range(num_games):
    eng = Engine(board=board_factory(), blocked=1, players={0: 0, 1: 1})
    while not eng.has_winner():
        if player == 0:
            eng.make_move(*random_agent(eng.get_board_representation()))
        else:
            eng.make_move(*reflex_agent(eng.get_board_representation()))

        player = 1 - player
    winner = eng.get_winners()[0]
    if len(winner) == 2:
        scores[-1] = scores[-1] + 1
    else:
        scores[winner[0]] = scores[winner[0]] + 1
print(scores)
