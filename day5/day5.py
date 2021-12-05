def main():
    my_input = get_input()
    coordinates_frequency = part1(my_input)
    part2(my_input, coordinates_frequency)
    return 0

def get_input():
    coordinates = []
    with open("input.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            temp_line = line.strip().split()
            coordinates.append((temp_line[0].split(","), temp_line[2].split(",")))
    return coordinates

def part1(my_input):
    coordinates_frequency = {}
    for elem in my_input:
        find_connecting_coordinates(elem[0], elem[1], coordinates_frequency)
    two_or_more = count_frequencies(coordinates_frequency)
    print(two_or_more)
    return coordinates_frequency

def find_connecting_coordinates(coord1, coord2, coordinates_frequency):
    coord1_x = int(coord1[0])
    coord1_y = int(coord1[1])

    coord2_x = int(coord2[0])
    coord2_y = int(coord2[1])

    x_difference = coord1_x - coord2_x
    y_difference = coord1_y - coord2_y

    if (x_difference == 0):
        if (y_difference > 0):
            for i in range(abs(y_difference) + 1):
                add_coord_to_dictionary((coord1_x,  coord2_y + i), coordinates_frequency)
                
        else:
            for i in range(abs(y_difference) + 1):
                add_coord_to_dictionary((coord1_x,  coord2_y - i), coordinates_frequency)
    
    if (y_difference == 0):
        if (x_difference > 0):
            for i in range(abs(x_difference) + 1):
                add_coord_to_dictionary((coord1_x - i,  coord2_y), coordinates_frequency)
        else:
            for i in range(abs(x_difference) + 1):
                add_coord_to_dictionary((coord1_x + i,  coord2_y), coordinates_frequency)

def find_diagonal_coordinates(coord1, coord2, coordinates_frequency):
    coord1_x = int(coord1[0])
    coord1_y = int(coord1[1])

    coord2_x = int(coord2[0])
    coord2_y = int(coord2[1])

    x_difference = coord1_x - coord2_x
    y_difference = coord1_y - coord2_y

    if (x_difference > 0):
        if (y_difference > 0):
            for i in range(abs(x_difference) + 1):
                add_coord_to_dictionary((coord1_x - i,  coord1_y - i), coordinates_frequency)
        if (y_difference < 0):
            for i in range(abs(x_difference) + 1):
                add_coord_to_dictionary((coord1_x - i,  coord1_y + i), coordinates_frequency)
    
    if (x_difference < 0):
        if (y_difference > 0):
            for i in range(abs(x_difference) + 1):
                add_coord_to_dictionary((coord1_x + i,  coord1_y - i), coordinates_frequency)
        if (y_difference < 0):
            for i in range(abs(x_difference) + 1):
                add_coord_to_dictionary((coord1_x + i,  coord1_y + i), coordinates_frequency)
    return 0

def add_coord_to_dictionary(coord, coordinates_frequency):
    if coord in coordinates_frequency:
        coordinates_frequency[coord] += 1
    else:
         coordinates_frequency[coord] = 1

def count_frequencies(coordinates_frequency):
    two_or_more = 0
    for key, value in coordinates_frequency.items():
        if (value >= 2):
            two_or_more += 1
    return two_or_more

def part2(my_input, coordinates_frequency):
    for elem in my_input:
        find_diagonal_coordinates(elem[0], elem[1], coordinates_frequency)
    two_or_more = count_frequencies(coordinates_frequency)
    print(two_or_more)
    return 0

main()