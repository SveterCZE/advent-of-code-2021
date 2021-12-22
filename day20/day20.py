def main():
    decoding_table, image = get_input()
    part1(decoding_table, image, 2)
    decoding_table, image = get_input()
    part1(decoding_table, image, 50)
    return 0

def get_input():
    f = open("input.txt", "r")
    image = []
    for i, j in enumerate(f):
        if i == 0:
            decoding_table = j.strip()
        elif i > 1:
            image.append(list(j.strip()))
    return decoding_table, image

def part1(decoding_table, image, rounds):
    image = add_padding(image, 0, decoding_table)
    for i in range(1,rounds+1):
        image = magnifiy_image(image, decoding_table)
        image = add_padding(image, i, decoding_table)
    number_of_light = count_light(image)
    print(number_of_light)
    return 0

def count_light(checked_image):
    number_of_light = 0
    for i in range(len(checked_image)):
        for j in range(len(checked_image[0])):
            if checked_image[i][j] == "#":
                number_of_light +=1
    return number_of_light

def magnifiy_image(initial_image, decoding_table):
    size_x = len(initial_image) - 2
    size_y = len(initial_image[0]) - 2
    magnified_image = []
    for i in range(size_x):
        temp_line = []
        for j in range(size_y):
            temp_line.append("0")
        magnified_image.append(temp_line)
    for i in range(size_x):
        for j in range(size_y):
                magnified_representation = get_magnified_representation(initial_image, i, j)
                magnified_representation = convert_infinity_back(magnified_representation)
                magnified_representation_decimal = conver_to_decimal(magnified_representation)
                magnified_representation_converted = convert_to_magnified_char(magnified_representation_decimal, decoding_table)
                magnified_image[i][j] = magnified_representation_converted
    return magnified_image


def convert_to_magnified_char(magnified_representation_decimal, decoding_table):
    return decoding_table[magnified_representation_decimal]

def get_magnified_representation(initial_image, i, j):
    maginified_reading = list("000000000")
    for x in range(3):
        for y in range(3):
            if initial_image[x + i][y + j] == "#":
                maginified_reading[(3*x) + y] = "1"
    return "".join(maginified_reading)

def determine_infinity_pixel(magnification_round, decoding_table):
    if magnification_round % 2 == 0:
        return decoding_table[-1]
    else:
        return decoding_table[0]

def convert_infinity_back(magnified_representation):
    representation_split = list(magnified_representation)
    return "".join(representation_split)

def conver_to_decimal(binary_input):
    return int(binary_input, 2)

def add_padding(original_image, magnification_step, decoding_table):
    size_x = len(original_image)
    size_y = len(original_image[0])
    new_image = []
    for i in range(size_x + 4):
        temp_line = []
        for j in range(size_y + 4):
            temp_line.append(determine_infinity_pixel(magnification_step, decoding_table))
        new_image.append(temp_line)
    for i in range(size_x):
        for j in range(size_y):
            new_image[i+2][j+2] = original_image[i][j]
    return new_image

main()