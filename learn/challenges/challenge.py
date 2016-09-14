from PIL import Image, ImageDraw
from urllib.request import urlretrieve
from scipy import misc
from io import BytesIO
from math import sqrt
import os
import zipfile

url = 'http://alcove.io/challenge.x.png'
file, message = urlretrieve(url)

f = open(file, 'rb')

im = Image.open(f)


w, h = im.size
"""
for y in range(w):
    for x in range(h):
        pixel = im.getpixel((x, y))
        if pixel[0] > 0:
            print(hex(pixel[1]), end=' ')
    print()


"""
x = 480
y = 320
visited = {(x, y)}


colors = {}

def get_next(x, y):
    for i in range(8):
        if i == 0:
            x1 = x - 1
            y1 = y
        elif i == 1:
            x1 = x + 1
            y1 = y
        elif i == 2:
            x1 = x
            y1 = y - 1
        elif i == 3:
            x1 = x
            y1 = y + 1

        elif i == 4:
            x1 = x - 1
            y1 = y - 1
        elif i == 5:
            x1 = x - 1
            y1 = y + 1
        elif i == 6:
            x1 = x + 1
            y1 = y - 1
        elif i == 7:
            x1 = x + 1
            y1 = y + 1


        pixel = im.getpixel((x1, y1))
        if pixel[0] != 0 and (x1, y1) not in visited:
            visited.add((x1, y1))
            return x1, y1

res = []
while True:
    try:
        x, y = get_next(x, y)
        #draw.point((x, y))
        pixel = im.getpixel((x, y))
        cur = pixel[1]
        #cur = cur.to_bytes(2, byteorder='big')
        res.append(cur)
        #print(x, y)
        #if cur not in colors:
        #    colors[cur] = 0
        #colors[cur] += 1
        #print(cur, end=' ')
    except:
        break

#f1 = BytesIO(res)
im = Image.new('RGB', (640, 640))
print(res)
#draw = ImageDraw.Draw(im)
#draw.point(res)
#im.show()
#im.show()
#f1 = open('test', 'wb')
#f1.write(res)

"""

a, b, c = non_zero


x = 479
y = 319

visited = {(x, y)}


def get_next(x, y):
    for i in range(8):
        if i == 0:
            x1 = x
            y1 = y - 1
        elif i == 1:
            x1 = x
            y1 = y + 1
        elif i == 2:
            x1 = x - 1
            y1 = y
        elif i == 3:
            x1 = x + 1
            y1 = y
        elif i == 4:
            x1 = x + 1
            y1 = y + 1
        elif i == 5:
            x1 = x - 1
            y1 = y - 1
        elif i == 6:
            x1 = x - 1
            y1 = y + 1
        elif i == 7:
            x1 = x + 1
            y1 = y - 1
        color = face[y1][x1]
        if color[0] != 0 and (x1, y1) not in visited:
            visited.add((x1, y1))
            return x1, y1

im = Image.fromarray(face, 'RGB')
draw = ImageDraw.Draw(im)
k = 0
while True:
    try:
        x, y = get_next(x, y)
        draw.point((x, y))
        k += 1
        color = face[y][x]
        cur = str(hex(color[1]))[-2:]
        print(color[1], end=',')
    except:
        print(x, y)
        break


im.show()
"""
"""

colors = {}

visited = set()

for i in range(len(a)):
    x = b[i]
    y = a[i]
    if (x, y) in visited:
        continue
    visited.add((x, y))
    color = face[a[i], b[i]]
    red = color[0]
    green = color[1]
    blue = color[2]
    #print(red, green, blue)
    if green not in colors:
        colors[green] = {'count': 0, 'coords': []}
    colors[green]['count'] += 1
    colors[green]['coords'].append((x, y))

for color in colors:
    print(color, colors[color]['count'], colors[color]['coords'])
"""
"""
visited = set()

for i in range(len(a)):
    y = a[i]
    x = b[i]
    visited.add((x, y))
    draw.point((x, y))

print(len(visited))



colors = {}

for i in range(len(a)):
    color = face[a[i], b[i]]
    red = color[0]
    green = color[1]
    blue = color[2]
    #print(red, green, blue)
    if green not in colors:
        colors[green] = 0
    colors[green] += 1


print(len(colors.keys()))






def get_next(x, y):
    count = 0
    for i in range(8):
        if i == 0:
            x1 = x
            y1 = y - 1
            count += 1
        if i == 1:
            x1 = x
            y1 = y + 1
            count += 1
        if i == 2:
            x1 = x - 1
            y1 = y
            count += 1
        if i == 3:
            x1 = x + 1
            y1 = y
            count += 1
        if i == 4:
            x1 = x + 1
            y1 = y + 1
            count += 1
        if i == 5:
            x1 = x - 1
            y1 = y - 1
            count += 1
        if i == 6:
            x1 = x - 1
            y1 = y + 1
            count += 1
        if i == 7:
            x1 = x + 1
            y1 = y - 1
            count += 1
        color = face[y1][x1]
        if color[0] != 0 and (x1, y1) not in visited:
            visited.add((x1, y1))
            return x1, y1, count


x = 319
y = 479
visited = {x, y}
draw.point((x, y))
k = 0
res = {}
while True:
    try:
        x, y, count = get_next(x, y)
        if count == 5:
            print(x, y, count)
        draw.point((x, y))
        k += 1
        color = face[y][x]
        cur = str(hex(color[1]))[-2:]
    except:
        print(x, y)
        break

print(len(visited), k)
im.show()










#im.show()
"""

"""

x = 479
y = 319

visited = {(x, y)}


def get_next(x, y):
    for i in range(8):
        if i == 0:
            x1 = x
            y1 = y - 1
        elif i == 1:
            x1 = x
            y1 = y + 1
        elif i == 2:
            x1 = x - 1
            y1 = y
        elif i == 3:
            x1 = x + 1
            y1 = y
        elif i == 4:
            x1 = x + 1
            y1 = y + 1
        elif i == 5:
            x1 = x - 1
            y1 = y - 1
        elif i == 6:
            x1 = x - 1
            y1 = y + 1
        elif i == 7:
            x1 = x + 1
            y1 = y - 1
        color = face[y1][x1]
        if color[0] != 0 and (x1, y1) not in visited:
            visited.add((x1, y1))
            return x1, y1

im = Image.fromarray(face, 'RGB')
draw = ImageDraw.Draw(im)
draw.point((x, y))
k = 0
while True:
    try:
        x, y = get_next(x, y)
        draw.point((x, y))
        k += 1
        color = face[y][x]
        cur = str(hex(color[1]))[-2:]
    except:
        print(x, y)
        break

print(len(visited), k)
im.show()
"""
"""



#print(min_d, max_d)
im = Image.fromarray(face, 'RGB')
draw = ImageDraw.Draw(im)

results = {}

#max_d = 103258
for i in range(len(a)):
    y = a[i]
    x = b[i]
    max_d = 0
    coords = None
    for j in range(len(a)):
        y1 = a[j]
        x1 = b[j]
        d = (x1 - x) ** 2 + (y1 - y) ** 2
        if d > max_d:
            coords = (x, y, x1, y1)
            max_d = d
    #print(coords, max_d)
    results[coords] = max_d

k = 0
for coords, d in results.items():
    x, y, x1, y1 = coords
    print(x, y, x1, y1, face[y][x], face[y1][x1])

im.show()
"""
"""
results = []
for i in range(len(a)):
    y = a[i]
    x = b[i]
    max_d = 0
    min_d = 0
    for j in range(len(a)):
        y1 = a[j]
        x1 = b[j]
        d = (x1 - x) ** 2 + (y1 - y) ** 2
        max_d = max(d, max_d)
        min_d = min(d, min_d)
    results.append(max_d)

"""

"""
max_d = 103258#max(max_results)


#print(min_d, max_d)

results = []

#max_d = 103258
for i in range(len(a)):
    y = a[i]
    x = b[i]

    for j in range(len(a)):
        y1 = a[j]
        x1 = b[j]
        d = (x1 - x) ** 2 + (y1 - y) ** 2
        if d == max_d:
            results.append((x, y, x1, y1, d))




im = Image.fromarray(face, 'RGB')
draw = ImageDraw.Draw(im)

k = 0
for result in results:
    x, y, x1, y1, d = result

    draw.line((x, y, x1, y1))
    print(x, y, x1, y1)
    print(face[y][x])

im.show()
"""



"""
colors = {}

for i in range(len(a)):
    color = face[a[i], b[i]]
    red = color[0]
    green = color[1]
    blue = color[2]
    #print(red, green, blue)
    if green not in colors:
        colors[green] = 0
    colors[green] += 1

"""

"""
center_x = 320#(right + left) / 2
center_y = 320#(bottom + top) / 2
r = 160

#print(center_x, center_y)

draw.point((center_x, center_y))
draw.line(((320, 320), (480, 320)))

for x in range(640):
    for y in range(640):
        f = (x - 320) **2 + (y - 320) **2 == r**2
        if f:
            print(face[y][x])
            draw.point((x, y))


im.show()
"""


#im = Image.fromarray(face, 'RGB')
#im.show()
"""
a, b, c = non_zero



for i in range(len(a)):
    y = a[i]
    line = face[y]
    nonzero_in_line = line.nonzero()
    d, e = nonzero_in_line
    s = 0
    for j in range(len(d)):
        x = d[j]
        if e[j] == 0:
            s += 1
            color = line[x]
            #print(y, x,  color)
    if s % 2 != 0:
        pass
        #print(y)



"""
"""
colors = {}

for i in range(len(a)):
    color = face[a[i], b[i]]
    red = color[0]
    green = color[1]
    blue = color[2]
    #print(red, green, blue)
    if green not in colors:
        colors[green] = 0
    colors[green] += 1



for color in colors:
    if colors[color] % 3 != 0:
        print(color, colors[color])

for i in range(len(a)):
    color = face[a[i], b[i]]
    if color[1] == 0:
        print(a[i], b[i])
    else:
        color[0] = 0
        color[1] = 0
        color[2] = 0
"""

#for i in range(256):
#    if i not in colors:
#        print(i)



"""

im = Image.new('RGB', (640, 640))
#im = Image.open(f)
#im = Image.fromarray(face, 'RGB')
draw = ImageDraw.Draw(im)
draw.ellipse((left, top, right, bottom))
f = io.BytesIO()
im.save(f, 'PNG')

new_face = misc.imread(f)
new_non_zero = new_face.nonzero()

a1, b1, c1 = new_non_zero

for i in range(len(a1)):
    color = new_face[a1[i], b1[i]]
    if color[0] == 255 and color[1] == 255 and color[2] == 255:
        color = face[a1[i], b1[i]]
        color[0] =  0
        color[1] = 0
        color[2] = 0

im = Image.fromarray(face, 'RGB')
im.show()
print(non_zero[0].__len__(), new_non_zero[0].__len__())
"""
"""
for y in a:
    s = set()
    line = face[y].nonzero()[0]
    for x in line:
        s.add(x)
    if len(s) % 2 == 1:
        print(y, s)

"""
"""
top = min(a)
bottom = max(a)

vertical_d = bottom - top

left = min(b)
right = max(b)

horizontal_d = right - left

x = right
print(x)



top_y = a[0]
top_x = b[0]


bottom_y = a[-1]
bottom_x = b[-1]

d = bottom_y - top_y
r = d / 2

center_y = top_y + r
"""
#colors = {}

"""
for i in range(len(a)):
    color = face[a[i], b[i]]
    if color[0] == 255 and color[1] == 255 and color[2] == 255:
        print(a[i], b[i])
    else:
       color[0] = color[1] = color[2] = 0
"""

#im = Image.open(f)
#draw = ImageDraw.Draw(im)
#draw.line(((0, 239), (639, 239) ))
#draw.line(((0, 320), (639, 320) ))
#im.show()
#draw.ellipse((top_x, top_y, top_x + 10, top_y + 10))
#draw.ellipse((left, left, bottom, bottom))

#im = Image.fromarray(face, 'RGB')
#im.show()
"""
im = Image.new('RGB', (640, 640))
draw = ImageDraw.Draw(im)
draw.ellipse((left, left, bottom, bottom))
del draw

im.save('tmp.png')
f = open('tmp.png', 'rb')



face = misc.imread(f)
non_zero = face.nonzero()

a, b, c = non_zero

top = min(a)
bottom = max(a)
left = min(b)
right = max(b)

print(top, bottom, left, right)

"""