def main():
    my_input = get_input()
    part1(my_input)
    part2(my_input)
    return 0

def get_input():
    with open("input.txt", "r") as f:
        lines = f.readlines()
    movements = [line.strip() for line in lines]
    return movements

def part1(my_input):
    depth = 0
    horizontal_pos = 0
    for elem in my_input:
        instruction = elem.split()[0]
        movement = int(elem.split()[1])
        if instruction == "down":
            depth += movement
        elif instruction == "up":
            depth -= movement
        elif instruction == "forward":
            horizontal_pos += movement
    print(depth*horizontal_pos)
    return 0

def part2(my_input):
    depth = 0
    horizontal_pos = 0
    aim = 0
    for elem in my_input:
        instruction = elem.split()[0]
        movement = int(elem.split()[1])
        if instruction == "down":
            aim += movement
        elif instruction == "up":
            aim -= movement
        elif instruction == "forward":
            horizontal_pos += movement
            depth = (aim * movement) + depth
    print(depth * horizontal_pos)
    return 0

main()