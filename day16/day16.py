def main():
    instructions = get_input()
    part1(instructions)
    return 0

def get_input():
    f = open("input.txt", "r")
    initial_input = ""
    for line in f:
        initial_input += line.strip()
    return initial_input

def part1(instructions):
    binary_instructions = convert_to_binary(instructions)
    packet_version, literal_value = process_binary_input(binary_instructions)
    print("Part 1: ", packet_version)
    print("Part 2: ", literal_value)

def process_binary_input(binary_instructions):
    packet_version, packet_length, literal_value = process_binary_input_recursive(binary_instructions)
    return packet_version, literal_value

def process_binary_input_recursive(binary_instructions):
    packet_version = get_packet_version(binary_instructions)
    packet_type = get_packet_type(binary_instructions)
    # Literal value --- Base case, returning packet, 
    if packet_type == 4:
        literal_value = process_literal_value(binary_instructions[6:])
        packet_length = int(6 + ((len(literal_value) / 4) * 5))
        return packet_version, packet_length, conver_to_decimal(literal_value)
    else:
        values_of_embedded_packets = []
    # Operator
        packet_header = binary_instructions[6]
        if packet_header == "0":
            length_type_ID = binary_instructions[7:22]
            length_in_bits = conver_to_decimal(length_type_ID)
            remaining_binary_instruction = binary_instructions[22:22+length_in_bits]
            bits_explored = 0
            while (length_in_bits > bits_explored):
                current_packet_version, current_packet_length, literal_value = process_binary_input_recursive(remaining_binary_instruction)
                packet_version += current_packet_version
                bits_explored += current_packet_length
                remaining_binary_instruction = remaining_binary_instruction[current_packet_length:]
                values_of_embedded_packets.append(literal_value)
            applied_values = apply_operator(values_of_embedded_packets, packet_type)
            return packet_version, bits_explored + 22, applied_values

        # Iterate over certain number of sub-packets
        elif packet_header == "1":
            bits_explored = 18
            length_type_ID = binary_instructions[7:18]
            number_of_sub_packets = conver_to_decimal(length_type_ID)
            remaining_binary_instruction = binary_instructions[18:]
            for i in range(number_of_sub_packets):
                current_packet_version, current_packet_length, literal_value = process_binary_input_recursive(remaining_binary_instruction)
                packet_version += current_packet_version
                bits_explored += current_packet_length
                remaining_binary_instruction = remaining_binary_instruction[current_packet_length:]
                values_of_embedded_packets.append(literal_value)
            applied_values = apply_operator(values_of_embedded_packets, packet_type)
            return packet_version, bits_explored, applied_values


def apply_operator(values_of_embedded_packets, packet_type):
    if packet_type == 0:
        temp_sum = 0
        for elem in values_of_embedded_packets:
            temp_sum += elem
        return temp_sum
    elif packet_type == 1:
        temp_product = values_of_embedded_packets[0]
        for elem in values_of_embedded_packets[1:]:
            temp_product *= elem
        return temp_product
    elif packet_type == 2:
        temp_min = values_of_embedded_packets[0]
        for elem in values_of_embedded_packets[1:]:
            if elem < temp_min:
                temp_min = elem
        return temp_min
    elif packet_type == 3:
        temp_max = values_of_embedded_packets[0]
        for elem in values_of_embedded_packets[1:]:
            if elem > temp_max:
                temp_max = elem
        return temp_max
    elif packet_type == 5:
        if values_of_embedded_packets[0] > values_of_embedded_packets[1]:
            return 1
        else:
            return 0
    elif packet_type == 6:
        if values_of_embedded_packets[0] < values_of_embedded_packets[1]:
            return 1
        else:
            return 0
    elif packet_type == 7:
        if values_of_embedded_packets[0] == values_of_embedded_packets[1]:
            return 1
        else:
            return 0



def process_literal_value(literal_value_binary):
    extracted_binary_value = "" + recursive_process_literal_value(literal_value_binary)
    return extracted_binary_value

def recursive_process_literal_value(literal_value_binary):
    if literal_value_binary[0] == "0":
        return literal_value_binary[1:5]
    else:
        return literal_value_binary[1:5] + recursive_process_literal_value(literal_value_binary[5:])

def convert_to_binary(instructions):
    return bin(int('1' + instructions, 16))[3:]

def get_packet_type(binary_instructions):
    binary_packet_type = binary_instructions[3:6]
    binary_packet_version_decimal = conver_to_decimal(binary_packet_type)
    return binary_packet_version_decimal

def get_packet_version(binary_instructions):
    binary_packet_version = binary_instructions[0:3]
    binary_packet_version_decimal = conver_to_decimal(binary_packet_version)
    return binary_packet_version_decimal

def conver_to_decimal(binary_input):
    return int(binary_input, 2)

main()