import heapq
from queue import LifoQueue, Queue


IDEAL_BOARD = ['_','1','2','3','4','5','6','7','8']



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
        def __init__(self, board_config: list, predecessor = None):
            self.board_config = board_config
            self.visited = False
            self.predecessor: Vertex = predecessor
            self.heuristic = self.calculate_heuristic(IDEAL_BOARD) 
            
        def calculate_heuristic(self):
            if IDEAL_BOARD is None:
                raise ValueError("Heuristic was not defined")
            return 1
        
        @property
        def total_cost(self):
            return 1 + self.heuristic
        
        def clone(self):
            return Vertex(self.board_config, self.predecessor)

        def __str__(self):
            board_str = str(self.board_config[:3]) + "\n" + str(self.board_config[3:6]) + "\n" + str(self.board_config[6:])
            return board_str + "\n" + "Cost = 1 + " + str(self.heuristic)
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
    initial_vertex = Vertex(IDEAL_BOARD)
    graph = Graph(initial_vertex)
    print(graph)
    
a_star()