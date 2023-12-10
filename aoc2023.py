#!/usr/bin/env python3
from os import system
import bs4, requests, argparse
from pathlib import Path
from getpass import getpass
from re import findall, DOTALL
import colorama
import json
import pprint
import random
import numpy
from time import sleep
from math import floor
from tqdm import tqdm


# HELPER FUNCTIONS FOR PUZZLES:


def day_1(text):
    total = 0
    for line in text.split("\n"):
        line = "".join([x for x in line if x.isdigit()])
        if not line:
            continue
        line = int(f"{line[0]}{line[-1]}")
        total += line
    return total


def day_1_final(text):
    total = 0
    word_num = dict([(word, i) for i, word in enumerate("zero one two three four five six seven eight nine".split())])
    for line in text.split("\n"):
        for word, i in word_num.items():
            line = line.replace(word, f"{word[:-1]}{i}{word[1:]}")
        line = "".join([x for x in line if x.isdigit()])
        if not line:
            continue
        line = int(f"{line[0]}{line[-1]}")
        total += line
    return total


def day_2(text):
    game = dict()
    for round in text.strip().split("\n"):
        number, pulls = round.split(":")
        number = int(number.split()[1])
        game[number] = {"blue": 0, "red": 0, "green": 0}
        for pull in pulls.strip().split(";"):
            for color in pull.split(", "):
                color = color.strip()
                amount, color = color.split()
                amount = int(amount)
                if game[number][color.strip()] < amount:
                    game[number][color.strip()] = amount
    total = 0
    num_dice = {"red": 12, "green": 13, "blue": 14}
    for round in game:
        if all([num_dice[color] >= game[round][color] for color in num_dice]):
            total += round
    return total


def day_2_final(text):
    game = dict()
    for round in text.strip().split("\n"):
        number, pulls = round.split(":")
        number = int(number.split()[1])
        game[number] = {"blue": 0, "red": 0, "green": 0}
        for pull in pulls.strip().split(";"):
            for color in pull.split(", "):
                color = color.strip()
                amount, color = color.split()
                amount = int(amount)
                if game[number][color.strip()] < amount:
                    game[number][color.strip()] = amount
    total = 0
    for round in game:
        total += game[round]["red"] * game[round]["blue"] * game[round]["green"]
    return total


def day_3(text):
    total = 0
    symbols = [x for x in set(text) if not x.isdigit() and not x == "." and not x.isspace()]
    _text = text.replace(".", "\n")
    for c in symbols:
        _text = _text.replace(c, "\n")
    numbers = list(map(int, _text.split()))
    numbers.sort(reverse=True)
    # numbers = list(map(int,findall('\d+',text)))
    char_index = list()
    number_index = {num: list() for num in numbers}
    lines = text.split("\n")
    for x, line in enumerate(lines):
        for y, c in enumerate(line):
            if c in symbols:
                char_index.append((x, y))
        for number in numbers:
            try:
                start = line.index(str(number))
                low_x = x - 1 if x - 1 >= 0 else 0
                low_y = start - 1 if start - 1 >= 0 else 0
                number_index[number].append(f"{low_x}-{x+1},{low_y}-{start+len(str(number))}")
                line = line.replace(str(number), "." * len(str(number)), 1)
            except:
                pass
    for x, y in char_index:
        to_del = list()
        for num, points in number_index.items():
            for point in points:
                x_bounds, y_bounds = point.split(",")
                low_x, up_x = x_bounds.split("-")
                low_y, up_y = y_bounds.split("-")
                low_y = int(low_y)
                low_x = int(low_x)
                up_x = int(up_x)
                up_y = int(up_y)
                if low_y <= y <= up_y and low_x <= x <= up_x:
                    total += num
    return total


def day_3_final(text):
    total = 0
    symbols = [x for x in set(text) if not x.isdigit() and not x == "." and not x.isspace()]
    _text = text.replace(".", "\n")
    for c in symbols:
        _text = _text.replace(c, "\n")
    symbols = "*"
    numbers = list(map(int, _text.split()))
    numbers.sort(reverse=True)
    # numbers = list(map(int,findall('\d+',text)))
    char_index = list()
    number_index = {num: list() for num in numbers}
    lines = text.split("\n")
    for x, line in enumerate(lines):
        for y, c in enumerate(line):
            if c in symbols:
                char_index.append((x, y))
        for number in numbers:
            try:
                start = line.index(str(number))
                low_x = x - 1 if x - 1 >= 0 else 0
                low_y = start - 1 if start - 1 >= 0 else 0
                number_index[number].append(f"{low_x}-{x+1},{low_y}-{start+len(str(number))}")
                line = line.replace(str(number), "." * len(str(number)), 1)
            except:
                pass
    for x, y in char_index:
        gear_num = list()
        for num, points in number_index.items():
            for point in points:
                x_bounds, y_bounds = point.split(",")
                low_x, up_x = x_bounds.split("-")
                low_y, up_y = y_bounds.split("-")
                low_y = int(low_y)
                low_x = int(low_x)
                up_x = int(up_x)
                up_y = int(up_y)
                if low_y <= y <= up_y and low_x <= x <= up_x:
                    gear_num.append(num)
        if len(gear_num) == 2:
            total += gear_num[0] * gear_num[1]

    return total


def day_4(text):
    total = 0
    for line in text.strip().split("\n"):
        round, nums = line.split(": ")
        winning, scratched = nums.split(" | ")
        winning = winning.split()
        scratched = scratched.split()
        found = sum([num in winning for num in scratched])
        if found:
            total += 2 ** (found - 1)
    return total


def day_4_final(text):
    total = 0
    numcards = [1 for _ in range(len(text.split("\n")))]
    for i, line in enumerate(text.strip().split("\n")):
        round, nums = line.split(": ")
        winning, scratched = nums.split(" | ")
        winning = winning.split()
        scratched = scratched.split()
        found = sum([num in winning for num in scratched])
        for index in range(found):
            numcards[index + 1 + i] += 1 * numcards[i]
    return sum(numcards)


def day_5(text):
    maps = text.split("\n\n")
    seeds = list(map(int, maps[0].split()[1:]))
    for conversion in maps[1:]:
        index_transformed = []
        for line in conversion.split("\n")[1:]:
            transform_start_index, start_index, rng = list(map(int, line.split()))
            for i in range(len(seeds)):
                if start_index <= seeds[i] < start_index + rng and i not in index_transformed:
                    seeds[i] += transform_start_index - start_index
                    index_transformed.append(i)
    index = 99999999999
    min = 9999999999999999999
    for i, num in enumerate(seeds):
        if num < min:
            min = num
            index = i
    return seeds[index]

#TODO: write this properly so it doesn't take several hours to find the answer
def day_5_final(text):
    maps = text.split("\n\n")
    seeds = list(map(int, maps[0].split()[1:]))
    index = 30000000
    break_through = False
    break_while = False
    while True:
        location = index
        for conversion in maps[-1:0:-1]:
            for line in conversion.split('\n')[1:]:
                start, dest, rng = list(map(int, line.split()))
                if start <= location < start + rng:
                    location += dest - start
                    break
        if any([ seeds[i] <= location < seeds[i]+seeds[i+1] for i in range(0,len(seeds),2)]):
            break
        if not index%1000000: print(index)
        index += 1
    return index

    # for conversion in maps[1:]:
    #     _seed = dict()
    #     # print(f"{_seed =}")
    #     keys_hit = list()
    #     partial_key_hit =list()
    #     for line in conversion.split("\n")[1:]:
    #             dest_start_index, start_index, rng = list(map(int, line.split()))
    #             dest_end_index = dest_start_index + rng - 1
    #             end_index = start_index + rng-1
    #             diff = dest_start_index - start_index 
    #             print(f"{start_index = } {end_index =} {dest_start_index =} {dest_end_index =}")
    #             for key, value in seeds.items():
    #                 st_seed, end_seed = key
    #                 st_tr, end_tr = value
    #                 if start_index <= st_tr <= end_tr <= end_index:
    #                     print('mid')
    #                     _seed[key] = (st_tr+diff,end_tr+diff)
    #                     keys_hit.append(key)
    #                 elif start_index <= st_tr <= end_index <= end_tr:#handle this
    #                     print('beginning')
    #                     start_diff = end_index - st_tr
    #                     _seed[(st_seed,start_diff + st_seed)] = (st_tr+diff,end_tr+diff)
    #                     _seed[(start_diff + st_seed+1,end_seed)] = (st_tr+diff,end_tr+diff)
    #                     partial_key_hit.append(key)
    #                 elif st_tr <= start_index <= end_tr <= end_index:#handle this
    #                     print('end')
    #                     end_diff= end_tr - start_index
    #                     _seed[(end_seed-end_diff,end_seed)] = (st_tr+diff,end_tr+diff)
    #                     _seed[(st_seed,end_seed-end_diff-1 )] = (st_tr,end_tr-end_diff)
    #                     partial_key_hit.append(key)
    #                 print(f"\t{_seed = }")
    #     print(f"{_seed = }")
    #     print(f"{keys_hit =}")
    #     for key in filter(lambda x: x not in keys_hit and x not in partial_key_hit,seeds):
    #         _seed[key] = seeds[key]
    #     print(f"{_seed = }")
    #     # for key in partial_key_hit:
    #     #     k_start, k_end = key
    #     #     for seed in seeds:
    #     #         s_start, s_end = seed
    #     #         if k_start < s_end < k_end:
    #     #             diff = s_end-k_start
    #     #             _seed[(s_end+1,k_end)] = (seeds[seed][0],seeds[seed][1])
    #     #         if k_end > s_start > k_start:
    #     #             diff = s_start-k_end
    #     #             _seed[(s_start,k_end-1)] = (seeds[seed][0],seeds[seed][1])
                    
    #             # print(f"{_seed =}")
    #     seeds = dict(_seed)
    #     print(f"{conversion =} | {seeds =} {_seed =}")
    #     # print(seeds)

    # return min(map(lambda x: x[0],seeds))


def day_6(text):
    lines = text.split('\n')
    times = list(map(int,lines[0].split()[1:]))
    distances = list(map(int,lines[1].split()[1:]))
    total = 1
    for i in range(len(times)):
        num_won = 0
        speed = 1
        while True:
            if distances[i] < speed*(times[i]-speed):
                num_won += 1
            elif num_won:
                total = total * num_won
                break
            speed += 1
    return total



def day_6_final(text):
    lines = text.split('\n')
    time = int(''.join(lines[0].split()[1:]))
    distance = int(''.join(lines[1].split()[1:]))
    num_won = 0
    speed = 1
    while True:
        if distance < speed*(time-speed):
            num_won += 1
        elif num_won:
            break
        speed += 1
    return num_won

def rank_card(hand):
    hand = hand.split(' ')[0]
    ranks = {"A": 14, "K": 13, "Q": 12,"J":11, "T": 10, "9":9, "8": 8,"7":7,"6":6,"5":5,"4":4,"3":3,"2":2,"1":1}
    rank = [ranks[c] for c in hand]
    counts = [hand.count(c) for c in hand]
    if 5 in counts:
        return (50,rank)
    if 4 in counts:
        return (40,rank)
    if 3 in counts and 2 in counts:
        return (30,rank)
    if 3 in counts:
        return (20,rank)
    if counts.count(2) == 4:
        return (15,rank)
    if 2 in counts:
        return (10,rank)
    return (0,rank)
    
def rank_card_2(hand):
    hand = hand.split(' ')[0]
    ranks = {"A": 14, "K": 13, "Q": 12, "T": 10, "9":9, "8": 8,"7":7,"6":6,"5":5,"4":4,"3":3,"2":2,"J":0,"1":1}
    rank = [ranks[c] for c in hand]
    counts = [hand.count(c) for c in hand]
    if 5 in counts:
        return (50,rank)
    if 4 in counts:
        if 'J' in hand:
            return (50, rank)
        return (40,rank)
    if 3 in counts and 2 in counts:
        if 'J' in hand:
            return (50, rank)
        return (30,rank)
    if 3 in counts:
        if 'J' in hand:
            return (40, rank)
        return (20,rank)
    if counts.count(2) == 4:
        if 'J' in hand and hand.count('J') != 2:
            return (30,rank)
        if 'J' in hand:
            return (40,rank)
        return (15,rank)
    if 2 in counts:
        if 'J' in hand:
            return (20,rank)
        return (10,rank)
    if 'J' in hand:
        return (10,rank)
    return (0,rank)      

def day_7(text):
    return sum((i*int(hand.split()[1]) for i, hand in enumerate(sorted(text.split('\n'),key=lambda x: rank_card(x), reverse = False), start = 1)))


def day_7_final(text):
    l = [i*int(hand.split()[1]) for i, hand in enumerate(sorted(text.split('\n'),key=lambda x: rank_card(x)), start = 1)]
    return sum([i*int(hand.split()[1]) for i, hand in enumerate(sorted(text.split('\n'),key=lambda x: rank_card_2(x)), start = 1)])


def day_8(text):
    moves, locations = text.split('\n\n')
    num_moves = len(moves)
    location = {loc.split(' = ')[0] : loc.split(' = ')[1].strip('()').split(', ') for loc in locations.split('\n')}
    index = 0
    current = 'AAA'
    while current != 'ZZZ':
        if moves[index%num_moves] == 'L':
            current = location[current][0]
        else:
            current = location[current][1]
        index += 1
    return index


def day_8_final(text):
    moves, locations = text.split('\n\n')
    num_moves = len(moves)
    location = {loc.split(' = ')[0] : loc.split(' = ')[1].strip('()').split(', ') for loc in locations.split('\n')}
    starts = list(filter(lambda x: x[-1] == 'A', location))
    index = 0
    indexs = [0 for _ in starts]
    while any((not x for x in indexs)):
        if moves[index%num_moves] == 'L':
            for i in range(len(starts)):
                if not indexs[i]:
                    starts[i] = location[starts[i]][0]
                    if starts[i].endswith('Z'):
                        indexs[i] = index + 1
        else:
            for i in range(len(starts)):
                if not indexs[i]:
                    starts[i] = location[starts[i]][1]
                    if starts[i].endswith('Z'):
                        indexs[i] = index + 1
        index += 1
    lcm = 1
    for i in indexs:
        lcm = numpy.lcm(lcm,i)
    return lcm
    


def day_9(text):
    total = 0
    def predict_next(readings):
        if not any(readings):
            return 0
        return predict_next([readings[i]-readings[i-1] for i in range(1,len(readings))]) + readings[-1]
    for line in text.split('\n'):
        readings = list(map(int,line.split()))
        total += predict_next(readings)
    return total



def day_9_final(text):
    total = 0
    def predict_next(readings):
        if not any(readings):
            return 0
        return -predict_next([readings[i]-readings[i-1] for i in range(1,len(readings))]) + readings[0]
    for line in text.split('\n'):
        readings = list(map(int,line.split()))
        total += predict_next(readings)
    return total


def day_10(text):
    # appending buffer .'s so I don't have to bound check
    pipes = text.strip().split('\n')
    pipes.append('.'*len(pipes[0]))
    pipes.insert(0,'.'*len(pipes[0]))
    pipes = [f".{line}." for line in pipes]
    print('\n'.join(pipes))
    s=(0,0)
    for i , line in enumerate(pipes):
        if (p := line.find('S')) != -1:
            s = (i,p)
            break
    print(s)
    visited = [s]
    #next is a keyword. I should change this
    next = []
    count = 1
    if pipes[s[0]+1][s[1]] in "F7|":
        next.append((s[0]+1,s[1]))
    if pipes[s[0]-1][s[1]] in "JL|":
        next.append((s[0]-1,s[1]))
    if pipes[s[0]][s[1]+1] in "J7-":
        next.append((s[0],s[1]+1))
    if pipes[s[0]][s[1]-1] in "FL-":
        next.append((s[0],s[1]-1))
    # print(next)
    while 1:
        _next = list()
        for point in next:
            if pipes[point[0]][point[1]] in "|7F" and pipes[point[0]+1][point[1]] in "FJL7|" and (point[0]+1,point[1]) not in visited:
                _next.append((point[0]+1,point[1]))
            if pipes[point[0]][point[1]] in "|JL" and pipes[point[0]-1][point[1]] in "FJL7|" and (point[0]-1,point[1]) not in visited:
                _next.append((point[0]-1,point[1]))
            if pipes[point[0]][point[1]] in "-FL" and pipes[point[0]][point[1]+1] in "FJL7-" and (point[0],point[1]+1) not in visited:
                _next.append((point[0],point[1]+1))
            if pipes[point[0]][point[1]] in "-7J" and pipes[point[0]][point[1]-1] in "FJL7-" and (point[0],point[1]-1) not in visited:
                _next.append((point[0],point[1]-1))
            visited.append(point)
        if any((_next.count(n) > 1 for n in _next)):
            return count + 1
        next = _next
        count += 1
        # print(next)
        # print(f"{visited = }")



def day_10_final(text):
    output = False
    pipes = text.strip().split('\n')
    output and print('\n'.join(pipes))
    y_bound = len(pipes)
    x_bound = len(pipes[0])
    s=(0,0)
    for i , line in enumerate(pipes):
        if (p := line.find('S')) != -1:
            s = (i,p)
            break
    visited = [s]
    #next is a keyword. I should change this
    next = []
    count = 1
    up = down = right = left = 0
    if pipes[s[0]+1][s[1]] in "|JL":
        down = 1
        next.append((s[0]+1,s[1]))
    if pipes[s[0]-1][s[1]] in "F7|":
        up = 1
        next.append((s[0]-1,s[1]))
    if pipes[s[0]][s[1]+1] in "J7-":
        right = 1
        next.append((s[0],s[1]+1))
    if pipes[s[0]][s[1]-1] in "FL-":
        left = 1
        next.append((s[0],s[1]-1))
    if up:
        if right:
            pipes[s[0]] = pipes[s[0]].replace('S','L')
        elif left:
            pipes[s[0]] = pipes[s[0]].replace('S','J')
        else:
            pipes[s[0]] = pipes[s[0]].replace('S','|')
    elif down:
        if right:
            pipes[s[0]] = pipes[s[0]].replace('S','F')
        else:
            pipes[s[0]] = pipes[s[0]].replace('S','7')
    else:
        pipes[s[0]] = pipes[s[0]].replace('S','-')
    while 1:
        _next = list()
        for point in next:
            y,x = point
            if pipes[y][x] in "|7F" and pipes[y+1][x] in "FJL7|" and (y+1,x) not in visited:
                _next.append((y+1,x))
            if pipes[y][x] in "|JL" and pipes[y-1][x] in "FJL7|" and (y-1,x) not in visited:
                _next.append((y-1,x))
            if pipes[y][x] in "-FL" and pipes[y][x+1] in "FJL7-" and (y,x+1) not in visited:
                _next.append((y,x+1))
            if pipes[y][x] in "-7J" and pipes[y][x-1] in "FJL7-" and (y,x-1) not in visited:
                _next.append((y,x-1))
            visited.append(point)
        if any((_next.count(n) > 1 for n in _next)):
            visited.extend(_next)
            count += 1
            break
        next = _next
        count += 1
    inside = False
    count = 0
    transf = {"L":"└","F":"┌","J":"┘","7":"┐","-":"─","|":"|"}
    for i in range(y_bound):
        pipes[i] = list(pipes[i])
        for j in range(x_bound):
            pipes[i][j] = transf.get(pipes[i][j]) if (i,j) in visited else ' '
    output and print('\n'.join([''.join(line) for line in pipes]))
    for i, line in enumerate(pipes):
        inside = False
        wall = 'False'
        for j, c in enumerate(line):
            #this logic is close but all wron....
            if c == "-": continue
            elif c == "|":
                inside = not inside
            elif c == transf["F"]:
                wall = 'top'
            elif c == transf['L']:
                wall = 'bottom'
            elif c == transf['J']:
                if wall == "top":
                    inside = not inside
                wall = ''
            elif c == transf["7"]:
                if wall == 'bottom':
                    inside = not inside
                wall = ''
            else:
                if inside and c == ' ':
                    # print(f"{i},{j}: {c}")
                    pipes[i][j] = f"{colorama.Back.BLUE} {colorama.Back.RESET}"
                    count += 1
                    string = '\n'.join([''.join(line) for line in pipes])
                    output and system('clear')
                    output and print(string)
                    output and sleep(.1)
    return count


def day_11(text):
    print("day 11 is not implemented yet")


def day_11_final(text):
    print("day 11 final is not implemented yet")


def day_12(text):
    print("day 12 is not implemented yet")


def day_12_final(text):
    print("day 12 final is not implemented yet")


def day_13(text):
    print("day 13 is not implemented yet")


def day_13_final(text):
    print("day 13 final is not implemented yet")


def day_14(text):
    print("day 14 is not implemented yet")


def day_14_final(text):
    print("day 14 final is not implemented yet")


def day_15(text):
    print("day 15 is not implemented yet")


def day_15_final(text):
    print("day 15 final is not implemented yet")


def day_16(text):
    print("day 16 is not implemented yet")


def day_16_final(text):
    print("day 16 final is not implemented yet")


def day_17(text):
    print("day 17 is not implemented yet")


def day_17_final(text):
    print("day 17 final is not implemented yet")


def day_18(text):
    print("day 18 is not implemented yet")


def day_18_final(text):
    print("day 18 final is not implemented yet")


def day_19(text):
    print("day 19 is not implemented yet")


def day_19_final(text):
    print("day 19 final is not implemented yet")


def day_20(text):
    print("day 20 is not implemented yet")


def day_20_final(text):
    print("day 20 final is not implemented yet")


def day_21(text):
    print("day 21 is not implemented yet")


def day_21_final(text):
    print("day 21 final is not implemented yet")


def day_22(text):
    print("day 22 is not implemented yet")


def day_22_final(text):
    print("day 22 final is not implemented yet")


def day_23(text):
    print("day 23 is not implemented yet")


def day_23_final(text):
    print("day 23 final is not implemented yet")


def day_24(text):
    print("day 24 is not implemented yet")


def day_24_final(text):
    print("day 24 final is not implemented yet")


def day_25(text):
    print("day 25 is not implemented yet")


def day_25_final(text):
    print("day 25 final is not implemented yet")


# REGISTER ALL METHODS IN A DICTIONARY
day_func = {
    "1": day_1,
    "1_final": day_1_final,
    "2": day_2,
    "2_final": day_2_final,
    "3": day_3,
    "3_final": day_3_final,
    "4": day_4,
    "4_final": day_4_final,
    "5": day_5,
    "5_final": day_5_final,
    "6": day_6,
    "6_final": day_6_final,
    "7": day_7,
    "7_final": day_7_final,
    "8": day_8,
    "8_final": day_8_final,
    "9": day_9,
    "9_final": day_9_final,
    "10": day_10,
    "10_final": day_10_final,
    "11": day_11,
    "11_final": day_11_final,
    "12": day_12,
    "12_final": day_12_final,
    "13": day_13,
    "13_final": day_13_final,
    "14": day_14,
    "14_final": day_14_final,
    "15": day_15,
    "15_final": day_15_final,
    "16": day_16,
    "16_final": day_16_final,
    "17": day_17,
    "17_final": day_17_final,
    "18": day_18,
    "18_final": day_18_final,
    "19": day_19,
    "19_final": day_19_final,
    "20": day_20,
    "20_final": day_20_final,
    "21": day_21,
    "21_final": day_21_final,
    "22": day_22,
    "22_final": day_22_final,
    "23": day_23,
    "23_final": day_23_final,
    "24": day_24,
    "24_final": day_24_final,
    "25": day_25,
    "25_final": day_25_final,
}


def main(day_num, online=False, submit=False, part_one=False, part_two=False):
    if online:
        headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}

        s = requests.Session()
        cookie = {'session': Path('.cookie').read_text().strip()}
        day = "https://adventofcode.com/2023/day/{}/input"
        submit_answer_url = "https://adventofcode.com/2023/day/{}/answer"

    puzzle_input = s.get(day.format(day_num), cookies=cookie).content.decode().strip("\n") if online else Path(f"day{day_num}.txt").read_text().strip("\n")
    if part_one:
        print(f"day {day_num} part 1:")
        ans = day_func[day_num](puzzle_input)
        print(ans)
        if submit:
            data = {"level": "1", "answer": str(ans)}
            resp = s.post(submit_answer_url.format(day_num), data=data, cookies=cookie)
            results = b"one gold star" in resp.content
            print("success" if results else "failed")
    if part_two:
        print(f"day {day_num} part 2:")
        ans = day_func[f"{day_num}_final"](puzzle_input)
        print(ans)
        if submit:
            data = {"level": "2", "answer": str(ans)}
            resp = s.post(submit_answer_url.format(day_num), data=data, cookies=cookie)
            results = b'<span class="day-success">one gold star</span> closer to collecting enough star fruit.' in resp.content
            print("success" if results else "failed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(__file__)
    parser.add_argument("day", nargs="+", help="sets the day to be ran")
    parser.add_argument("-o", "--online", action="store_true", help="this flag causes the script to pull the input from the website. Otherwise, it will use dayX.txt as input.")
    parser.add_argument("-s", "--submit", action="store_true", help="this flag will submit the answer generated to advent of code.")
    parser.add_argument("-1", "--part_one", action="store_true", help="run the first part of the puzzle")
    parser.add_argument("-2", "--part_two", action="store_true", help="run the second part of the puzzle")
    args = parser.parse_args()
    part_one = True if args.part_one == args.part_two else args.part_one
    part_two = args.part_two
    for day in args.day:
        main(day, online=args.online, submit=args.submit, part_one=part_one, part_two=part_two)
