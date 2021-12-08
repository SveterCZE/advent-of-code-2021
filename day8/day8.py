def main():
    signals = get_input()
    part1(signals)
    part2(signals)

def get_input():
    f = open("input.txt", "r")
    output_signals = []
    for line in f:
        signals = [(elem.strip()) for elem in line.split("|")]
        output_signals.append(signals[1].split())
    return output_signals

def part1(signals):
    counter = 0
    for elem in signals:
        for item in elem:
            if len(item) == 2 or len(item) == 3 or len(item) == 4 or len(item) == 7:
                counter += 1
    print(counter)
    return 0

def part2(signals):
    pass

main()