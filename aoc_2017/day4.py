def main():
    print(part_one())
    print(part_two())

def part_one():
    valid_count = 0
    f = open('day4_input.txt', 'r')
    
    for line in f:
        password_dict = {}
        valid = True
        for word in (line.strip().split(' ')):
            if word in password_dict:
                valid = False
                break
            else:   
                password_dict[word] = 1
        if valid:
            valid_count += 1
        
    f.close()
    return valid_count

def part_two():
    valid_count = 0
    f = open('day4_input.txt', 'r')
    
    for line in f:
        password_dict = {}
        valid = True
        for word in (line.strip().split(' ')):
            word_list = list(word)
            word_list.sort()
            word = ''.join(word_list)
            if word in password_dict:
                valid = False
                break
            else:   
                password_dict[word] = 1
        if valid:
            valid_count += 1
        
    f.close()
    return valid_count

if __name__ == '__main__':
    main()
