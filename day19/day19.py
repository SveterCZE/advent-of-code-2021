def main():
    scanner_results = get_input()
    part1(scanner_results)
    # part2(instructions)
    return 0

def get_input():
    f = open("sample2.txt", "r")
    scanner_results = {}
    counter = 0
    for line in f:
        temp_line = list(line.strip().split(","))
        if len(temp_line) != 3 and len(temp_line[0]) != 0:
            scanner_results[counter] = []
        elif len(temp_line[0]) == 0:
            counter += 1
        elif len(temp_line) == 3:
            temp_list = (int(temp_line[0]), int(temp_line[1]), int(temp_line[2]))
            scanner_results[counter].append(temp_list)
    return scanner_results

def part1(scanner_results):
    scanner_positions = {}
    scanner_positions[0] = (0,0,0)
    
    # Find scanners overlapping with the initial scanner
    first_scanner_results = scanner_results[0]
    second_scanner_results = scanner_results[1]
    potential_overlaps = {}
    for scanner1_coordinate in first_scanner_results:
        # scanner1_coordinate_combinations = create_possible_combinations(scanner1_coordinate)
        # for possible_scanner1_coord in scanner1_coordinate_combinations:
            for scanner2_coordinate in second_scanner_results:
                scanner2_coordinate_combinations = create_possible_combinations(scanner2_coordinate)
                for possible_scanner2_coord in scanner2_coordinate_combinations:
                    potential_overlaps = try_potential_combination(scanner1_coordinate, possible_scanner2_coord, potential_overlaps)
    for key,value in potential_overlaps.items():
        if value == 12:
            scanner_positions[1] = key
    print(scanner_positions)

    # Find scanners overlapping with the second scanner
    first_scanner_results = scanner_results[1]
    second_scanner_results = scanner_results[4]
    potential_overlaps = {}
    for scanner1_coordinate in first_scanner_results:
        # modified_scanner1_coordinate = modify_coordinate(scanner1_coordinate, scanner_positions[1]) 
        # scanner1_coordinate_combinations = create_possible_combinations(scanner1_coordinate)
        # for possible_scanner1_coord in scanner1_coordinate_combinations:
        for scanner2_coordinate in second_scanner_results:
                scanner2_coordinate_combinations = create_possible_combinations(scanner2_coordinate)
                for possible_scanner2_coord in scanner2_coordinate_combinations:
                    potential_overlaps = try_potential_combination(scanner1_coordinate, possible_scanner2_coord, potential_overlaps)
    for key,value in potential_overlaps.items():
        if value == 12:
            modified_key = modify_coordinate(key, scanner_positions[1])
            scanner_positions[4] = modified_key
    print(scanner_positions)

def modify_coordinate(scanner1_coordinate, offset):
    print(offset)
    print(scanner1_coordinate)
    return (offset[0] - scanner1_coordinate[0], offset[1] - scanner1_coordinate[1], offset[2] - scanner1_coordinate[2])

def create_possible_combinations(scanner_combinations):
    possible_combinations = []
    figure_x = scanner_combinations[0]
    figure_y = scanner_combinations[1]
    figure_z = scanner_combinations[2]

    possible_combinations.append((figure_x, figure_y, figure_z))
    possible_combinations.append((figure_z, figure_x, figure_y))    
    possible_combinations.append((figure_y, figure_z, figure_x))
    possible_combinations.append((figure_y, figure_x, -figure_z))
    possible_combinations.append((figure_x, figure_z, -figure_y))
    possible_combinations.append((figure_z, figure_y, -figure_x))

    # possible_combinations_with_signs = get_combinations_with_signs(possible_combinations)
    # print(len(possible_combinations_with_signs))
    return possible_combinations


def get_combinations_with_signs(possible_combinations):
    possible_combinations_with_signs = set()
    for elem in possible_combinations:
        figure_x = elem[0]
        figure_y = elem[1]
        figure_z = elem[2]
        possible_combinations_with_signs.add((figure_x, figure_y, figure_z))
        possible_combinations_with_signs.add((-figure_x, -figure_y, figure_z))
        possible_combinations_with_signs.add((-figure_x, figure_y, -figure_z))
        possible_combinations_with_signs.add((figure_x, -figure_y, -figure_z))
    return possible_combinations_with_signs

def try_potential_combination(scanner1_coordinate, scanner2_coordinate, potential_overlaps):
    list_of_alternatives = []
    list_of_alternatives.append((scanner1_coordinate[0] + scanner2_coordinate[0], scanner1_coordinate[1] + scanner2_coordinate[1], scanner1_coordinate[2] + scanner2_coordinate[2]))
    list_of_alternatives.append((scanner1_coordinate[0] + scanner2_coordinate[0], scanner1_coordinate[1] + scanner2_coordinate[1], scanner1_coordinate[2] - scanner2_coordinate[2]))
    list_of_alternatives.append((scanner1_coordinate[0] + scanner2_coordinate[0], scanner1_coordinate[1] - scanner2_coordinate[1], scanner1_coordinate[2] - scanner2_coordinate[2]))
    list_of_alternatives.append((scanner1_coordinate[0] + scanner2_coordinate[0], scanner1_coordinate[1] - scanner2_coordinate[1], scanner1_coordinate[2] + scanner2_coordinate[2]))
    list_of_alternatives.append((scanner1_coordinate[0] - scanner2_coordinate[0], scanner1_coordinate[1] - scanner2_coordinate[1], scanner1_coordinate[2] - scanner2_coordinate[2]))
    list_of_alternatives.append((scanner1_coordinate[0] - scanner2_coordinate[0], scanner1_coordinate[1] - scanner2_coordinate[1], scanner1_coordinate[2] + scanner2_coordinate[2]))
    list_of_alternatives.append((scanner1_coordinate[0] - scanner2_coordinate[0], scanner1_coordinate[1] + scanner2_coordinate[1], scanner1_coordinate[2] + scanner2_coordinate[2]))
    list_of_alternatives.append((scanner1_coordinate[0] - scanner2_coordinate[0], scanner1_coordinate[1] + scanner2_coordinate[1], scanner1_coordinate[2] - scanner2_coordinate[2]))

    for elem in list_of_alternatives:
        if elem not in potential_overlaps:
            potential_overlaps[elem] = 1
        else:
            potential_overlaps[elem] += 1
    return potential_overlaps

main()