#************************************************Lesson 1
"""
You are given a non-empty list of integers (X). For this task, you should return a list consisting of only the non-unique elements in this list. To do so you will need to remove all unique elements (elements which are contained in a given list only once). When solving this task, do not change the order of the list. Example: [1, 2, 3, 1, 3] 1 and 3 non-unique elements and result will be [1, 3, 1, 3].
Input: A list of integers.

Output: The list of integers.

"""


#**********************************
checkio=lambda d:[x for x in d if d.count(x)>1]
#**************************************

from collections import Counter
# This requires two traversals of the list: O(n), plus the overhead of the dict
def checkio(data):
    c = Counter(data)
    return [x for x in data if c[x] > 1]
#******************************************
from collections import Counter

def checkio(data):
    count = Counter(data)
    count.subtract(set(data))
    return [x for x in data if x in +count] # +count - remove zero and negative counts
#****************************
def checkio(data):
    #Your code here
    #It's main function. Don't remove this function
    #It's using for auto-testing and must return a result for check.
    L = list(data)
    for ele in data:
        if L.count(ele) == 1:
            L.remove(ele)

    #replace this for solution
    return L
#*****************************************

#***************************************************Lesson 2
"""
A median is a numerical value separating the upper half of a sorted array of numbers from the lower half.
In a list where there are an odd number of entities, the median is the number found in the middle of the array.
If the array contains an even number of entities, then there is no single middle value, instead the median
becomes the average of the two numbers found in the middle. For this mission, you are given a non-empty array
of natural numbers (X). With it, you must separate the upper half of the numbers from the lower half
and find the median.

Input: An array as a list of integers.

Output: The median as a float or an integer.
"""

#**********************************
def checkio(data):

    #replace this for solution
    data.sort()
    #data = sorted(data)
    m = len(data) // 2
    return (data[m] + data[-1-m]) / 2

#************************************
def checkio(data):

    #replace this for solution
    data.sort()
    num = int(len(data))
    if num % 2 == 0:
        return (data[int(num/2-1)] + data[int(num/2)]) / 2
    else:
        return data[int(num/2)]
#***********************
checkio = lambda d: (lambda t, n: t[n] + t[-n-1])(sorted(d), len(d)//2)/2
#******************************
def checkio(data):

    #replace this for solution
    m = sorted(data)[(len(data)-1)//2:(len(data)//2)+1]
    return sum(m) / len(m)

#******************************************* Lesson 3
"""
 Stephan and Sophia forget about security and use simple passwords for everything. Help Nikola develop a password security check module. The password will be considered strong enough if its length is greater than or equal to 10 symbols, it has at least one digit, as well as containing one uppercase letter and one lowercase letter in it. The password contains only ASCII latin letters or digits.

Input: A password as a string (Unicode for python 2.7).

Output: Is the password safe or not as a boolean or any data type that can be converted and processed as a boolean. In the results you will see the converted results.
"""

#******************************************
"""
Функция получает строку.
True если не(
строка < 10,
или вся из цифр,
или вся - символьная,
или вся lower,
или вся upper,
)
То есть если любое условие выполняется, то это нам не подходит
Строка не меньше 10, не вся из цифр, не вся из букв, не вся в нижнем регистре, не вся в верхнем
"""

checkio = lambda s: not(
        len(s) < 10
        or s.isdigit()
        or s.isalpha()
        or s.islower()
        or s.isupper()
    )

#******************************************

import re

DIGIT_RE = re.compile('\d')
UPPER_CASE_RE = re.compile('[A-Z]')
LOWER_CASE_RE = re.compile('[a-z]')

def checkio(data):
    """
    Return True if password strong and False if not

    A password is strong if it contains at least 10 symbols,
    and one digit, one upper case and one lower case letter.
    """
    if len(data) < 10:
        return False

    if not DIGIT_RE.search(data):
        return False

    if not UPPER_CASE_RE.search(data):
        return False

    if not LOWER_CASE_RE.search(data):
        return False

    return True

#******************************************

def checkio(data):
    if len(data) < 10:
        return False
    if data.upper() == data:
        return False
    if data.lower() == data:
        return False
    return any(c.isdigit() for c in data)

#******************************************
#Битовая операция. Не разобрал. На потом.
f=lambda d,x:any(ord(t)&96==x for t in d)
checkio=lambda d:f(d,32)&f(d,64)&f(d,96)&(len(d)>9)

#****************************************
checkio=lambda s:len(s)>9 and all(any(f(c)for c in s)for f in[str.isdigit,str.isupper,str.islower])
#*****************************************
checkio = lambda x: len(x) >= 10 and x.lower() != x and x.upper() != x and any(a.isdigit() for a in x)
#*****************************************

#********************************************** lesson 4
"""
You are given a text, which contains different english letters and punctuation symbols. You should find the most frequent letter in the text. The letter returned must be in lower case.
While checking for the most wanted letter, casing does not matter, so for the purpose of your search, "A" == "a". Make sure you do not count punctuation symbols, digits and whitespaces, only letters.

If you have two or more letters with the same frequency, then return the letter which comes first in the latin alphabet. For example -- "one" contains "o", "n", "e" only once for each, thus we choose "e".

Input: A text for analysis as a string (unicode for py2.7).

Output: The most frequent letter in lower case as a string.

"""
import string

def checkio(text):
    """
    We iterate through latyn alphabet and count each letter in the text.
    Then 'max' selects the most frequent letter.
    For the case when we have several equal letter,
    'max' selects the first from they.
    """
    text = text.lower()
    return max(string.ascii_lowercase, key=text.count)
#*************************************
from collections import Counter

def checkio(text):
    count = Counter([x for x in text.lower() if x.isalpha()])
    m = max(count.values())
    return sorted([x for (x, y) in count.items() if y == m])[0]

#These "asserts" using only for self-checking and not necessary for auto-testing
#**********************************
"""Find the most common ASCII letter in a string."""
import collections
import string

ASCII_LOWER = str.maketrans(string.ascii_uppercase, string.ascii_lowercase)
LOWER_SET = set(string.ascii_lowercase)

def checkio(text):
    """Return the most common letter (a-z) in the given text."""
    # Not using Counter.most_common since we need to sort by code point as well
    # as frequency.
    return next(c for c, _ in
        sorted(collections.Counter(str.translate(text, ASCII_LOWER)).items(),
            key=lambda r: (-r[1], r[0]))
        if c in LOWER_SET)
#*******************************************
import string
from collections import Counter

def checkio(text):
    count = Counter([c.lower() for c in text if c in string.ascii_letters])
    dummy_c, freq = count.most_common(1)[0]
    return min([c for c, f in count.most_common() if f == freq])

#These "asserts" using only for self-checking and not necessary for auto-testing

#********************************************
checkio=lambda t:max('abcdefghijklmnopqrstuvwxyz',key=t.lower().count)
#*********************************************
def checkio(x):
    x = x.lower()
    maximum = max([x.count(i) for i in set(x) if i.isalpha()])
    candidates = [j for j in x if x.count(j) == maximum and j.isalpha()]
    return sorted(candidates)[0]
#******************************************
checkio = lambda text: max(set([x for x in text.lower() if x in 'abcdefghijklmnopqrstuvwxyz']), key=text.lower().count)
#***********************************************
def checkio(text):
    return chr(max(range(97,123), key=lambda x:text.lower().count(chr(x))))
#******************************************
import string
from collections import Counter

def checkio(text):
    # lower-case-ize text, then remove any non-letter characters
    text = [char for char in text.lower()
            if char in string.ascii_lowercase]

    # count occurrences of letters
    # returns a list of tuples [('letter', occurrences), (...)]
    most_common = Counter(text).most_common()

    # sort by number of occurrences (in descending order, hence -x[1]), then
    # sort by letter in ascending order
    most_common.sort(key=lambda x: (-x[1], x[0]))

    # thanks to the sorting, the desired result will be the letter in the first
    # element of the list
    return most_common[0][0]
#*********************************************
def checkio(text):
    s = text.lower()
    return max("abcdefghijklmnopqrstuvwxyz", key=s.count)
#****************************************
def checkio(text):
    text = text.casefold()
    dico =([0]*26)
    for i in range(len(text)):
        if text[i].isalpha():
            dico[ord(text[i])-97]+=1
    maxi = max(dico)
    for i in range(26):
        if dico[i]==maxi:
            return chr(i+97)
#*****************************************
from collections import Counter

def checkio(text):
    counted = Counter(a for a in text.lower() if a.islower()).most_common()
    max_cnt = counted[0][1]
    most = (x for x in counted if x[1] == max_cnt)

    return sorted(most)[0][0]
#**************************

#***********************************Level 4
"""
Tic-Tac-Toe, sometimes also known as Xs and Os, is a game for two players (X and O) who take turns marking the spaces in a 3×3 grid. The player who succeeds in placing three respective marks in a horizontal, vertical, or diagonal rows (NW-SE and NE-SW) wins the game.
But we will not be playing this game. You will be the referee for this games results. You are given a result of a game and you must determine if the game ends in a win or a draw as well as who will be the winner. Make sure to return "X" if the X-player wins and "O" if the O-player wins. If the game is a draw, return "D".
"""
#********************My:
def checkio(game_result):
    game_result = [list(row.lower()) for row in game_result]
    result = {'x': 0, 'o': 0, '.': 0}
    for i in range(3):
        if game_result[i][0] == game_result[i][1] == game_result[i][2]:
            result[game_result[i][0]] += 1
        elif game_result[0][i] == game_result[1][i] == game_result[2][i]:
            result[game_result[0][i]] += 1
    if game_result[0][0] == game_result[1][1] == game_result[2][2] or game_result[0][2] == game_result[1][1] == game_result[2][0]:
        result[game_result[1][1]] += 1
    if result['x'] > result['o']:
        return 'X'
    elif result['x'] < result['o']:
        return 'O'
    else:
        return 'D'

#*********************************
def checkio(res):
    res += list(map(''.join, zip(*res)))
    if "OOO" in res: return "O"
    if "XXX" in res: return "X"
    mid = res[1][1]
    for i in 0, 2:
        if res[0][2-i] == res[2][i] == mid != ".":
            return mid
    return "D"
#************************************
def checkio(res):
    res += list(map(''.join, zip(*res)))
    if "OOO" in res: return "O"
    if "XXX" in res: return "X"
    mid = res[1][1]
    for i in 0, 2:
        if res[0][2-i] == res[2][i] == mid != ".":
            return mid
    return "D"
#************************************
def checkio(game_result):
    all_results = '_'.join(game_result + [''.join(p) for p in zip(*game_result)] + [''.join(game_result[i][i] for i in range(3))] + [''.join(game_result[i][2-i] for i in range(3))])
    return 'X' if 'XXX' in all_results else 'O' if 'OOO' in all_results else 'D'


#************************************
from re import match

def checkio(game):
    # {0}: initial blank, {1}: blanks among O- or X-characters, {2}: group ID
    pat = r'^.{{{0}}}([OX]).{{{1}}}\{2}.{{{1}}}\{2}'

    initblanks = (0, 3, 6), (2,), (0, 1, 2), (0,)
    blanks = ((i, blank) for blank in range(4) for i in initblanks[blank])
    pats = '|'.join(pat.format(i, b, g) for g, (i, b) in enumerate(blanks, 1))

    matched = match(pats, ''.join(game))
    if not matched: return 'D'
    return 'O' if 'O' in matched.groups() else 'X'


def checkio(game_result):

    gs = ""
    let_array = ["X", "O"]
    for item in game_result:
        gs += item

    win1 = gs[2]+gs[5]+gs[8]
    win2 = gs[1]+gs[4]+gs[7]
    win3 = gs[0]+gs[3]+gs[6]
    win4 = gs[0]+gs[1]+gs[2]
    win5 = gs[3]+gs[4]+gs[5]
    win6 = gs[6]+gs[7]+gs[8]
    win7 = gs[0]+gs[4]+gs[8]
    win8 = gs[6]+gs[4]+gs[2]

    win_array = [win1,win2,win3,win4,win5,win6,win7,win8]

    for item in let_array:
        for i in range(0,8):
            if win_array[i] == item+item+item:
                return item


    return "D"
#************************************
# From Daniel Dou with love...

def checkio(board):
    # First we put everything together into a single string
    x = "".join(board)

    # Next we outline the 8 possible winning combinations.
    combos = ["012", "345", "678", "036", "147", "258", "048", "246"]

    # We go through all the winning combos 1 by 1 to see if there are any
    # all Xs or all Os in the combos
    for i in combos:
        if x[int(i[0])] == x[int(i[1])] == x[int(i[2])] and x[int(i[0])] in "XO":
            return x[int(i[0])]
    return "D"
#************************************
def win(arr):
    chars = list(set(arr))
    if len(chars) == 1 and chars[0] != '.':
            return chars[0]
    return '.'

def checkio(game_result):
    game_lines = []

    for i in range(3):
        horizontal_line = game_result[i]
        game_lines.append(horizontal_line)

    for i in range(3):
        vertical_line = [game_result[x][i] for x in range(3)]
        game_lines.append(vertical_line)

    diagnoal_right = [game_result[0][0], game_result[1][1], game_result[2][2]]
    game_lines.append(diagnoal_right)

    diagnoal_left = [game_result[2][0], game_result[1][1], game_result[0][2]]
    game_lines.append(diagnoal_left)

    for line in game_lines:
        w = win(line)
        if w != '.': return w

    return 'D'
#************************************
def checkio(game_result):
    for i in range(3):
        if (game_result[i][0] in ['O', 'X']) and (game_result[i][0] == game_result[i][1] == game_result[i][2]):
            return game_result[i][0]
        if (game_result[0][i] in ['O', 'X']) and (game_result[0][i] == game_result[1][i] == game_result[2][i]):
            return game_result[0][i]
    if (game_result[1][1] in ['O', 'X']) and ((game_result[0][0] == game_result[1][1] == game_result[2][2]) or (game_result[0][2] == game_result[1][1] == game_result[2][0])):
        return game_result[1][1]
    return "D"
#************************************
def checkio(gr):
    st = ''.join(gr)
    for c in 'X','O':
        if any(c*3 in (gr[i], st[i::3]) for i in range(3)): return c
        if c*3 in (st[0::4], st[2:-1:2]): return c
    return "D"
#************************************
def checkio(game_result):
    r = 'D'
    i = 0
    while i<=2 and r == 'D':
        if(game_result[i][0] == game_result[i][1] and game_result[i][0] == game_result[i][2] and game_result[i][0] != '.'):
            r = game_result[i][0]
        if(game_result[0][i] == game_result[1][i] and game_result[0][i] == game_result[2][i] and game_result[0][i] != '.'):
            r = game_result[0][i]
        i= i+1
    if((game_result[1][1] == game_result[0][0] and game_result[1][1] == game_result[2][2] and game_result[1][1] != '.') or (game_result[1][1] == game_result[0][2] and game_result[1][1] == game_result[2][0] and game_result[1][1] != '.')):
        r = game_result[1][1]
    return r
#************************************ Lesson 4
FIRST_TEN = ["one", "two", "three", "four", "five", "six", "seven",
             "eight", "nine"]
SECOND_TEN = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
              "sixteen", "seventeen", "eighteen", "nineteen"]
OTHER_TENS = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy",
              "eighty", "ninety"]
HUNDRED = "hundred"


def checkio(number):

    n = number // 100
    t = [FIRST_TEN[n-1], HUNDRED] if n > 0 else []

    n = (number // 10) % 10
    t += [OTHER_TENS[n-2]] if n > 1 else []

    n = number % (10 if n > 1 else 20)
    t += [(FIRST_TEN+SECOND_TEN)[n-1]] if n > 0 else []

    return ' '.join(t)
#************************************
def checkio(number):
    l=["","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen","twenty"]
    d=dict(enumerate(l))
    d.update({30:"thirty",40:"forty",50:"fifty",60:"sixty",70:"seventy",80:"eighty",90:"ninety"})
    h=number//100
    if h:
        return (d[h]+" hundred "+checkio(number%100)).strip()
    if number in d:
        return d[number]
    return d[number//10*10]+" "+d[number%10]
#************************************
def checkio(number):
    # I wanted to take a special approach approach with this function and make a POC of the less ligne as possible

    # Turning them into dict so that we can use its .get() method and never have some IndexError
    spe = dict(enumerate(('', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen')))
    decades = dict(enumerate(('', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety')))

    # [::-1] so that the key for the unit is always 0
    # [-2:] ignore the hundred if necessary
    return (lambda r: r if r else 'zero')(' '.join(filter(lambda p: p, [(spe.get(d.get(2)), 'hundred'*bool(d.get(2)), decades.get(d.get(1)), spe.get(d.get(0)+10*(10<=int(str(number)[-2:])<20))) for d in (dict(enumerate(map(int, str(number)[::-1]))),)][0])))

    # Note: spe and decades could also have been included in the one line but I prefer it this way. Note2: I'm sure this could be shortened again :p
#************************************
def checkio(n, d=dict(enumerate(" one two three four five six seven eight nine ten eleven twelve".split(" ")))):
    def i(s, j=iter("o en ree ir ve f t ".split(" "))):
        for k in j: s = __import__("re").sub(k + "$", next(j), s)
        return s
    return(d[n//100]+" hundred "*(n>99)+d.get(n%100,n%100<20and i(d[n%10])+"teen"or i(d[n//10%10]).replace("u","")+"ty "+d[n%10])).strip()

#************************************
X='thir four fif six seven eigh nine'.split()
A=' one two three four five six seven eight nine ten eleven twelve'.split(' ')+[s+'teen'for s in X]
B=['twenty']+[s.replace('u','')+'ty'for s in X]
f=lambda n,v=0:v and[A[v],'hundred']+f(n%100)or n<20 and [A[n]]or[B[n//10-2]]+f(n%10)
checkio=lambda n:' '.join(f(n,n//100)).strip()
#************************************
FIRST_TEN = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
SECOND_TEN = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
OTHER_TENS = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
HUNDRED = "hundred"

print 305 // 100

def checkio(number):
    result = []
    if number >= 100:
        result.append(FIRST_TEN[number // 100] + " hundred")
    if (number % 100) // 10 > 1:
        result.append(OTHER_TENS[((number % 100) // 10) - 2])
    if (number % 100) // 10 == 1:
        result.append(SECOND_TEN[number % 10])
    elif (number % 10) > 0:
        result.append(FIRST_TEN[number % 10])

    return ' '.join(result)
#************************************
FIRST_TEN = ["one", "two", "three", "four", "five", "six", "seven",
             "eight", "nine"]
SECOND_TEN = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
              "sixteen", "seventeen", "eighteen", "nineteen"]
OTHER_TENS = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy",
              "eighty", "ninety"]
HUNDRED = "hundred"


def checkio(number):

    #replace this for solution
    return FIRST_TEN[number - 1] if number < 10 else SECOND_TEN[number - 10] if number < 20 else OTHER_TENS[number // 10 - 2] + ("" if 0 == number % 10 else (" " + checkio(number % 10))) if number < 100 else FIRST_TEN[number // 100 - 1] + " hundred" + ("" if 0 == number % 100 else (" " + checkio(number % 100)))
#************************************
FIRST_TEN = ["one", "two", "three", "four", "five", "six", "seven",
             "eight", "nine"]
SECOND_TEN = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
              "sixteen", "seventeen", "eighteen", "nineteen"]
OTHER_TENS = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy",
              "eighty", "ninety"]
HUNDRED = "hundred"


def checkio(number):
    if 1 <= number <= 9:
        return FIRST_TEN[number - 1]
    elif 10 <= number <= 19:
        return SECOND_TEN[number-10]
    elif 20 <= number <= 99:
        m, n = divmod(number, 10)
        if n == 0:
            return OTHER_TENS[m-2]
        else:
            return ' '.join([OTHER_TENS[m-2], checkio(n)])
    elif 100 <= number <= 999:
        y, k = divmod(number, 100)
        if k == 0:
            return ' '.join([FIRST_TEN[y - 1], HUNDRED])
        else:
            return ' '.join([FIRST_TEN[y - 1], HUNDRED, checkio(k)])
#************************************
def checkio(i):
    if i < 20:
        result = 'zero,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen'.split(',')[i]
    elif i < 100:
        result = ',,twenty,thirty,forty,fifty,sixty,seventy,eighty,ninety'.split(',')[i//10]
        if i % 10:
            result += ' ' + checkio(i % 10)
    elif i < 1000:
        result = checkio(i // 100) + ' hundred'
        if i % 100:
            result += ' ' + checkio(i % 100)
    return result
#************************************
UNITS = ["zero", "one", "two", "three", "four", "five", "six", "seven",
             "eight", "nine"]
OVER_TEN = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
              "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy",
              "eighty", "ninety"]

def checkio(number):
    hundreds, remainder = divmod(number, 100)
    tens, units = divmod(remainder, 10)
    # construct the 4 possible parts of the result and filter out the empty ones
    return ' '.join(filter(None,
                           ['{0} hundred'.format(UNITS[hundreds]) if hundreds else '',
                            TENS[tens-2] if tens > 1 else '',
                            OVER_TEN[units] if tens == 1 else '',
                            UNITS[units] if (tens != 1 and units) or not number else '']))
#************************************ 1191
def checkio(number):
    result = ''
    ones_list = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
            'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
    tens_list = ['ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    data_str = str(number)
    if number < 20:
        result = ones_list[number-1]

    subdata = int(data_str[-2:])
    if subdata < 20 and subdata > 0:
        result = ones_list[subdata-1]

    elif number >= 20:
        ones = int(data_str[-1])
        tens = int(data_str[-2])
        if tens != 0:
            result = tens_list[tens-1]
        if ones != 0:
            result += ' ' + ones_list[ones-1]

    if number > 99:
        hundreds = int(data_str[0])
        if hundreds > 1:
            result = ones_list[hundreds-1] + ' ' + 'hundreds' + ' ' + result
        else:
            result = 'one hundred' + ' ' + result
        if result[-1] == ' ':
            result = result[:-1]

    return result
#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************

#************************************