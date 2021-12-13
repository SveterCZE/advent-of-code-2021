def main():
    coordinates, instructions = get_input()
    part1(coordinates, instructions)
    part2(coordinates, instructions)
    return 0

def get_input():
    f = open("input.txt", "r")
    instructions = []
    coordinates = set()
    for line in f:
        if line[0].isnumeric() == True:
            temp_line = line.strip().split(",")
            coordinates.add((int(temp_line[0]), int(temp_line[1])))
        elif line[0].isalpha() == True:
            temp_line = line.strip().split("=")
            instructions.append((temp_line[0][-1], int(temp_line[1])))
    return coordinates, instructions

def part1(coordinates, instructions):
    folded_paper = fold(coordinates, instructions[0])
    print(len(folded_paper))

def fold(coordinates, instruction):
    after_fold = set()
    fold_direction = instruction[0]
    fold_number = instruction[1]
    for elem in coordinates:
        if fold_direction == "x":
            if elem[0] < fold_number:
                after_fold.add(elem)
            else:
                new_x_coordinate = (fold_number * 2) - elem[0]
                new_coordinate = (new_x_coordinate, elem[1])
                after_fold.add(new_coordinate)
        elif fold_direction == "y":
            if elem[1] < fold_number:
                after_fold.add(elem)
            else:
                new_y_coordinate = (fold_number * 2) - elem[1]
                new_coordinate = (elem[0], new_y_coordinate)
                after_fold.add(new_coordinate)
    return after_fold

def display_folded_paper(folded_paper):
    highest_x = 0
    highest_y = 0
    for elem in folded_paper:
        if elem[0] > highest_x:
            highest_x = elem[0]
        if elem[1] > highest_y:
            highest_y = elem[1]
    display_grid = []
    for i in range(highest_y + 1):
        temp_line = []
        for i in range(highest_x + 1):
            temp_line.append(".")
        display_grid.append(temp_line)
    for elem in folded_paper:
        display_grid[elem[1]][elem[0]] = "X"
    print(display_grid)


def part2(coordinates, instructions):
    folded_paper = coordinates
    for i, j in enumerate(instructions):
        folded_paper = fold(folded_paper, instructions[i])
    display_folded_paper(folded_paper)

main()