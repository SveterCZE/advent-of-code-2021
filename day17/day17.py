import re

def main():
    instructions = get_input()
    part1(instructions)
    part2(instructions)
    return 0

def get_input():
    f = open("input.txt", "r")
    for line in f:
        coords = line.replace('..',' ').replace('=',' ').replace(',',' ').split()
        return ((int(coords[3]), int(coords[4])), (int(coords[6]), int(coords[7])))

def part1(instructions):
    x_borders = instructions[0]
    y_borders = instructions[1]
    max_result = 0
    for i in range(350):
        for j in range(350):
            temp_result_bool, result = shoot(i,j, x_borders, y_borders)
            if temp_result_bool == False:
                pass
            elif result > max_result:
                max_result = result
    print(max_result)
    return 0

def shoot(x_velocity, y_velocity, x_borders, y_borders):
    current_x_coord = 0
    current_y_coord = 0
    max_y_coordinate = 0
    while(True):
        current_x_coord += x_velocity
        current_y_coord += y_velocity
        if x_velocity > 0:
            x_velocity -= 1
        y_velocity -= 1
        if max_y_coordinate < current_y_coord:
            max_y_coordinate = current_y_coord
        if is_it_hit(current_x_coord, current_y_coord, x_borders, y_borders) == True:
            return True, max_y_coordinate
        elif is_it_miss(current_x_coord, current_y_coord, x_borders, y_borders, x_velocity) == True:
            return False, max_y_coordinate

def is_it_hit(current_x_coord, current_y_coord, x_borders, y_borders):
    if current_x_coord >= x_borders[0] and current_x_coord <= x_borders[1] and current_y_coord >= y_borders[0] and current_y_coord <= y_borders[1]:
        return True
    else:
        return False

def is_it_miss(current_x_coord, current_y_coord, x_borders, y_borders, x_velocity):
    if current_x_coord > x_borders[1]:
        return True
    elif x_velocity == 0 and current_y_coord < y_borders[0]:
        return True
    else:
        return False

def part2(instructions):
    x_borders = instructions[0]
    y_borders = instructions[1]
    good_result = 0
    for i in range(350):
        for j in range(-350, 350):
            temp_result_bool, result = shoot(i,j, x_borders, y_borders)
            if temp_result_bool == True:
                good_result += 1 
    print(good_result)
    return 0

main()
