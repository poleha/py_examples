from urllib.request import urlopen
import pickle

resp = urlopen('http://www.pythonchallenge.com/pc/def/banner.p')
result = resp.read()

res = pickle.loads(result)


for a in res:
    for b in a:
        print(b[0] * b[1], end='')
    print('')


