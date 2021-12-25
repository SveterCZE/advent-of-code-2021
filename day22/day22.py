def main():
    instructions = get_input()
    part1(instructions[:20])
    part2(instructions)
    return 0

def get_input():
    f = open("input.txt", "r")
    instructions = []
    for line in f:
        coords = line.replace('..',' ').replace('=',' ').replace(',',' ').split()
        instructions.append((coords[0], (int(coords[2]), int(coords[3])), (int(coords[5]), int(coords[6])), (int(coords[8]), int(coords[9]))))
    return instructions

def part1(instructions):
    print(instructions)
    db_points = set()
    for elem in instructions:
        if elem[0] == "on":
            db_points = turn_on(elem, db_points)
        else:
            db_points = turn_off(elem, db_points)
    print(len(db_points))

def turn_on(current_instruction, db_points):
    for x in range(current_instruction[1][0], current_instruction[1][1] + 1):
        for y in range(current_instruction[2][0], current_instruction[2][1] + 1):
            for z in range(current_instruction[3][0], current_instruction[3][1] + 1):
                coord_tuple = (x, y, z)
                db_points.add(coord_tuple)
    return db_points

def turn_off(current_instruction, db_points):
    for x in range(current_instruction[1][0], current_instruction[1][1] + 1):
        for y in range(current_instruction[2][0], current_instruction[2][1] + 1):
            for z in range(current_instruction[3][0], current_instruction[3][1] + 1):
                coord_tuple = (x, y, z)
                if coord_tuple in db_points:
                    db_points.remove(coord_tuple)
    return db_points

def part2(insturctions):
    pass

main()
