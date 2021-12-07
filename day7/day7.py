def main():
    crab = get_input()
    part1(crab)
    part2(crab)

def get_input():
    f = open("input.txt", "r")
    for line in f:
        crab = [int(elem.strip()) for elem in line.split(",")]
    crab.sort()
    return crab

def part1(crab):
    median = find_median(crab)
    total_fuel = 0
    for elem in crab:
        total_fuel += abs(elem - median)
    print(total_fuel)
    return 0

def part2(crab):
    average = find_average(crab)
    total_fuel = 0
    for elem in crab:
        total_fuel += count_fuel_cost(abs(elem - average))
    print(total_fuel)

def find_median(crab):
    if len(crab) % 2 == 1:
        return crab[round(crab/2)]
    else:
        edge1 = round(len(crab)/2) - 1
        edge2 = round(len(crab)/2)
        return int ((crab[edge1] + crab[edge2]) / 2)

def find_average(crab):
    sum = 0
    for elem in crab:
        sum += elem
    return int((sum/len(crab)))

def count_fuel_cost(distance):
    result = (distance*(distance + 1)) / 2
    return int(result)

main()