import itertools
import copy

def get_input():
    f = open("input.txt", "r")
    instructions = {}
    instruction_counter = 0
    for i, j in enumerate(f):
        split_line = (j.strip().split())
        if split_line[0] == "inp":
            temp_instruction = []
            instructions[instruction_counter] = temp_instruction
            instruction_counter+=1
        temp_instruction.append(split_line)
    return instructions

def main():
    instructions = get_input()
    correct_numbers = get_valid_numbers(instructions)
    if len(correct_numbers) > 0:
        print("Maximum serial number:", max(correct_numbers))
        print("Minimum serial number:", min(correct_numbers))
        print("Valid serial numbers:", len(correct_numbers))
    else:
        print("No valid serial numbers found! Stay determined.")

def get_valid_numbers(instructions):
    valid_numbers = set()
    # Set target number for this round
    target_z_register = 0
    # I am looking for number 13
    list_representation = []
    digit_order = 13
    get_valid_numbers_helper(instructions, valid_numbers, digit_order, list_representation, target_z_register)
    return valid_numbers

def get_valid_numbers_helper(instructions, valid_numbers, digit_order, list_representation, target_z_register):
    # Base case --- all numbers have been added
    if digit_order < 1:
        print("level:", digit_order, "".join(map(str, list_representation)))
        pass
    if digit_order < 0:
        valid_numbers.append(int("".join(map(str, list_representation))))
        print("adding number")
    # Recursive_case --- search deeper
    else:
        valid_combinations = get_valid_combinations(instructions, digit_order, target_z_register)
        digit_order -= 1
        for elem in valid_combinations:
            new_list_representation = copy.deepcopy(list_representation)
            new_list_representation.append(elem[0])
            get_valid_numbers_helper(instructions, valid_numbers, digit_order, new_list_representation, elem[1])

def get_valid_combinations(instructions, digit_order, target_z_register):
    valid_combinations = set()
    for w_register in range(1,10):
        for initial_z_register in range(27000):
            if check_number_recursive_helper(instructions[digit_order], w_register, initial_z_register, target_z_register) == True:
                valid_combinations.add((w_register, initial_z_register))
        for initial_z_register in range(target_z_register*26 - 100, target_z_register*26 + 100):
            if check_number_recursive_helper(instructions[digit_order], w_register, initial_z_register, target_z_register) == True:
                valid_combinations.add((w_register, initial_z_register))
        for initial_z_register in range(-target_z_register*26 - 27, - target_z_register*26):
            if check_number_recursive_helper(instructions[digit_order], w_register, initial_z_register, target_z_register) == True:
                valid_combinations.add((w_register, initial_z_register))
    return valid_combinations


# def is_valid_combination(instructions, w_register, initial_z_register, target_z_number):
#     x_register = 0
#     y_register = 0
#     input_counter = 0
#     correct = check_number_recursive_helper(w_register, instructions[1:], w_register, x_register, y_register, initial_z_register, input_counter)

# def check_number(checked_number, instructions, results_database, z_register):
#     w_register = int(checked_number[0])
#     x_register = 0
#     y_register = 0
#     # z_register = 0
#     input_counter = 0
#     pointer_counter = 0
#     correct = check_number_recursive_helper(checked_number, instructions[1:], results_database, w_register, x_register, y_register, z_register, input_counter, pointer_counter)
#     if correct == True:
#         print(checked_number, z_register)
#     return correct

def check_number_recursive_helper(instructions, w_register, z_register, target_z_register):
    pointer_counter = 0
    x_register = 0
    y_register = 0
    # unique_tuple = (checked_number[input_counter:], z_register)
    # if unique_tuple in results_database:
    #     return results_database[unique_tuple]
    # else:
    for elem in instructions:
            pointer_counter += 1
            # if elem[0] == "inp":
            #     input_counter += 1
            #     w_register = int(checked_number[input_counter])
            #     recursive_call_result = check_number_recursive_helper(checked_number, instructions[pointer_counter:], results_database, w_register, x_register, y_register, z_register, input_counter, pointer_counter)
            #     results_database[unique_tuple] = recursive_call_result
            #     return recursive_call_result
            if elem[0] == "mul":
                w_register, x_register, y_register, z_register = mul_operation(elem, w_register, x_register, y_register, z_register)
            elif elem[0] == "add":
                w_register, x_register, y_register, z_register = add_operation(elem, w_register, x_register, y_register, z_register)
            elif elem[0] == "mod":
                w_register, x_register, y_register, z_register, correct_operation = mod_operation(elem, w_register, x_register, y_register, z_register)
                if correct_operation == False:
                    # results_database[unique_tuple] = False
                    return False
            elif elem[0] == "div":
                w_register, x_register, y_register, z_register, correct_operation = div_operation(elem, w_register, x_register, y_register, z_register)
                if correct_operation == False:
                    # results_database[unique_tuple] = False
                    return False
            elif elem[0] == "eql":
                w_register, x_register, y_register, z_register = eql_operation(elem, w_register, x_register, y_register, z_register)
        
    if z_register == target_z_register:
            # results_database[unique_tuple] = True
            return True
    else:
            # results_database[unique_tuple] = False
            return False

def mul_operation(instruction, w_register, x_register, y_register, z_register):
    multiplication_result = get_value(instruction[1], w_register, x_register, y_register, z_register) * get_value(instruction[2], w_register, x_register, y_register, z_register)
    if instruction[1] == "w":
        return multiplication_result, x_register, y_register, z_register
    elif instruction[1] == "x":
        return w_register, multiplication_result, y_register, z_register
    elif instruction[1] == "y":
        return w_register, x_register, multiplication_result, z_register
    elif instruction[1] == "z":
        return w_register, x_register, y_register, multiplication_result

def add_operation(instruction, w_register, x_register, y_register, z_register):
    sum = get_value(instruction[1], w_register, x_register, y_register, z_register) + get_value(instruction[2], w_register, x_register, y_register, z_register)
    if instruction[1] == "w":
        return sum, x_register, y_register, z_register
    elif instruction[1] == "x":
        return w_register, sum, y_register, z_register
    elif instruction[1] == "y":
        return w_register, x_register, sum, z_register
    elif instruction[1] == "z":
        return w_register, x_register, y_register, sum

def eql_operation(instruction, w_register, x_register, y_register, z_register):
    value_1 = get_value(instruction[1], w_register, x_register, y_register, z_register)
    value_2 = get_value(instruction[2], w_register, x_register, y_register, z_register)
    if (value_1 == value_2):
        equality = 1
    else:
        equality = 0
    if instruction[1] == "w":
        return equality, x_register, y_register, z_register
    elif instruction[1] == "x":
        return w_register, equality, y_register, z_register
    elif instruction[1] == "y":
        return w_register, x_register, equality, z_register
    elif instruction[1] == "z":
        return w_register, x_register, y_register, equality

def mod_operation(instruction, w_register, x_register, y_register, z_register):
    value_1 = get_value(instruction[1], w_register, x_register, y_register, z_register)
    value_2 = get_value(instruction[2], w_register, x_register, y_register, z_register)

    # Check correctness
    if value_1 < 0 or value_2 <= 0:
        return w_register, x_register, y_register, z_register, False
    
    modulo_remainder = value_1 % value_2
    if instruction[1] == "w":
        return modulo_remainder, x_register, y_register, z_register, True
    elif instruction[1] == "x":
        return w_register, modulo_remainder, y_register, z_register, True
    elif instruction[1] == "y":
        return w_register, x_register, modulo_remainder, z_register, True
    elif instruction[1] == "z":
        return w_register, x_register, y_register, modulo_remainder, True

def div_operation(instruction, w_register, x_register, y_register, z_register):
    value_1 = get_value(instruction[1], w_register, x_register, y_register, z_register)
    value_2 = get_value(instruction[2], w_register, x_register, y_register, z_register)

    # Check correctness
    if value_2 == 0:
        return False
    
    division_result = int(value_1 / value_2)
    if instruction[1] == "w":
        return division_result, x_register, y_register, z_register, True
    elif instruction[1] == "x":
        return w_register, division_result, y_register, z_register, True
    elif instruction[1] == "y":
        return w_register, x_register, division_result, z_register, True
    elif instruction[1] == "z":
        return w_register, x_register, y_register, division_result, True


def get_value(instruction, w_register, x_register, y_register, z_register):
    if instruction[0] == "-":
        return -int(instruction[1:])
    elif instruction.isnumeric() == True:
        return int(instruction)
    elif instruction == "w":
        return w_register
    elif instruction == "x":
        return x_register
    elif instruction == "y":
        return y_register
    elif instruction == "z":
        return z_register

main()