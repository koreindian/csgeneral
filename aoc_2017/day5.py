def main():
    inst = parse_input()
    #print(part_one(inst))
    print(part_two([0,3,0,1,-3]))
    print(part_two(inst))

def part_one(instructions):
    memo = {}
    count = 0

    i = 0
    while i >= 0 and i < len(instructions):
        instructions[i] += 1
        i += instructions[i] - 1
        count += 1

    return count

def part_two(instructions):
    memo = {}
    count = 0

    i = 0
    while i >= 0 and i < len(instructions):
        offset = 1
        if instructions[i] >= 3:
            offset = -1

        instructions[i] += offset
        i += instructions[i] - offset
        count += 1

    return count

def parse_input():
    f = open('day5_input.txt', 'r')
    instructions = []

    for line in f:
        instructions.append(int(line.strip()))
    f.close()

    return instructions

if __name__ == '__main__':
    main()
  


