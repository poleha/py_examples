# http://www.pythonchallenge.com/pc/return/italy.html
from PIL import Image


with open('wire.png', 'rb') as f:
    source_image = Image.open(f)
    dest = Image.new(source_image.mode, (100, 100))

    directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
    x = -1
    y = 0
    z = 0

    for i in range(200):
        direction = directions[i % 4]
        # 0 0
        # 1 1
        # 2 2
        # 3 3
        # 4 0
        # 5 1

        print(100 - (i + 1) // 2, end=' ') #100 99 99 98 98 97 97 96 96 95 95 94 94 93 93 92 92...
        for j in range(100 - (i + 1) // 2):
            pixel = source_image.getpixel((z, 0))
            x += direction[0]
            y += direction[1]
            dest.putpixel((x, y), pixel)
            z += 1

dest.show()



