def main():
    my_input = get_input()
    part1(my_input)
    part2(my_input)
    return 0

def get_input():
    with open("input.txt", "r") as f:
        lines = f.readlines()
    numbers = [int(line.strip()) for line in lines]
    return numbers

def part1(my_input):
    higher = 0
    for i in range(len(my_input)):
        if (my_input[i] > my_input[i-1]):
            higher += 1
    print (higher)
    return 0

def part2(my_input):
    higher = 0
    for i in range(len(my_input) - 2):
        if ((my_input[i] + my_input[i+1] + my_input[i+2]) > (my_input[i-1] + my_input[i] + my_input[i+1])):
            higher += 1
    print (higher)
    return 0

main()