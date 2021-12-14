def main():
    initial_protein, instructions = get_input()
    part1(initial_protein, instructions)
    part2(initial_protein, instructions)
    return 0

def get_input():
    f = open("input.txt", "r")
    initial_protein = ""
    instructions = {}
    for no, line in enumerate(f):
        if no == 0:
            initial_protein += line.strip()
        if no > 1:
            temp_line = line.strip().split(" -> ")
            instructions[temp_line[0]] = temp_line[1]
    return initial_protein, instructions

def part1(initial_protein, instructions):
    protein_as_pairs_of_letters = convert_initial_protein(initial_protein)
    for i in range(10):
        protein_as_pairs_of_letters = run_insertion_process(protein_as_pairs_of_letters, instructions)
    count = count_letters(protein_as_pairs_of_letters, initial_protein)
    lowest, highest = find_low_high(count)
    print(highest - lowest)

def part2(initial_protein, instructions):
    protein_as_pairs_of_letters = convert_initial_protein(initial_protein)
    for i in range(40):
        protein_as_pairs_of_letters = run_insertion_process(protein_as_pairs_of_letters, instructions)
    count = count_letters(protein_as_pairs_of_letters, initial_protein)
    lowest, highest = find_low_high(count)
    print(highest - lowest)

def find_low_high(count):
    low = 9999999999999999999999999
    high = 0
    for key, value in count.items():
        if value > high:
            high = value
        if value < low:
            low = value
    return low, high

def count_letters(protein_as_pairs_of_letters, initial_protein):
    count = {}
    count[initial_protein[0]] = 1
    count[initial_protein[-1]] = 1
    for key, value in protein_as_pairs_of_letters.items():
        # print(key, value)
        if key[0] in count:
            count[key[0]] += value
        else:
            count[key[0]] = value

        if key[1] in count:
            count[key[1]] += value
        else:
            count[key[1]] = value
    for key, value in count.items():
        count[key] = int(value/2)
    return count

def convert_initial_protein(initial_protein):
    protein_pairs = {}
    for i in range(len(initial_protein) - 1):
        temp_pair = initial_protein[i:i+2]
        if temp_pair in protein_pairs:
            protein_pairs[temp_pair] += 1
        else:
            protein_pairs[temp_pair] = 1
    return protein_pairs

def run_insertion_process(protein_as_pairs_of_letters, instructions):
    new_protein_as_pairs_of_letters = {}
    for key, value in protein_as_pairs_of_letters.items():
        inserted_value = instructions[key]
        new_pair_1 = key[0] + inserted_value
        new_pair_2 = inserted_value + key[1]

        if new_pair_1 in new_protein_as_pairs_of_letters:
            new_protein_as_pairs_of_letters[new_pair_1] += value
        else:
            new_protein_as_pairs_of_letters[new_pair_1] = value
        
        if new_pair_2 in new_protein_as_pairs_of_letters:
            new_protein_as_pairs_of_letters[new_pair_2] += value
        else:
            new_protein_as_pairs_of_letters[new_pair_2] = value
    return new_protein_as_pairs_of_letters

main()