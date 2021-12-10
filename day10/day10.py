def main():
    navigation_instructions = get_input()
    incomplete_lines = part1(navigation_instructions)
    part2(incomplete_lines)
    return 0

def get_input():
    f = open("input.txt", "r")
    navigation_instructions = []
    for line in f:
        navigation_instructions.append(list(line.strip()))
    return navigation_instructions

def part1(navigation_instructions):
    error_score = 0
    incomplete_lines = []
    for elem in navigation_instructions:
        line_error_score = find_error_score(elem)
        if line_error_score == 0:
            incomplete_lines.append(elem)
        error_score += line_error_score
    print(error_score)
    return incomplete_lines

def part2(incomplete_lines):
    completion_scores = []
    for elem in incomplete_lines:
        completion_scores.append(count_completion_score(elem))
    completion_scores.sort()
    print(completion_scores[round(len(completion_scores) / 2)])
    return 0

def count_completion_score(incomplete_line):
    opening_chars = ['(', '[', '{', '<']
    closing_chars = [')', ']', '}', '>']
    navigation_stack = []
    for char in incomplete_line:
        if char in opening_chars:
            navigation_stack.append(char)
        elif char in closing_chars:
            navigation_stack.pop()
    completion_stack = []
    for elem in navigation_stack:
        completion_stack.append(find_completion_char(elem))
    completion_stack.reverse()
    completion_score = count_list_score(completion_stack)
    return completion_score

def count_list_score(completion_stack):
    score = 0
    for elem in completion_stack:
        score *= 5
        score += item_completion_score(elem)
    return score

def item_completion_score(closing_symbol):
    if closing_symbol == ")":
        return 1
    elif closing_symbol == "]":
        return 2
    elif closing_symbol == "}":
        return 3
    elif closing_symbol == ">":
        return 4

def find_error_score(checked_line):
    opening_chars = ['(', '[', '{', '<']
    closing_chars = [')', ']', '}', '>']
    navigation_stack = []
    for char in checked_line:
        if char in opening_chars:
            navigation_stack.append(char)
        elif char in closing_chars:
            removed_char = navigation_stack.pop()
            if bad_char_found(opening_chars, closing_chars, char, removed_char):
                return calculate_error_score(char)

    return 0

def find_completion_char(pair_char):
    if pair_char == "(":
        return ")"
    if pair_char == "[":
        return "]"
    if pair_char == "{":
        return  "}"
    if pair_char == "<":
        return ">"

def bad_char_found(opening_chars, closing_chars, closing_char, opening_char):
    if opening_chars.index(opening_char) == closing_chars.index(closing_char):
        return False
    else:
        return True

def calculate_error_score(bad_char):
    if bad_char == ")":
        return 3
    if bad_char == "]":
        return 57
    if bad_char == "}":
        return 1197
    if bad_char == ">":
        return 25137

main()