import copy
import random
import itertools


class Engine:
    def get_config_args(self):
        return self.players, self.get_board_representation(), self.num_blocked, self.num_holes, self.seed, self.players_points

    def __init__(self, players, board, blocked, holes=1, seed=None, player_points=None):
        self.seed = seed
        self.GRAPH = 'GRAPH'
        self.FILLED = 'FILLED'
        self.BLOCKED = -1
        self.players = players  # players -> colors map
        self.num_players = len(players)
        self.num_nodes = len(board[self.GRAPH])
        self.board = board  # 'GRAPH' -> nodeID -> neighbors, 'FILLED' -> nodeID -> color, points
        self.whose_turn = 0
        self.num_blocked = blocked
        self.num_holes = holes
        self.move_stack = []
        self.__check_assertions()
        if self.seed: random.seed(self.seed)
        if player_points is not None:
            self.players_points = player_points
        else:
            self.__make_player_points()
        self.__block_random_points()

    def __block_random_points(self):
        blocked_nodes = random.choices(list(self.board[self.GRAPH].keys()), k=self.num_blocked)
        for node in blocked_nodes:
            self.board[self.FILLED][node] = self.BLOCKED, 0

    def __make_player_points(self):
        self.players_points = {}
        for player in range(self.num_players):
            points_range = list(
                range(1, int((self.num_nodes - self.num_blocked - self.num_holes) / self.num_players) + 1))
            self.players_points[player] = points_range

    def __check_assertions(self):
        assert self.num_players > 0, "Invalid num_players = %d" % (self.num_players)
        assert self.GRAPH in self.board, "No \"GRAPH\" in board provided"
        assert self.FILLED in self.board, "No \"FILLED\" in board provided"
        assert self.num_players < self.num_nodes, "Too many players %d or too few nodes in graph = %d" % (
            self.num_players, self.num_nodes)
        assert self.num_nodes > self.num_blocked, "Too many blocked nodes = %d" % self.num_blocked
        assert (self.num_nodes - self.num_blocked - self.num_holes) % self.num_players == 0
        for i in range(0, self.num_players):
            assert i in self.players, "Player %d not in player -> color map" % i
            # assert players[i] is valid color, ""

    def undo_move(self):
        (node_id, player, points) = self.move_stack[-1]
        self.move_stack = self.move_stack[0:-2]
        del self.board[self.FILLED][node_id]
        self.players_points[player].append(points)
        self.whose_turn = player

    def make_move(self, player, node_id, points):
        assert player == self.whose_turn, "Not the right player\'s turn"
        assert node_id in self.board[self.GRAPH], "Node id %d not in graph" % node_id
        assert points in range(1, int((self.num_nodes - self.num_blocked - self.num_holes) / self.num_players) + 1), \
            "Invalid points bet %d. Must be in (%d,%d)" \
            % (points, 1, int((self.num_nodes - self.num_blocked - self.num_holes) / self.num_players) + 1)
        assert points in self.players_points[player], "Already used up %d points bet before" % points
        assert node_id not in self.board[self.FILLED].keys(), "Duplicate Move"
        assert player != -1, "Aha"
        self.board[self.FILLED][node_id] = player, points
        self.players_points[player].remove(points)
        self.whose_turn = (self.whose_turn + 1) % self.num_players
        self.move_stack.append((node_id, player, points))

    def has_winner(self):
        return len(self.board[self.FILLED]) == self.num_nodes - self.num_holes

    def compute_player_scores(self, empty_cells):
        player_scores = {}
        for empty_cell in empty_cells:
            neighbors = self.board[self.GRAPH][empty_cell]
            for neighbor in neighbors:
                player_there, points = self.board[self.FILLED][neighbor]
                player_scores[player_there] = player_scores.get(player_there, 0) + points
        return player_scores

    def __compute_best_players_and_score(self, player_scores):
        max_score = -1
        max_players = []
        for player in player_scores:
            if max_score < player_scores[player]:
                max_score = player_scores[player]
                max_players = [player]
            elif max_score == player_scores[player]:
                max_players.append(player)
        return max_players, max_score

    def get_valid_moves(self):
        if self.has_winner():
            return None
        empty_cells = set(self.board[self.GRAPH].keys()).difference(set(self.board[self.FILLED].keys()))
        valid_points = self.players_points[self.whose_turn]
        p = list(itertools.product([self.whose_turn], empty_cells, valid_points))
        if len(p) < 1:
            _ = 0
        return p

    def get_winners(self):
        if len(self.board[self.FILLED]) < self.num_nodes - self.num_holes:
            return -1
        # get open space and get sum of points around it by player and take max
        empty_cells = set(self.board[self.GRAPH].keys()).difference(set(self.board[self.FILLED].keys()))
        assert len(empty_cells) == self.num_holes, "More empty than allowed at end of game %d vs %d" % (
            len(empty_cells), self.num_holes)
        player_scores = self.compute_player_scores(empty_cells)
        best_players, best_score = self.__compute_best_players_and_score(player_scores)
        return best_players, best_score

    def get_board_representation(self):
        return copy.deepcopy(self.board)
