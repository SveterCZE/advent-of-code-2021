def main():
    my_input = get_input()
    part1(my_input)
    part2(my_input)
    return 0

def get_input():
    with open("input.txt", "r") as f:
        lines = f.readlines()
    bingo = [line.strip() for line in lines]
    return bingo

def part1(my_input):
    drawn_numbers = list(my_input[0].split(","))
    list_of_grids = []

    for i in range(1, len(my_input)):
        if (len(my_input[i]) == 0):
            list_of_grids.append([])
        else:
            list_of_grids[-1].append((my_input[i].split()))
            
    for drawn_number in drawn_numbers:
        for grid in list_of_grids:
            for i in range(len(grid)):
                for j in range(len(grid)):
                    try:
                        if int(grid[i][j]) == int(drawn_number):
                            grid[i][j] = "X"
                    except:
                        pass
            
        for grid in list_of_grids:
            if victorious_grid(grid) == True:
                board_sum = calculate_board_sum(grid)
                print(board_sum * int(drawn_number))
                return
    return

def victorious_grid(checked_grid):
    # Check vertical
    for line in checked_grid:
        interim_sum = 0
        for i in range(len(line)):
            try:
                interim_sum += int(line[i])
            except:
                pass
        if interim_sum == 0:
            return True

    # Check horizontal
    for i in range(len(checked_grid)):
        interim_sum = 0
        for j in range(len(checked_grid)):
            try:
                interim_sum += int(checked_grid[j][i])
            except:
                pass
        if interim_sum == 0:
            return True
    return False 

def calculate_board_sum(checked_grid):
    interim_sum = 0
    for i in range(len(checked_grid)):
        for j in range(len(checked_grid)):
            try:
                interim_sum += int(checked_grid[j][i])
            except:
                pass
    return interim_sum

def part2(my_input):
    drawn_numbers = list(my_input[0].split(","))
    list_of_grids = []
    list_of_winning_grids = []

    for i in range(1, len(my_input)):
        if (len(my_input[i]) == 0):
            list_of_grids.append([])
        else:
            list_of_grids[-1].append((my_input[i].split())) 
    
    no_of_grids = len(list_of_grids)

    for x in range(len(drawn_numbers)):
        for grid in list_of_grids:
            for i in range(len(grid)):
                for j in range(len(grid)):
                    try:
                        if int(grid[i][j]) == int(drawn_numbers[x]):
                            grid[i][j] = "X"
                    except:
                        pass
        
        for grid in list_of_grids:
            if victorious_grid(grid) == True:
                if grid not in list_of_winning_grids:
                    list_of_winning_grids.append(grid)
        
            if (len(list_of_winning_grids)) == len(list_of_grids) - 1:
                for grid in list_of_grids:
                    if victorious_grid(grid) != True:
                        for i in range(len(grid)):
                            for j in range(len(grid)):
                                try:
                                    if int(grid[i][j]) == int(drawn_numbers[x + 1]):
                                        grid[i][j] = "X"
                                except:
                                    pass
                        board_sum = calculate_board_sum(grid)
                        print(board_sum * int(drawn_numbers[x + 1]))
                return

main()