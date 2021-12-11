def main():
    cave_map = get_input()
    low_coordinates = part1(cave_map)
    part2(cave_map, low_coordinates)
    return 0

def get_input():
    f = open("input.txt", "r")
    cave_map = []
    for line in f:
        cave_map.append(list(line.strip()))
    return cave_map

def part1(cave_map):
    risk_points = 0
    low_coordinates = []
    for i in range(len(cave_map)):
        for j in range(len(cave_map[i])):
            if is_lower_than_neighbours(cave_map, i, j) == True:
                risk_points += (1 + int((cave_map[i][j])))
                low_coordinates.append((i,j))        
    print(risk_points)
    return low_coordinates

def is_lower_than_neighbours(cave_map, i, j):
    current_coord_value = cave_map[i][j]
    neighbouring_coordinates = []
    A = (i + 1, j)
    if is_valid_coord(cave_map, A) == True:
        neighbouring_coordinates.append(A)
    B = (i - 1, j)
    if is_valid_coord(cave_map, B) == True:
        neighbouring_coordinates.append(B)
    C = (i, j + 1)
    if is_valid_coord(cave_map, C) == True:
        neighbouring_coordinates.append(C)
    D = (i, j - 1)
    if is_valid_coord(cave_map, D) == True:
        neighbouring_coordinates.append(D)
    for elem in neighbouring_coordinates:
        if current_coord_value >= cave_map[elem[0]][elem[1]]:
            return False
    return True

def part2(cave_map, low_coordinates):
    list_of_basin_sizes = []
    for elem in low_coordinates:
        list_of_basin_sizes.append(calculate_basin_site(cave_map, elem))
    list_of_basin_sizes.sort(reverse=True)
    print(list_of_basin_sizes[0] * list_of_basin_sizes[1] * list_of_basin_sizes[2])
    return 0

def calculate_basin_site(cave_map, start_coordinate):
    basin = {start_coordinate}
    calculate_basin_site_recursive(cave_map, start_coordinate, basin)
    return len(basin)

def calculate_basin_site_recursive(cave_map, start_coordinate, basin):
    neighbouring_tiles = get_neighbouring_tiles(cave_map, start_coordinate)
    current_coordinate_value = cave_map[start_coordinate[0]][start_coordinate[1]]
    for elem in neighbouring_tiles:
        if elem in basin:
            continue
        elif is_valid_coord(cave_map, elem) == True:
            if int(cave_map[elem[0]][elem[1]]) > int(current_coordinate_value) and int(cave_map[elem[0]][elem[1]]) != 9:
                basin.add(elem)
                calculate_basin_site_recursive(cave_map, elem, basin)


def get_neighbouring_tiles(cave_map, start_coordinate):
    neighbouring_tiles = []
    neighbouring_tiles.append((start_coordinate[0] + 1, start_coordinate[1]))
    neighbouring_tiles.append((start_coordinate[0] - 1, start_coordinate[1]))
    neighbouring_tiles.append((start_coordinate[0], start_coordinate[1] + 1))
    neighbouring_tiles.append((start_coordinate[0], start_coordinate[1] - 1))
    return neighbouring_tiles

def is_valid_coord(cave_map, elem):
    if (elem[0] < 0) or  (elem[1] < 0):
        return False
    elif (elem[0] > len(cave_map) - 1) or  (elem[1] > len(cave_map[0]) - 1):
        return False
    return True

main()