def main():
    fish = get_fish()
    part1(fish)
    part2(fish)

def get_fish():
    with open("input.txt", "r") as f:
        lines = f.readlines()
    fish = [line.strip().split(",") for line in lines]
    return fish[0]

def part1(fish):
    fish_count = [0] * 9
    for i, fish_no in enumerate(fish):
        fish_count[int(fish_no)] += 1
    for i in range(256):
        hatch_fish(fish_count)
        sum_fish = 0
    for elem in fish_count:
        sum_fish += elem
    print(sum_fish)
    return

def hatch_fish(fish_count):
    fish_giving_birth = fish_count[0]
    for i in range(1, len(fish_count)):
        fish_count[i-1] = fish_count[i]
    fish_count[6] += fish_giving_birth
    fish_count[8] = fish_giving_birth

def part2(fish):
    pass

main()