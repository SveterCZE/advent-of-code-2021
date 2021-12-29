import itertools

def get_input():
    f = open("input.txt", "r")
    instructions = []
    for i, j in enumerate(f):
        instructions.append((j.strip().split()))
    return instructions

def main():
    instructions = get_input()
    # sample_input = "13579246899999"
    results_database = {}
    correct_numbers = set()
    # print(instructions)
    for i in itertools.product([9,8,7,6,5,4,3,2,1], repeat=14):
        if check_number(i, instructions, results_database) == True:
            correct_numbers.add(int("".join(map(str,i))))
    print("Correct numbers: ", len(correct_numbers))
    print("Correct numbers: ", max(correct_numbers))
    return 0

def check_number(checked_number, instructions, results_database):
    w_register = int(checked_number[0])
    x_register = 0
    y_register = 0
    z_register = 0
    input_counter = 0
    pointer_counter = 0
    correct = check_number_recursive_helper(checked_number, instructions[1:], results_database, w_register, x_register, y_register, z_register, input_counter, pointer_counter)
    return correct

def check_number_recursive_helper(checked_number, instructions, results_database, w_register, x_register, y_register, z_register, input_counter, pointer_counter):
    pointer_counter = 0
    unique_tuple = (checked_number[input_counter:], z_register)
    if unique_tuple in results_database:
        return results_database[unique_tuple]
    else:
        for elem in instructions:
            pointer_counter += 1
            if elem[0] == "inp":
                input_counter += 1
                w_register = int(checked_number[input_counter])
                recursive_call_result = check_number_recursive_helper(checked_number, instructions[pointer_counter:], results_database, w_register, x_register, y_register, z_register, input_counter, pointer_counter)
                results_database[unique_tuple] = recursive_call_result
                return recursive_call_result
            elif elem[0] == "mul":
                w_register, x_register, y_register, z_register = mul_operation(elem, w_register, x_register, y_register, z_register)
            elif elem[0] == "add":
                w_register, x_register, y_register, z_register = add_operation(elem, w_register, x_register, y_register, z_register)
            elif elem[0] == "mod":
                w_register, x_register, y_register, z_register, correct_operation = mod_operation(elem, w_register, x_register, y_register, z_register)
                if correct_operation == False:
                    results_database[unique_tuple] = False
                    return False
            elif elem[0] == "div":
                w_register, x_register, y_register, z_register, correct_operation = div_operation(elem, w_register, x_register, y_register, z_register)
                if correct_operation == False:
                    results_database[unique_tuple] = False
                    return False
            elif elem[0] == "eql":
                w_register, x_register, y_register, z_register = eql_operation(elem, w_register, x_register, y_register, z_register)
        
        if z_register == 0:
            results_database[unique_tuple] = True
            return True
        else:
            results_database[unique_tuple] = False
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
        return int(instruction[1:])
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