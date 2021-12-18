from collections import defaultdict

def main():
    grid = get_input()
    part1(grid)
    part2(grid)
    return 0

def get_input():
    f = open("input.txt", "r")
    grid = []
    for line in f:
        grid.append(list(map(int,line.strip())))
    return grid

def part1(grid):
    node_count = len(grid) * len(grid[0])
    g = Graph(node_count, grid)
    return 0

def part2(grid):
    modified_grid = extend_grid(grid)
    node_count = len(modified_grid) * len(modified_grid[0])
    g = Graph(node_count, modified_grid)
    return 0

def extend_grid(grid):
    extended_grid = []
    for i in range(len(grid) * 5):
        temp_grid = []
        for j in range(len(grid[0]) * 5):
            temp_grid.append(0)
        extended_grid.append(temp_grid)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            initial_value = grid[i][j]
            increased_values = generate_increased_numbers(initial_value)
            grid_size = len(grid)
            for x in range(5):
                for y in range(5):
                    extended_grid[(x * grid_size) + i][(y * grid_size) + j] = increased_values[x][y]
    return extended_grid

def fill_extended_grid(start_coordinate, grid, extended_grid):
    initial_value = grid[start_coordinate[0]][start_coordinate[1]]
    increased_values = generate_increased_numbers(initial_value)
    grid_size = len(grid)
    for i in range(5):
        for j in range(5):
            extended_grid[i * grid_size][j * grid_size] = increased_values[i][j]


def generate_increased_numbers(initial_number):
    increased_number_grid = []
    for i in range(5):
        temp_grid = []
        for j in range(5):
            temp_number = initial_number + i + j
            if temp_number > 9:
                temp_number -= 9
            # print(temp_number)
            temp_grid.append(temp_number)
        increased_number_grid.append(temp_grid)
    return increased_number_grid

class Node_Distance :
    def __init__(self, name, dist):
        self.name = name
        self.dist = dist

class Graph :
    def __init__ (self, node_count, grid) :
        self.adjlist = defaultdict(list)
        self.node_count = node_count
        self.grid = grid
        self.build()
        self.Dijkstras_Shortest_Path(0)

    def build(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                valid_neighbouring_tiles = self.get_neighbouring_tiles(i,j)
                this_coordinate = ((i * len(self.grid)) + j)
                weight = self.grid[i][j]
                for elem in valid_neighbouring_tiles:
                    self.Add_Into_Adjlist(elem, Node_Distance(this_coordinate, weight))

    def get_neighbouring_tiles(self, i,j):
        neighbouring_coordinates = []
        A = (i + 1, j)
        B = (i - 1, j)
        C = (i, j + 1)
        D = (i, j - 1)

        if self.is_valid(A) == True:
            neighbouring_coordinates.append(self.convert_coordinate_to_number(A))
        if self.is_valid(B) == True:
            neighbouring_coordinates.append(self.convert_coordinate_to_number(B))
        if self.is_valid(C) == True:
            neighbouring_coordinates.append(self.convert_coordinate_to_number(C))
        if self.is_valid(D) == True:
            neighbouring_coordinates.append(self.convert_coordinate_to_number(D))
        return neighbouring_coordinates

    def convert_coordinate_to_number(self, coordinate):
        this_coordinate = ((coordinate[0] * len(self.grid)) + coordinate[1])
        return this_coordinate

    def is_valid(self, coordinate):
        if coordinate[0] < 0 or coordinate[1] < 0:
            return False
        if coordinate[0] >= len(self.grid):
            return False
        if  coordinate[1] >= len(self.grid[0]):
            return False
        else:
            return True

    def Add_Into_Adjlist (self, src, node_dist):
        self.adjlist[src].append(node_dist)

    def Dijkstras_Shortest_Path (self, source):
        distance = [999999999999] * self.node_count
        distance[source] = 0

        dict_node_length = {source: 0}

        while dict_node_length :
            current_source_node = min(dict_node_length, key = lambda k: dict_node_length[k])
            del dict_node_length[current_source_node]

            for node_dist in self.adjlist[current_source_node] :
                adjnode = node_dist.name
                length_to_adjnode = node_dist.dist

                if distance[adjnode] > distance[current_source_node] + length_to_adjnode :
                    distance[adjnode] = distance[current_source_node] + length_to_adjnode
                    dict_node_length[adjnode] = distance[adjnode]

        print(distance[self.node_count - 1])

main()
