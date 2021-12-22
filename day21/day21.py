def main():
    player1_pos, player2_pos = get_input()
    part1(player1_pos, player2_pos)
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


def part2(player1_pos, player2_pos):
    pass

main()