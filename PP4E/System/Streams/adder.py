import sys
sum = 0
while True:
    try:
        line = input() #Тут читаем линии построчно. Тоже сработает для открытия файла.
        print(line)
    except EOFError:
        break
    else:
        sum += int(line)
print(sum)
