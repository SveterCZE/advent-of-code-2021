def main():
    scanner_results = get_input()
    part1(scanner_results)
    # part2(instructions)
    return 0

def get_input():
    f = open("input.txt", "r")
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

def roll(v): return (v[0],v[2],-v[1])
def turn(v): return (-v[1],v[0],v[2])
def sequence (v):
    for cycle in range(2):
        for step in range(3):  # Yield RTTT 3 times
            v = roll(v)
            yield(v)           #    Yield R
            for i in range(3): #    Yield TTT
                v = turn(v)
                yield(v)
        v = roll(turn(roll(v)))  # Do RTR

def generate_roll_options():
    roll_options = set()
    roll_options_generator = sequence((1,2,3))
    for i in roll_options_generator:
        roll_options.add(i)
    return roll_options

def part1(scanner_results):
    # Generate potential orientantions
    roll_options = generate_roll_options()
    # Create a set of beacon coordinates
    confirmed_beacons = set()
    # Feed into the set the beacons seen by scanner 0
    beacon_status = create_beacon_status_checker(scanner_results)
    confirmed_beacons = feed_initial_scanners(confirmed_beacons, scanner_results, beacon_status)
    connected_beacons = 0
    while True:
        for key, value in beacon_status.items():
            if value == False:
                connect_new_beacons(confirmed_beacons, roll_options, scanner_results, key, beacon_status)
        if all_beacons_connected(beacon_status) == True:
            print("All beacons are found.")
            break
        currently_connected_beacons = count_connected_beacons(beacon_status)
        if currently_connected_beacons == connected_beacons:
            print("Some beacons cannot be connected.")
            break
        connected_beacons = currently_connected_beacons

    print(len(confirmed_beacons))

def find_first_unconnected(beacon_status):
    for key, value in beacon_status.items():
        if value == False:
            return key

def connect_new_beacons(confirmed_beacons, roll_options, scanner_results, relevant_beacon, beacon_status):
    # Find bacons overlap between scanners 0 and 1
    potential_matches = {}
    for confirmed_coordinate in confirmed_beacons:
        for possible_rotation_master in roll_options:
            scanner2_rotated_coordinates = generate_rotated_coordinates(possible_rotation_master, scanner_results[relevant_beacon])
            for rotated_coordinate in scanner2_rotated_coordinates:
                distance = calculate_coord_distance(confirmed_coordinate, rotated_coordinate)
                if (distance, possible_rotation_master) not in potential_matches:
                    potential_matches[(distance, possible_rotation_master)] = 1
                else:
                    potential_matches[(distance, possible_rotation_master)] += 1
    for key,value in potential_matches.items():
        if value == 12:
            offset = key[0]
            rotation = key[1]
            confirmed_beacons = rotate_and_add_new_bacons(confirmed_beacons, scanner_results[relevant_beacon], offset, rotation)
            beacon_status[relevant_beacon] = True

def count_connected_beacons(beacon_status):
    count = 0
    for key, value in beacon_status.items():
        if value == True:
            count += 1
    return count

def all_beacons_connected(beacon_status):
    for key, value in beacon_status.items():
        if value == False:
            return False
    return True

def feed_initial_scanners(confirmed_beacons, scanner_results, beacon_status):
    for elem in scanner_results[0]:
        confirmed_beacons.add(elem)
    beacon_status[0] = True
    return confirmed_beacons

def create_beacon_status_checker(scanner_results):
    beacon_status = {}
    for key, value in scanner_results.items():
        beacon_status[key] = False
    return beacon_status

def rotate_and_add_new_bacons(confirmed_bacons, scanner_results, offset, rotation):
    for elem in scanner_results:
        rotated_bacon_coordinate = generate_rotated_coordinate(elem, offset, rotation)
        confirmed_bacons.add(rotated_bacon_coordinate)
    return confirmed_bacons

def generate_rotated_coordinate(initial_coordinate, offset, rotation):
    x_value = initial_coordinate[abs(rotation[0]) - 1]
    y_value = initial_coordinate[abs(rotation[1]) - 1]
    z_value = initial_coordinate[abs(rotation[2]) - 1]

    if rotation[0] > 0:
        x_mult = 1
    else:
        x_mult = -1
    
    if rotation[1] > 0:
        y_mult = 1
    else:
        y_mult = -1

    if rotation[2] > 0:
        z_mult = 1
    else:
        z_mult = -1

    coord_x = (x_value * x_mult) + offset[0]
    coord_y = (y_value * y_mult) + offset[1]
    coord_z = (z_value * z_mult) + offset[2]

    return (coord_x, coord_y, coord_z)

def calculate_coord_distance(scanner1_coordinate, rotated_coordinate):
    return(scanner1_coordinate[0] - rotated_coordinate[0], scanner1_coordinate[1] - rotated_coordinate[1], scanner1_coordinate[2] - rotated_coordinate[2])

def generate_rotated_coordinates(rotation_master, scanner_input_coordinates):
    rotated_coordinates = set()
    for input_coordinate in scanner_input_coordinates:
        rotated_coordinate = apply_rotation(rotation_master, input_coordinate)
        rotated_coordinates.add(rotated_coordinate)
    return rotated_coordinates

def apply_rotation(rotation_master, input_coordinate):
    rotated_coordinate = [None, None, None]
    # Determine first rotated coordinate
    if abs(rotation_master[0]) == 1:
        rotated_coordinate[0] = input_coordinate[0]
    elif abs(rotation_master[0]) == 2:
        rotated_coordinate[0] = input_coordinate[1]
    elif abs(rotation_master[0]) == 3:
        rotated_coordinate[0] = input_coordinate[2]

    # Determine second rotated coordinate
    if abs(rotation_master[1]) == 1:
        rotated_coordinate[1] = input_coordinate[0]
    elif abs(rotation_master[1]) == 2:
        rotated_coordinate[1] = input_coordinate[1]
    elif abs(rotation_master[1]) == 3:
        rotated_coordinate[1] = input_coordinate[2]

    # Determine third rotated coordinate
    if abs(rotation_master[2]) == 1:
        rotated_coordinate[2] = input_coordinate[0]
    elif abs(rotation_master[2]) == 2:
        rotated_coordinate[2] = input_coordinate[1]
    elif abs(rotation_master[2]) == 3:
        rotated_coordinate[2] = input_coordinate[2]

    # Determine negative values
    if rotation_master[0] < 0:
        rotated_coordinate[0] *= -1
    if rotation_master[1] < 0:
        rotated_coordinate[1] *= -1
    if rotation_master[2] < 0:
        rotated_coordinate[2] *= -1

    return (rotated_coordinate[0], rotated_coordinate[1], rotated_coordinate[2])

main()