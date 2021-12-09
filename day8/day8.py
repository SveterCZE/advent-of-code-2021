def main():
    wires_setup, signals = get_input()
    part1(signals)
    part2(wires_setup, signals)
    return 0

def get_input():
    f = open("input.txt", "r")
    wires_setup = []
    output_signals = []
    for line in f:
        signals = [(elem.strip()) for elem in line.split("|")]
        wires_setup.append(signals[0].split())
        output_signals.append(signals[1].split())
    return wires_setup, output_signals

def part1(signals):
    counter = 0
    for elem in signals:
        for item in elem:
            if len(item) == 2 or len(item) == 3 or len(item) == 4 or len(item) == 7:
                counter += 1
    print(counter)
    return 0

def part2(wires_setup, signals):
    sum = 0
    for i in range(len(wires_setup)):
        sum += check_current_line(wires_setup[i], signals[i])
    print(sum)
    return 0

def check_current_line(wires_setup, signals):
    letter_dict = sum_letters_in_setup(wires_setup)
    decoding_table = generate_decoding_table(wires_setup, letter_dict)
    converted_sum = convert_to_sum(signals, decoding_table)
    return converted_sum

def sum_letters_in_setup(wires_setup):
    letter_dict = {}
    for elem in wires_setup:
        for letter in elem:
            if letter in letter_dict:
                letter_dict[letter] += 1
            else:
                letter_dict[letter] = 1
    return letter_dict

def generate_decoding_table(wires_setup, letter_dict):
    decoding_table = [0] * 7
    # Initial iteration to find unique frequencies
    temp_chars_to_delete = []
    for key, value in letter_dict.items():
        if value == 6:
            decoding_table[1] = key
            temp_chars_to_delete.append(key)
        elif value == 4:
            decoding_table[4] = key
            temp_chars_to_delete.append(key)
        elif value == 9:
            decoding_table[5] = key
            temp_chars_to_delete.append(key)
    for elem in temp_chars_to_delete:
        letter_dict.pop(elem)
    # Find position "top right"
    for elem in wires_setup:
        if len(elem) == 2:
            if elem[0] == decoding_table[5]:
                decoding_table[2] = elem[1]
                letter_dict.pop(elem[1])
            else:
                decoding_table[2] = elem[0]
                letter_dict.pop(elem[0])
    # Find position "top"
    temp_chars_to_delete = []
    for key, value in letter_dict.items():
        if value == 8:
            decoding_table[0] = key
            temp_chars_to_delete.append(key)
    for elem in temp_chars_to_delete:
        letter_dict.pop(elem)
    # Find position "middle"
    for elem in wires_setup:
        if len(elem) == 4:
            for letter in elem:
                if letter not in decoding_table:
                    decoding_table[3] = letter
                    letter_dict.pop(letter)
    # Find the position bottom
    for key, value in letter_dict.items():
        decoding_table[6] = key
    
    return decoding_table

def convert_to_sum(signals, decoding_table):
    figure_string = ""
    for elem in signals:
        figure_string += str(find_correspodning_number(elem, decoding_table))
    return int(figure_string)

def find_correspodning_number(signal, decoding_table):
    if len(signal) == 2:
        return 1
    elif len(signal) == 3:
        return 7
    elif len(signal) == 4:
        return 4
    elif len(signal) == 7:
        return 8
    elif len(signal) == 6 and decoding_table[3] not in signal:
        return 0
    elif len(signal) == 5 and decoding_table[1] not in signal and decoding_table[5] not in signal: 
        return 2
    elif len(signal) == 5 and decoding_table[1] not in signal and decoding_table[4] not in signal:
        return 3
    elif len(signal) == 5 and decoding_table[2] not in signal and decoding_table[4] not in signal:
        return 5
    elif len(signal) == 6 and decoding_table[2] not in signal:
        return 6
    elif len(signal) == 6 and decoding_table[4] not in signal:
        return 9

main()