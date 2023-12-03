#!/usr/bin/env python3

import bs4, requests, argparse
from pathlib import Path
from getpass import getpass
from re import findall, DOTALL
import json
import pprint
import random
from math import floor
from tqdm import tqdm


#HELPER FUNCTIONS FOR PUZZLES:

def day_1(text):
	total = 0
	for line in text.split('\n'):
		print(line)
		line = ''.join([x for x in line if x.isdigit()])
		if not line: continue
		print(line)
		line = int(f"{line[0]}{line[-1]}")
		print(f"{total =}")
		total += line
	return total

def day_1_final(text):
	total = 0
	word_num = dict([(word, i) for i, word in enumerate("zero one two three four five six seven eight nine".split())])
	for line in text.split('\n'):
		for word, i in word_num.items():
			line = line.replace(word,f"{word[:-1]}{i}{word[1:]}")
		print(line)		
		line = ''.join([x for x in line if x.isdigit()])
		print(line)
		if not line: continue
		line = int(f"{line[0]}{line[-1]}")
		print(line)
		total += line
		print("==========")
	return total

def day_2(text):
        game = dict()
        for round in text.strip().split('\n'):
                print(round)
                number, pulls = round.split(':')
                number = int(number.split()[1])
                game[number] = {'blue':0,'red':0,'green':0}
                for pull in pulls.strip().split(';'):
                       for color in pull.split(', '):
                              color = color.strip()
                              amount, color = color.split()
                              amount = int(amount)
                              if game[number][color.strip()] < amount:
                                     game[number][color.strip()] = amount
        total = 0
        num_dice = {'red':12,'green':13,'blue':14}
        for round in game:
               if all([num_dice[color] >= game[round][color]  for color in num_dice]):
                      total += round
        return total

def day_2_final(text):
        game = dict()
        for round in text.strip().split('\n'):
                print(round)
                number, pulls = round.split(':')
                number = int(number.split()[1])
                game[number] = {'blue':0,'red':0,'green':0}
                for pull in pulls.strip().split(';'):
                       for color in pull.split(', '):
                              color = color.strip()
                              amount, color = color.split()
                              amount = int(amount)
                              if game[number][color.strip()] < amount:
                                     game[number][color.strip()] = amount
        total = 0
        for round in game:
               total += game[round]['red']*game[round]['blue']*game[round]['green']
        return total

def day_3(text):
        total = 0
        symbols = [x for x in set(text) if not x.isdigit() and not x == '.' and not x.isspace()]
        _text = text.replace('.', '\n')
        for c in symbols:
               _text = _text.replace(c,'\n')
        numbers = list(map(int,_text.split()))
        numbers.sort(reverse=True)
        #numbers = list(map(int,findall('\d+',text)))
        char_index = list()
        number_index = {num:list() for num in numbers}
        lines = text.split('\n')
        for x, line in enumerate(lines):
                for y, c in enumerate(line):
                        if c in symbols:
                                char_index.append((x,y))
                for number in numbers:
                       try:
                              start = line.index(str(number))
                              low_x = x-1 if x-1 >=0 else 0
                              low_y = start-1 if start-1 >=0 else 0
                              number_index[number].append(f"{low_x}-{x+1},{low_y}-{start+len(str(number))}")
                              line = line.replace(str(number),'.'*len(str(number)),1)
                       except:
                              pass
        for x,y in char_index:
               to_del = list()
               for num, points in number_index.items():
                      for point in points:
                        x_bounds, y_bounds = point.split(',')
                        low_x, up_x = x_bounds.split('-')
                        low_y, up_y = y_bounds.split('-')
                        low_y = int(low_y)
                        low_x = int(low_x)
                        up_x = int(up_x)
                        up_y = int(up_y)
                        if low_y <= y <= up_y and low_x <= x <= up_x:
                                print(num,points)
                                total += num
                        
        print(symbols)
        print(char_index)
        print(numbers)
        print(number_index)
        return total

def day_3_final(text):
        total = 0
        symbols = [x for x in set(text) if not x.isdigit() and not x == '.' and not x.isspace()]
        _text = text.replace('.', '\n')
        for c in symbols:
               _text = _text.replace(c,'\n')
        symbols = '*'
        numbers = list(map(int,_text.split()))
        numbers.sort(reverse=True)
        #numbers = list(map(int,findall('\d+',text)))
        char_index = list()
        number_index = {num:list() for num in numbers}
        lines = text.split('\n')
        for x, line in enumerate(lines):
                for y, c in enumerate(line):
                        if c in symbols:
                                char_index.append((x,y))
                for number in numbers:
                       try:
                              start = line.index(str(number))
                              low_x = x-1 if x-1 >=0 else 0
                              low_y = start-1 if start-1 >=0 else 0
                              number_index[number].append(f"{low_x}-{x+1},{low_y}-{start+len(str(number))}")
                              line = line.replace(str(number),'.'*len(str(number)),1)
                       except:
                              pass
        for x,y in char_index:
               gear_num = list()
               for num, points in number_index.items():
                      for point in points:
                        x_bounds, y_bounds = point.split(',')
                        low_x, up_x = x_bounds.split('-')
                        low_y, up_y = y_bounds.split('-')
                        low_y = int(low_y)
                        low_x = int(low_x)
                        up_x = int(up_x)
                        up_y = int(up_y)
                        if low_y <= y <= up_y and low_x <= x <= up_x:
                                print(num,points)
                                gear_num.append(num)
               if len(gear_num) == 2:
                        total += gear_num[0] * gear_num[1]
                        print(total)
                        
        return total

def day_4(text):
        print('day 4 is not implemented yet')

def day_4_final(text):
        print('day 4 final is not implemented yet')

def day_5(text):
        print('day 5 is not implemented yet')

def day_5_final(text):
        print('day 5 final is not implemented yet')

def day_6(text):
        print('day 6 is not implemented yet')

def day_6_final(text):
        print('day 6 final is not implemented yet')

def day_7(text):
        print('day 7 is not implemented yet')

def day_7_final(text):
        print('day 7 final is not implemented yet')

def day_8(text):
        print('day 8 is not implemented yet')

def day_8_final(text):
        print('day 8 final is not implemented yet')

def day_9(text):
        print('day 9 is not implemented yet')

def day_9_final(text):
        print('day 9 final is not implemented yet')

def day_10(text):
        print('day 10 is not implemented yet')

def day_10_final(text):
        print('day 10 final is not implemented yet')

def day_11(text):
        print('day 11 is not implemented yet')

def day_11_final(text):
        print('day 11 final is not implemented yet')

def day_12(text):
        print('day 12 is not implemented yet')

def day_12_final(text):
        print('day 12 final is not implemented yet')

def day_13(text):
        print('day 13 is not implemented yet')

def day_13_final(text):
        print('day 13 final is not implemented yet')

def day_14(text):
        print('day 14 is not implemented yet')

def day_14_final(text):
        print('day 14 final is not implemented yet')

def day_15(text):
        print('day 15 is not implemented yet')

def day_15_final(text):
        print('day 15 final is not implemented yet')

def day_16(text):
        print('day 16 is not implemented yet')

def day_16_final(text):
        print('day 16 final is not implemented yet')

def day_17(text):
        print('day 17 is not implemented yet')

def day_17_final(text):
        print('day 17 final is not implemented yet')

def day_18(text):
        print('day 18 is not implemented yet')

def day_18_final(text):
        print('day 18 final is not implemented yet')

def day_19(text):
        print('day 19 is not implemented yet')

def day_19_final(text):
        print('day 19 final is not implemented yet')

def day_20(text):
        print('day 20 is not implemented yet')

def day_20_final(text):
        print('day 20 final is not implemented yet')

def day_21(text):
        print('day 21 is not implemented yet')

def day_21_final(text):
        print('day 21 final is not implemented yet')

def day_22(text):
        print('day 22 is not implemented yet')

def day_22_final(text):
        print('day 22 final is not implemented yet')

def day_23(text):
        print('day 23 is not implemented yet')

def day_23_final(text):
        print('day 23 final is not implemented yet')

def day_24(text):
        print('day 24 is not implemented yet')

def day_24_final(text):
        print('day 24 final is not implemented yet')

def day_25(text):
        print('day 25 is not implemented yet')

def day_25_final(text):
        print('day 25 final is not implemented yet')

# REGISTER ALL METHODS IN A DICTIONARY
day_func = {
    '1':day_1, '1_final':day_1_final,
    '2':day_2, '2_final':day_2_final,
    '3':day_3, '3_final':day_3_final,
    '4':day_4, '4_final':day_4_final,
    '5':day_5, '5_final':day_5_final,
    '6':day_6, '6_final':day_6_final,
    '7':day_7, '7_final':day_7_final,
    '8':day_8, '8_final':day_8_final,
    '9':day_9, '9_final':day_9_final,
    '10':day_10, '10_final':day_10_final,
    '11':day_11, '11_final':day_11_final,
    '12':day_12, '12_final':day_12_final,
    '13':day_13, '13_final':day_13_final,
    '14':day_14, '14_final':day_14_final,
    '15':day_15, '15_final':day_15_final,
    '16':day_16, '16_final':day_16_final,
    '17':day_17, '17_final':day_17_final,
    '18':day_18, '18_final':day_18_final,
    '19':day_19, '19_final':day_19_final,
    '20':day_20, '20_final':day_20_final,
    '21':day_21, '21_final':day_21_final,
    '22':day_22, '22_final':day_22_final,
    '23':day_23, '23_final':day_23_final,
    '24':day_24, '24_final':day_24_final,
    '25':day_25, '25_final':day_25_final,
}

def main(day_num, username=None, password=None, online = False, submit = False, part_one = False, part_two = False):
    if online:
        headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

        login_data = {
            'commit': 'Sign in',
            'utf8': '%E2%9C%93',
            'login': username if online and  username else '',
            'password': password if online and  password else ''
        }
        url = "https://github.com/session"
        s = requests.Session()
        r = s.get(url, headers=headers)
        soup = bs4.BeautifulSoup(r.content, 'html5lib')
        login_data['authenticity_token'] = soup.find('input', attrs={'name': 'authenticity_token'})['value']
        r = s.post(url, data=login_data, headers=headers)

        git = 'https://adventofcode.com/auth/github'
        day = 'https://adventofcode.com/2023/day/{}/input'
        submit_answer_url = 'https://adventofcode.com/2023/day/{}/answer'
        s.get(git)

    puzzle_input = s.get(day.format(day_num)).content.decode().strip('\n') if online else Path(f'day{day_num}.txt').read_text().strip('\n')
    if part_one:
        print(f'day {day_num} part 1:')
        ans = day_func[day_num](puzzle_input)
        print(ans)
        if submit:
            data = {'level':'1','answer':str(ans)}
            resp=s.post(submit_answer_url.format(day_num),data=data)
            results = b'one gold star' in resp.content
            print('success' if results else 'failed')
    if part_two:
        print(f'day {day_num} part 2:')
        ans = day_func[f'{day_num}_final'](puzzle_input)
        print(ans)
        if submit:
            data = {'level':'2','answer':str(ans)}
            resp=s.post(submit_answer_url.format(day_num),data=data)
            results = b'<span class="day-success">one gold star</span> closer to collecting enough star fruit.' in resp.content
            print('success' if results else 'failed')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(__file__)
    parser.add_argument('day', nargs='+', help='sets the day to be ran')
    parser.add_argument('-o','--online', action='store_true', help='this flag causes the script to pull the input from the website. Otherwise, it will use dayX.txt as input.')
    parser.add_argument('-s','--submit',action='store_true',help='this flag will submit the answer generated to advent of code.')
    parser.add_argument('-1','--part_one',action='store_true', help='run the first part of the puzzle')
    parser.add_argument('-2','--part_two',action='store_true', help='run the second part of the puzzle')
    parser.add_argument('-u','--username', help='Github username')
    parser.add_argument('-p','--password', help='github password')
    args = parser.parse_args()
    part_one = True if args.part_one==args.part_two else args.part_one
    part_two = args.part_two
    if args.online:
        username = args.username or input('enter username: ')
        password = args.password or getpass()
    else:
        password = None
        username = None
    for day in args.day:
        main(day, online=args.online, submit=args.submit, username=username, password=password, part_one=part_one, part_two=part_two)
