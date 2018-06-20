import networkx as nx
import matplotlib.pyplot as plt

from ui import UI


class UINetworkx(UI):
    def __init__(self, board, pos):
        # board:  'GRAPH' -> nodeID -> neighbors, 'FILLED' -> nodeID -> color, points
        self.GRAPH = 'GRAPH'
        self.FILLED = 'FILLED'
        self.board_graph = nx.Graph()
        p = list(board[self.GRAPH].keys())
        self.board_graph.add_nodes_from(p)
        for vertex in board[self.GRAPH].keys():
            for sink in board[self.GRAPH][vertex]:
                self.board_graph.add_edge(vertex, sink)
        self.pos = pos

    def update_board(self, board, colors):
        labels = {}
        for i in board['GRAPH'].keys():
            if i in board['FILLED'].keys():
                labels[i] = board['FILLED'][i][1]
            else:
                labels[i] = i
        nx.draw(self.board_graph, pos=self.pos, node_color=colors, labels=labels)
        plt.show()
