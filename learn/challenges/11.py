# http://garethrees.org/2007/05/07/python-challenge/
from PIL import Image, ImageDraw
from urllib.request import urlopen

#resp = urlopen('http://www.pythonchallenge.com/pc/return/cave.jpg')

f = open('cave.jpg', 'rb')

print(f.read())

img = Image.open(f)
draw = ImageDraw.Draw(img)

w, h = img.size

for x in range(5):
    for y in range(5):
        print(x + y, img.getpixel((x, y)))
"""
0 (0, 20, 0)
1 (148, 186, 111)
2 (0, 20, 0)
3 (145, 182, 105)
4 (0, 24, 0)
1 (142, 180, 105)
2 (0, 20, 0)
3 (158, 195, 118)
4 (0, 22, 0)
5 (150, 184, 108)
2 (0, 20, 0)
3 (148, 186, 109)
4 (0, 20, 0)
5 (158, 195, 118)
6 (0, 19, 0)
3 (139, 177, 100)
4 (0, 21, 0)
5 (148, 185, 108)
6 (0, 20, 0)
7 (156, 190, 114)
4 (0, 20, 0)
5 (144, 181, 104)
6 (0, 22, 0)
7 (153, 190, 113)
8 (0, 19, 0)
"""
for x in range(w):
    for y in range(h):
        if (x + y) % 2 == 1:
            draw.point((x, y), 0)

img.show() # evil