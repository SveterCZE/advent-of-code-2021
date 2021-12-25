def main():
    instructions = get_input()
    part1(instructions)
    return 0

def get_input():
    f = open("input.txt", "r")
    instructions = []
    for line in f:
        temp_line = list(line.strip())
        instructions.append(temp_line)
    return instructions

def part1(instructions):
    round_number = 0
    while(True):
        instructions, movement_number = move_one_round(instructions)
        round_number += 1
        if movement_number == 0:
            break
    print(round_number)
    return

def move_one_round(instructions):
    updated_grid = create_empty_grid(instructions)
    movement_count = 0
    # Move horizontally
    for i in range(len(instructions)):
        for j in range(len(instructions[0])):
            if instructions[i][j] == ">":
                next_horizontal_position = get_next_horizontal_position(i,j, instructions)
                if is_next_horizontal_position_available(next_horizontal_position, instructions) == True:
                    place_to_empty_grid_hor(next_horizontal_position, updated_grid)
                    movement_count += 1
                else:
                    place_to_empty_grid_hor((i,j), updated_grid)

    # Merge crowds of vertically moving herds into the grid
    for i in range(len(instructions)):
        for j in range(len(instructions[0])):
            if instructions[i][j] == "v":
                updated_grid[i][j] = "v"

    instructions = updated_grid
    updated_grid = create_empty_grid(instructions)

    # Move vertically
    for i in range(len(instructions)):
        for j in range(len(instructions[0])):
            if instructions[i][j] == "v":
                next_vertical_position = get_next_vertical_position(i,j,instructions)
                if is_next_vertical_position_available(next_vertical_position, instructions) == True:
                    place_to_empty_grid_ver(next_vertical_position, updated_grid)
                    movement_count +=1
                else:
                    place_to_empty_grid_ver((i,j), updated_grid)

    # Merge the horizontally moving herds into the grid
    for i in range(len(instructions)):
        for j in range(len(instructions[0])):
            if instructions[i][j] == ">":
                updated_grid[i][j] = ">"

    return updated_grid,movement_count

def place_to_empty_grid_hor(coordinates, updated_grid):
    updated_grid[coordinates[0]][coordinates[1]] = ">"

def place_to_empty_grid_ver(coordinates, updated_grid):
    updated_grid[coordinates[0]][coordinates[1]] = "v"

def get_next_horizontal_position(i,j, instructions):
    new_j = j + 1
    if new_j >= len(instructions[0]):
        new_j = 0
    return (i, new_j)

def get_next_vertical_position(i,j,instructions):
    new_i = i + 1
    if new_i >= len(instructions):
        new_i = 0
    return(new_i, j)

def is_next_horizontal_position_available(next_horizontal_position, instructions):
    if instructions[next_horizontal_position[0]][next_horizontal_position[1]] == ".":
        return True
    else:
        return False

def is_next_vertical_position_available(next_vertical_position, instructions):
    if instructions[next_vertical_position[0]][next_vertical_position[1]] == ".":
        return True
    else:
        return False

def move_horizontally(current_position, next_horizontal_position, instructions):
    instructions[current_position[0]][current_position[1]] = "."
    instructions[next_horizontal_position[0]][next_horizontal_position[1]] = ">"

def move_vertically(current_position, next_vertical_position, instructions):
    instructions[current_position[0]][current_position[1]] = "."
    instructions[next_vertical_position[0]][next_vertical_position[1]] = "v"

def create_empty_grid(instructions):
    empty_grid = []
    for i in range(len(instructions)):
        temp_row = []
        for j in range(len(instructions[0])):
            temp_row.append(".")
        empty_grid.append(temp_row)
    return empty_grid

main()
