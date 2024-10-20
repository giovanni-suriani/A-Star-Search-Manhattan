import heapq, copy
from queue import LifoQueue, Queue


IDEAL_BOARD = ['_', '1', '2', '3', '4', '5', '6', '7', '8']
              #['_', '1', '2', '3', '4', '5', '6', '7', '8']
TEST_BOARD = ['7','2','4','5','_','6','8','3','1']
TEST_BOARD2 = ['1','2','3','4','5','6','7','8','_']
TEST_BOARD3 = ['1','4','2','3','_','5','6','7','8']


class PriorityQueue:
    # Fila de prioridade minima, onde o menor valor é o de maior prioridade!!
    def __init__(self):
        self._queue = [] # Lista de tuplas (prioridade, index, item)
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

    def is_empty(self):
        return len(self._queue) == 0
    
    def __str__(self) -> str:
        a = ''
        for vertex in [t[2] for t in self._queue]:
            a += 'f(n) = '+ str(vertex.total_cost) + ','
        a = a[:-1]
        return a
    
    def __repr__(self):
        return self.__str__()

class Vertex:
    def __init__(self, board_config: list, predecessor=None, cost_g=0):
        self.board_config = board_config
        self.visited = False
        self.predecessor: Vertex = predecessor
        self.heuristic = self.calculate_heuristic()
        self.cost_g = cost_g
        
    def calculate_heuristic_each_piece(self, piece):
        if piece == '_':
            return 0
        place_at_board = self.board_config.index(piece)
        ideal_place = IDEAL_BOARD.index(piece)
        y_distance = abs(ideal_place // 3 - place_at_board // 3)  # Floor division
        x_distance = abs(place_at_board % 3 - ideal_place % 3)
        return x_distance + y_distance
    
    def calculate_heuristic(self):
        if IDEAL_BOARD is None:
            raise ValueError("Heuristic Board was not defined")
        return sum([self.calculate_heuristic_each_piece(piece) for piece in self.board_config])

    @property
    def total_cost(self):
        # g(n) + h(n)
        return self.cost_g + self.heuristic

    def change_void_to_right(self):
        void_position = self.board_config.index('_')
        if void_position % 3 == 2:
            raise ValueError("Void is at the leftmost position")
        piece_heuristic_before = self.calculate_heuristic_each_piece(self.board_config[void_position + 1])
        self.board_config[void_position] = self.board_config[void_position + 1]
        self.board_config[void_position + 1] = '_'
        piece_heuristic_now = self.calculate_heuristic_each_piece(self.board_config[void_position])
        # Otimizacao, nao precisa recalcular toda heuristica, somente o que mudou
        self.heuristic = self.heuristic + piece_heuristic_now - piece_heuristic_before
        
    def change_void_to_left(self):
        void_position = self.board_config.index('_')
        if void_position % 3 == 0:
            raise ValueError("Void is at the rightmost position")
        piece_heuristic_before = self.calculate_heuristic_each_piece(self.board_config[void_position - 1])
        self.board_config[void_position] = self.board_config[void_position - 1]
        self.board_config[void_position - 1] = '_'
        piece_heuristic_now = self.calculate_heuristic_each_piece(self.board_config[void_position])
        self.heuristic = self.heuristic + piece_heuristic_now - piece_heuristic_before
    
    def change_void_to_up(self):
        void_position = self.board_config.index('_')
        if void_position // 3 == 0:
            raise ValueError("Void is at the most top position")
        piece_heuristic_before = self.calculate_heuristic_each_piece(self.board_config[void_position - 3])
        self.board_config[void_position] = self.board_config[void_position - 3]
        self.board_config[void_position - 3] = '_'
        piece_heuristic_now = self.calculate_heuristic_each_piece(self.board_config[void_position])
        self.heuristic = self.heuristic + piece_heuristic_now - piece_heuristic_before
        
    def change_void_to_down(self):
        void_position = self.board_config.index('_')
        if void_position // 3 == 2:
            raise ValueError("Void is at the most bottom position")
        piece_heuristic_before = self.calculate_heuristic_each_piece(self.board_config[void_position + 3])
        self.board_config[void_position] = self.board_config[void_position + 3]
        self.board_config[void_position + 3] = '_'
        piece_heuristic_now = self.calculate_heuristic_each_piece(self.board_config[void_position])
        self.heuristic = self.heuristic + piece_heuristic_now - piece_heuristic_before

    def clone(self, predecessor=None):
        # Clona com predecessor
        if predecessor:
            return Vertex(copy.deepcopy(self.board_config), predecessor, predecessor.cost_g + 1)
        else:
            return Vertex(copy.deepcopy(self.board_config), predecessor)

    def __eq__(self, vertex):
        # Comparacao de igualdade de dois vertices
        # O ideal seria comparar pela referencia, sem precisar desse metodo
        # Pois comparacao de listas é da ordem de O(n) e referencia O(1)
        return self.board_config == vertex.board_config

    def __str__(self):
        board_str = str(self.board_config[:3]) + "\n" + str(self.board_config[3:6]) + "\n" + str(self.board_config[6:])
        return board_str + "\n" + "f(n) = " + str(self.cost_g) + " + " + str(self.heuristic)

    def __repr__(self):
        return "h(n) = " + str(self.heuristic)



class Graph:
    def __init__(self, initial_board_config:Vertex):
        self.initial_board_config = initial_board_config
        self.queue = PriorityQueue()
        self.queue.push(initial_board_config, initial_board_config.total_cost)
        self.tested_boards = [] # Lista de vertices testados
        
    def push_neighbors(self, vertex):
        if vertex.board_config.index('_') is not None:
            void_place = vertex.board_config.index('_')
            can_go_left = void_place % 3 != 0
            can_go_right = void_place % 3 != 2
            can_go_up = void_place // 3 != 0
            can_go_down = void_place // 3 != 2
            
            if can_go_left:
                vertex_left = vertex.clone(vertex) # Nao tem como colocar em uma linha as duas operacoes, retorna none implicitamente
                vertex_left.change_void_to_left()
                if not self.was_tested(vertex_left):
                    self.queue.push(vertex_left, vertex_left.total_cost)

            if can_go_right:
                vertex_right = vertex.clone(vertex)
                vertex_right.change_void_to_right()
                if not self.was_tested(vertex_right):
                    self.queue.push(vertex_right, vertex_right.total_cost)

            if can_go_up:
                vertex_up = vertex.clone(vertex)
                vertex_up.change_void_to_up()
                if not self.was_tested(vertex_up):
                    self.queue.push(vertex_up, vertex_up.total_cost)
                
            if can_go_down:
                vertex_down = vertex.clone(vertex)
                vertex_down.change_void_to_down()
                if not self.was_tested(vertex_down):
                    self.queue.push(vertex_down, vertex_down.total_cost)
                
        else:
            raise ValueError("Void is not in the board")
        
    def a_star_local_search(self, vertex):
        if self.test_condition(vertex):
            return True
        print(vertex)
        self.push_neighbors(vertex)
        self.tested_boards.append(vertex)
    
    def a_star_search(self):
        finished = False  
        while not self.queue.is_empty() or finished is False:
            #print(self.queue)
            vertex_to_analyze = self.queue.pop()
            finished = self.a_star_local_search(vertex_to_analyze)
            if finished:
                print("A* Search finished successfully, here's the path to the solution:")
                self.print_path(vertex_to_analyze)
                return
        raise ValueError("A* Search was not able to find a solution")

    def print_path(self, vertex):
        answer = []
        while vertex.predecessor:
            answer.append(str(vertex) + "\n")
            vertex = vertex.predecessor
        answer.append(str(vertex) + "\n")
        for i in range(len(answer) - 1, -1, -1):
            print(answer[i])
        

    def test_condition(self, vertex: Vertex):
        return vertex.board_config == IDEAL_BOARD
    
    def was_tested(self, vertex: Vertex):
        return vertex in self.tested_boards
    
    def __str__(self):
        return str(self.initial_board_config)
    
    def __repr__(self):
        return self.str


def a_star():
    initial_vertex = Vertex(TEST_BOARD)
    graph = Graph(initial_vertex)
    graph.a_star_search()
    
    
    #initial_vertex = Vertex(TEST_BOARD)
    #test_vertex = Vertex(TEST_BOARD2)
    #copy_vertex = initial_vertex.clone()
    #copy_vertex.cost_g = 2
    #list_vertex = [initial_vertex, test_vertex]
    #print(copy_vertex in list_vertex)
    

a_star()
