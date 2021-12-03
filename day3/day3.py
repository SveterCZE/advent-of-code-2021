def main():
    my_input = get_input()
    part1(my_input)
    part2(my_input)
    return 0

def get_input():
    with open("input.txt", "r") as f:
        lines = f.readlines()
    bits = [line.strip() for line in lines]
    return bits

def part1(my_input):
    zeroes = []
    ones = []
    most_common = []
    least_common = []
    initial_list = list(my_input[0])
    for i in range(len(initial_list)):
        zeroes.append(0)
        ones.append(0)
        most_common.append(0)
        least_common.append(0)

    figures = len(my_input)
    # print(figures)
    for i in range(figures):
        split_figure = list(my_input[i])
        # print(split_figure)
        for j in range(len(split_figure)):
            if split_figure[j] == "0":
                zeroes[j] += 1
            else:
                ones[j] += 1
    
    for i in range(len(zeroes)):
        if (zeroes[i] > ones[i]):
            most_common[i] = "0"
            least_common[i] = "1"
        else:
            most_common[i] = "1"
            least_common[i] = "0"
    
    most_common_binary = "".join(map(str, most_common))
    least_common_binary = "".join(map(str, least_common))

    print(int(most_common_binary, 2) * int(least_common_binary, 2))

    return 0

def part2(my_input):
    lead_zero = 0
    lead_one = 0
    for elem in my_input:
        if elem[0] == "0":
            lead_zero += 1
        else:
            lead_one += 1
    
    if (lead_zero > lead_one):
        most_common = "0"
    else:
        most_common = "1"
    
    oxygen_generation_numbers = []
    co2_numbers = []

    for elem in my_input:
        if elem[0] == most_common:
            oxygen_generation_numbers.append(elem)
        
        else:
            co2_numbers.append(elem)

    oxygen = recursive_helper_oxygen(oxygen_generation_numbers, 1)
    co2 = recursive_helper_co2(co2_numbers, 1)
    print(int(oxygen, 2) * int(co2, 2))
    return 0

def recursive_helper_co2(my_input, level):
    if len(my_input) == 1:
        return my_input[0]
    else:
        lead_zero = 0
        lead_one = 0
        for elem in my_input:
            if elem[level] == "0":
                lead_zero += 1
            else:
                lead_one += 1
        if (lead_zero > lead_one):
            most_common = "0"
        else:
            most_common = "1"
        
        co2_numbers = []
        for elem in my_input:
            if elem[level] == most_common:
                pass
            else:
                co2_numbers.append(elem)
        
        co2 = recursive_helper_co2(co2_numbers, level + 1)
        return co2

def recursive_helper_oxygen(my_input, level):
    if len(my_input) == 1:
        return my_input[0]
    else:
        lead_zero = 0
        lead_one = 0
        for elem in my_input:
            if elem[level] == "0":
                lead_zero += 1
            else:
                lead_one += 1
        if (lead_zero > lead_one):
            most_common = "0"
        else:
            most_common = "1"
        
        oxygen_numbers = []
        for elem in my_input:
            if elem[level] == most_common:
                oxygen_numbers.append(elem)
            else:
                pass
        
        oxygen = recursive_helper_oxygen(oxygen_numbers, level + 1)
        return oxygen


main()