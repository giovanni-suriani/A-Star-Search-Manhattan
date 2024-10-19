import heapq
from queue import LifoQueue, Queue


IDEAL_BOARD = ['_','1','2','3','4','5','6','7','8']
TEST_BOARD2 = ['1','2','3','4','5','6','7','8','_']
TEST_BOARD = ['7','2','4','5','_','6','8','3','1']


class PriorityQueue:
    # Fila de prioridade minima, onde o menor valor é o de maior prioridade!!
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

    def is_empty(self):
        return len(self._queue) == 0
    
    def __repr__(self):
        return str(self._queue)

class Vertex:
    def __init__(self, board_config: list, predecessor=None):
        self.board_config = board_config
        self.visited = False
        self.predecessor: Vertex = predecessor
        self.heuristic = self.calculate_heuristic()
        if predecessor:
            self.cost_g = 1 + predecessor.cost_g
        else:
            self.cost_g = 0

    def calculate_heuristic(self):
        def calculate_heuristic_each_piece(piece):
            if piece == '_':
                return 0
            place_at_board = self.board_config.index(piece)
            ideal_place = IDEAL_BOARD.index(piece)
            y_distance = abs(ideal_place // 3 - place_at_board // 3)  # Floor division
            x_distance = abs(place_at_board % 3 - ideal_place % 3)
            return x_distance + y_distance
        if IDEAL_BOARD is None:
            raise ValueError("Heuristic was not defined")
        return sum([calculate_heuristic_each_piece(piece) for piece in self.board_config])

    @property
    def total_cost(self):
        # g(n) + h(n)
        return self.cost_g + self.heuristic

    def clone(self):
        return Vertex(self.board_config, self.predecessor)

    def __str__(self):
        board_str = str(self.board_config[:3]) + "\n" + str(self.board_config[3:6]) + "\n" + str(self.board_config[6:])
        return board_str + "\n" + "f(n) = " + str(self.cost_g) + " + " + str(self.heuristic)

class Graph:
    def __init__(self, initial_board_config:Vertex):
        self.initial_board_config = initial_board_config
        
    def get_neighbors(self, vertex: Vertex):
        # TODO
        # Get the neighbors of the vertex
        pass
        
    def test_condition(self, vertex: Vertex):
        return vertex.board_config == IDEAL_BOARD
    
    def __str__(self):
        return str(self.initial_board_config)# + "\n" + str(self.initial_board_config[3:5]) + "\n" + str(self.initial_board_config[6:])
    
    def __repr__(self):
        return self.str


def a_star():
    initial_vertex = Vertex(TEST_BOARD)
    graph = Graph(initial_vertex)
    print(graph)

a_star()
