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

def part2(instructions):
    list_of_cubes = []
    for elem in instructions:
        instruction_cube = reactor_cube(elem[1:])
        if elem[0] == "on":
            list_of_cubes = turn_on_cube(list_of_cubes, instruction_cube, "on")
        elif elem[0] == "off":
            list_of_cubes = turn_on_cube(list_of_cubes, instruction_cube, "off")
    total_size = calculate_total_size(list_of_cubes)
    print(total_size)

def calculate_total_size(list_of_cubes):
    size_sum = 0
    for elem in list_of_cubes:
        size_sum += elem.calculate_volume()
    return size_sum

def turn_on_cube(list_of_cubes, inserted_cube, on_off_instruction):
    intersections = True
    while intersections:
        for i in reversed(range(len(list_of_cubes))):
            cuboid = list_of_cubes[i]
            # Alternative 1 --- Inserted cuboid fully encloses an existing cuboid. Remove the existing cuboid
            if inserted_cube.fully_contains_another_cube(cuboid) == True:
                del list_of_cubes[i]
                break
            # Alternative 2 --- Test if there any actaully any intersections
            if inserted_cube.x_left <= cuboid.x_right and inserted_cube.x_right >= cuboid.x_left and inserted_cube.y_left <= cuboid.y_right and inserted_cube.y_right >= cuboid.y_left and inserted_cube.z_left <= cuboid.z_right and inserted_cube.z_right >= cuboid.z_left:
                pass
            else:
                continue
            # Alternative 3 --- There are actually intersections
            if inserted_cube.x_left in range(cuboid.x_left+1, cuboid.x_right+1):
                list_of_cubes[i] =   reactor_cube(((cuboid.x_left, inserted_cube.x_left-1), (cuboid.y_left, cuboid.y_right), (cuboid.z_left, cuboid.z_right)))
                list_of_cubes.append(reactor_cube(((inserted_cube.x_left, cuboid.x_right),  (cuboid.y_left, cuboid.y_right), (cuboid.z_left, cuboid.z_right))))
                break

            if inserted_cube.x_right in range(cuboid.x_left, cuboid.x_right):
                list_of_cubes[i] =   reactor_cube(((inserted_cube.x_right+1, cuboid.x_right), (cuboid.y_left, cuboid.y_right), (cuboid.z_left, cuboid.z_right)))
                list_of_cubes.append(reactor_cube(((cuboid.x_left, inserted_cube.x_right),  (cuboid.y_left, cuboid.y_right), (cuboid.z_left, cuboid.z_right))))
                break
                
            if inserted_cube.y_left in range(cuboid.y_left+1, cuboid.y_right+1):
                list_of_cubes[i] =   reactor_cube(((cuboid.x_left, cuboid.x_right), (cuboid.y_left, inserted_cube.y_left-1), (cuboid.z_left, cuboid.z_right)))
                list_of_cubes.append(reactor_cube(((cuboid.x_left, cuboid.x_right), (inserted_cube.y_left, cuboid.y_right), (cuboid.z_left, cuboid.z_right))))
                break
            if inserted_cube.y_right in range(cuboid.y_left, cuboid.y_right):
                list_of_cubes[i] =   reactor_cube(((cuboid.x_left, cuboid.x_right), (inserted_cube.y_right+1, cuboid.y_right), (cuboid.z_left, cuboid.z_right)))
                list_of_cubes.append(reactor_cube(((cuboid.x_left, cuboid.x_right), (cuboid.y_left, inserted_cube.y_right), (cuboid.z_left, cuboid.z_right))))
                break
                
            if inserted_cube.z_left in range(cuboid.z_left+1, cuboid.z_right+1):
                list_of_cubes[i] =   reactor_cube(((cuboid.x_left, cuboid.x_right), (cuboid.y_left, cuboid.y_right), (cuboid.z_left, inserted_cube.z_left-1)))
                list_of_cubes.append(reactor_cube(((cuboid.x_left, cuboid.x_right), (cuboid.y_left, cuboid.y_right), (inserted_cube.z_left, cuboid.z_right))))
                break
            if inserted_cube.z_right in range(cuboid.z_left, cuboid.z_right):
                list_of_cubes[i] =   reactor_cube(((cuboid.x_left, cuboid.x_right), (cuboid.y_left, cuboid.y_right), (inserted_cube.z_right+1, cuboid.z_right)))
                list_of_cubes.append(reactor_cube(((cuboid.x_left, cuboid.x_right), (cuboid.y_left, cuboid.y_right), (cuboid.z_left, inserted_cube.z_right))))
                break
        else: intersections = False
    if on_off_instruction == "on": list_of_cubes.append(inserted_cube)
    return list_of_cubes

class reactor_cube():
    def __init__(self, initial_coordinates) -> None:
        self.x_left = initial_coordinates[0][0]
        self.x_right = initial_coordinates[0][1]
        self.y_left = initial_coordinates[1][0]
        self.y_right = initial_coordinates[1][1]
        self.z_left = initial_coordinates[2][0]
        self.z_right = initial_coordinates[2][1]

    def calculate_volume(self):
        x_size = abs(self.x_left - self.x_right) + 1
        y_size = abs(self.y_left - self.y_right) + 1
        z_size = abs(self.z_left - self.z_right) + 1
        return x_size * y_size * z_size

    def fully_contains_another_cube(self, contained_cube):
        if self.x_left <= contained_cube.x_left and self.x_right >= contained_cube.x_right and self.y_left <= contained_cube.y_left and self.y_right >= contained_cube.y_right and self.z_left <= contained_cube.z_left and self.z_right >= contained_cube.z_right:
            return True
        else:
            return False

main()
