from typing import NewType


def main():
    energy_levels = get_input()
    part1(energy_levels)
    energy_levels = get_input()
    part2(energy_levels)
    return 0

def get_input():
    f = open("input.txt", "r")
    energy_levels = []
    for line in f:
        energy_levels.append(list(map(int,line.strip())))
    return energy_levels

def part1(energy_levels):
    flash_counter = 0
    for i in range(100):
        flash_counter += run_energy_update(energy_levels)
    print(flash_counter)
    return 0

def part2(energy_levels):
    round_counter = 0
    while(True):
        run_energy_update(energy_levels)
        round_counter += 1
        if all_flashes(energy_levels):
            break
    print(round_counter)
    return 0

def all_flashes(energy_levels):
    for i in range(len(energy_levels)):
        for j in range(len(energy_levels[0])):
            if energy_levels[i][j] != 0:
                return False
    return True

def run_energy_update(energy_levels):
    round_flash_counter = 0
    increase_size_by_one(energy_levels)
    while (are_flashes_happening(energy_levels) == True):
        round_flash_counter += apply_flash(energy_levels)
    return round_flash_counter

def increase_size_by_one(energy_levels):
    for i in range(len(energy_levels)):
        for j in range(len(energy_levels[0])):
            energy_levels[i][j] += 1

def are_flashes_happening(energy_levels):
    for i in range(len(energy_levels)):
        for j in range(len(energy_levels[0])):
            if energy_levels[i][j] > 9:
                return True
    return False

def apply_flash(energy_levels):
    sub_round_flash_counter = 0
    for i in range(len(energy_levels)):
        for j in range(len(energy_levels[0])):
            if energy_levels[i][j] > 9:
                flash(energy_levels, i, j)
                sub_round_flash_counter += 1
    return sub_round_flash_counter

def flash(energy_levels, i, j):
    neighbouring_coordinates = generate_neighbouring_coordinates(i, j)
    # Set flashing coordinate to zero
    energy_levels[i][j] = 0
    
    # Increase neighbouring tiles by one, oness they are zero (i.e. aldready flashed)
    for elem in neighbouring_coordinates:
        if energy_levels[elem[0]][elem[1]] != 0:
            energy_levels[elem[0]][elem[1]] += 1

def generate_neighbouring_coordinates(i, j):
    neighbouring_coordinates = []
    A = (i + 1, j)
    is_valid_coordinate(A, neighbouring_coordinates)
    B = (i - 1, j)
    is_valid_coordinate(B, neighbouring_coordinates)
    C = (i, j + 1)
    is_valid_coordinate(C, neighbouring_coordinates)
    D = (i, j - 1)
    is_valid_coordinate(D, neighbouring_coordinates)
    E = (i + 1, j + 1)
    is_valid_coordinate(E, neighbouring_coordinates)
    F = (i + 1, j - 1)
    is_valid_coordinate(F, neighbouring_coordinates)
    G = (i - 1, j + 1)
    is_valid_coordinate(G, neighbouring_coordinates)
    H = (i - 1, j - 1)
    is_valid_coordinate(H, neighbouring_coordinates)
    
    return neighbouring_coordinates

def is_valid_coordinate(coord, neighbouring_coordinates):
    if coord[0] < 0 or coord[1] < 0:
        return
    elif coord[0] > 9 or coord[1] > 9:
        return
    else:
        neighbouring_coordinates.append(coord)
        return

main()