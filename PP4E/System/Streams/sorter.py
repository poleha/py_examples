import sys                                  # or sorted(sys.stdin)
lines = sys.stdin.readlines()               # sort stdin input lines,
#lines = list(sys.stdin)
#Ждем бесконечно окончания ввода
lines.sort()                                # send result to stdout
for line in lines: print(line, end='')      # for further processing
