def main():
    player1_pos, player2_pos = get_input()
    # part1(player1_pos, player2_pos)
    part2(player1_pos, player2_pos)

def get_input():
    f = open("input.txt", "r")
    for i, j in enumerate(f):
        if i == 0:
            player1_pos = int(list(j.strip())[-1])
        elif i == 1:
            player2_pos = int(list(j.strip())[-1])
    return player1_pos, player2_pos

def part1(player1_pos, player2_pos):
    player1_score = 0
    player2_score = 0
    dice_start_position = 1
    dice_rolled = 0
    while True:
        # Player 1 rolls
        dice_start_position, sum_of_dice_rolls = roll_dice(dice_start_position)
        dice_rolled += 3
        # Player 1 moves
        sum_of_dice_rolls = sum_of_dice_rolls % 10
        player1_pos += sum_of_dice_rolls
        if player1_pos > 10:
            player1_pos = player1_pos % 10
        player1_score += player1_pos
        if player1_score >= 1000:
            break
        
        # Player 2 rolls
        dice_start_position, sum_of_dice_rolls = roll_dice(dice_start_position)
        dice_rolled += 3
        sum_of_dice_rolls = sum_of_dice_rolls % 10
        player2_pos += sum_of_dice_rolls
        if player2_pos > 10:
            player2_pos = player2_pos % 10
        player2_score += player2_pos
        if player2_score >= 1000:
            break
    print(min(player1_score, player2_score) * dice_rolled)
    return 0


def roll_dice(dice_start_position):
    rolled_values_sum = 0
    for i in range(3):
        rolled_value = dice_start_position
        rolled_values_sum += rolled_value
        dice_start_position += 1
        if dice_start_position > 100:
            dice_start_position = 1
    return dice_start_position, rolled_values_sum

def determine_results_frequency():
    results_frequency = {}
    for i in range(1, 4):
        for j in range(1,4):
            for k in range(1,4):
                movement = i+j+k
                if movement in results_frequency:
                    results_frequency[movement] += 1
                else:
                    results_frequency[movement] = 1
    return(results_frequency)

def part2(player1_pos, player2_pos):
    results_frequency = determine_results_frequency()
    player1_score = 0
    player2_score = 0
    player1_tuple = (player1_pos, player1_score)
    player2_tuple = (player2_pos, player2_score)
    initial_state = (player1_tuple, player2_tuple)
    current_state = {}
    current_state[initial_state] = 1
    winning_unverses = [0,0]
    while True:
        current_state, winning_unverses = part2_player1_turn(current_state, winning_unverses, results_frequency)
        if len(current_state) == 0:
            break
        current_state, winning_unverses = part2_player2_turn(current_state, winning_unverses, results_frequency)
        if len(current_state) == 0:
            break
    print(max(winning_unverses[0], winning_unverses[1]))
    return 0

def part2_player1_turn(database_of_states, winning_unverses, results_frequency):
        updated_states = {}
        # Player 1 turn
        for key, initial_space_count in database_of_states.items():
            player1_pos = key[0][0]
            player1_score = key[0][1]
            player2_tuple = key[1]
            for steps_taken, steps_frequency in results_frequency.items():
                new_player1_position = player1_pos + steps_taken
                if new_player1_position > 10:
                    new_player1_position = new_player1_position % 10
                new_player1_score = new_player1_position + player1_score
                if new_player1_score >= 21:
                    winning_unverses[0] += initial_space_count * steps_frequency
                else:
                    player1_tuple = (new_player1_position, new_player1_score)
                    if (player1_tuple, player2_tuple) in updated_states:
                        updated_states[(player1_tuple, player2_tuple)] += initial_space_count * steps_frequency
                    else:
                        updated_states[(player1_tuple, player2_tuple)] = initial_space_count * steps_frequency
        
        return updated_states, winning_unverses

def part2_player2_turn(database_of_states, winning_unverses, results_frequency):
        updated_states = {}
        for key, initial_space_count in database_of_states.items():
            player2_pos = key[1][0]
            player2_score = key[1][1]
            player1_tuple = key[0]
            for steps_taken, steps_frequency in results_frequency.items():
                new_player2_position = player2_pos + steps_taken
                if new_player2_position > 10:
                    new_player2_position = new_player2_position % 10
                new_player2_score = new_player2_position + player2_score
                if new_player2_score >= 21:
                    winning_unverses[1] += initial_space_count * steps_frequency
                else:
                    player2_tuple = (new_player2_position, new_player2_score)
                    if (player1_tuple, player2_tuple) in updated_states:
                        updated_states[(player1_tuple, player2_tuple)] += initial_space_count * steps_frequency
                    else:
                        updated_states[(player1_tuple, player2_tuple)] = initial_space_count * steps_frequency
        
        return updated_states, winning_unverses

main()
