from PIL import Image

with open('mozart.gif', 'rb') as f:
    img = Image.open(f)
    new_img = Image.new(img.mode, img.size)
    w, h = img.size
    for y in range(h):
        shift = None
        for x in range(w):
            pixel = img.getpixel((x, y))
            if pixel == 195:
                shift = x
                break
        assert shift is not None, 'Error'

        for x in range(w):
            pixel = img.getpixel((x, y))
            new_x = x - shift
            if new_x < 0:
                new_x = w + new_x
            new_img.putpixel((new_x, y), pixel)

new_img.show()


