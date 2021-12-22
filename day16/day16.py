import copy

def main():
    instructions = get_input()
    part1(instructions)
    part2(instructions)
    return 0

def get_input():
    f = open("input.txt", "r")
    initial_input = ""
    for line in f:
        initial_input += line.strip()
    return initial_input

def part1(instructions):
    binary_instructions = convert_to_binary(instructions)
    # print("Initial:", binary_instructions)
    packet_versions_sum = process_binary_input(binary_instructions)

def part2(instructions):
    pass

def process_binary_input(binary_instructions):
    packet_versions_sum = 0
    packet_version, packet_length = process_binary_input_recursive(binary_instructions)
    print(packet_version)

def process_binary_input_recursive(binary_instructions):
    # print("Currently processed instruction: ", binary_instructions)
    packet_version = get_packet_version(binary_instructions)
    # print("Packet version: ", packet_version)
    packet_type = get_packet_type(binary_instructions)
    # print("Pacekt type:", packet_type)
    # Literal value --- Base case, returning packet, 
    if packet_type == 4:
        literal_value = process_literal_value(binary_instructions[6:])
        packet_length = int(6 + ((len(literal_value) / 4) * 5))
        # print(packet_length)
        # print("Literal_value", conver_to_decimal(literal_value))
        return packet_version, packet_length
    # Operator
    else:
        packet_header = binary_instructions[6]
        # print("Packet header:", packet_header)
        if packet_header == "0":
            length_type_ID = binary_instructions[7:22]
            length_in_bits = conver_to_decimal(length_type_ID)
            # print("Length of bits:", length_in_bits)
            remaining_binary_instruction = binary_instructions[22:22+length_in_bits]
            bits_explored = 0
            while (length_in_bits > bits_explored):
                current_packet_version, current_packet_length = process_binary_input_recursive(remaining_binary_instruction)
                packet_version += current_packet_version
                bits_explored += current_packet_length
                remaining_binary_instruction = remaining_binary_instruction[current_packet_length:]
            return packet_version, bits_explored + 22

        # Iterate over certain number of sub-packets
        elif packet_header == "1":
            bits_explored = 18
            length_type_ID = binary_instructions[7:18]
            number_of_sub_packets = conver_to_decimal(length_type_ID)
            # print("Number of remaining:", number_of_sub_packets)
            remaining_binary_instruction = binary_instructions[18:]
            for i in range(number_of_sub_packets):
                current_packet_version, current_packet_length = process_binary_input_recursive(remaining_binary_instruction)
                packet_version += current_packet_version
                bits_explored += current_packet_length
                remaining_binary_instruction = remaining_binary_instruction[current_packet_length:]
                # print(current_packet_version, current_packet_length)
            return packet_version, bits_explored


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