# http://www.pythonchallenge.com/pc/def/oxygen.html
from urllib.request import urlopen
from PIL import Image

#resp = urlopen('http://www.pythonchallenge.com/pc/def/oxygen.png')
resp = open('oxygen.png', 'rb')

img = Image.open(resp)

w, h = img.size

y = h // 2



for x in range(0, w, 7):
    pixel = img.getpixel((x, y))
    res = chr(pixel[0]) # smart guy, you made it. the next level is [105, 110, 116, 101, 103, 114, 105, 116, 121]pe_
    print(res, end='')

print()

for a in [105, 110, 116, 101, 103, 114, 105, 116, 121]:
    print(chr(a), end='')
