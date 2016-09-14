from PIL import Image, ImageDraw
from urllib.request import urlretrieve
from scipy import misc

# Retrieving and opening the image
url = 'http://alcove.io/challenge.x.png'
file, message = urlretrieve(url)

f = open(file, 'rb')

# Using scipy to analyze the image
face = misc.imread(f)
non_zero = face.nonzero()

a, b, c = non_zero

# Getting left, right, top and bottom points of the circle
top = min(a)
bottom = max(a)
left = min(a)
right = max(a)

vertical_d = bottom - top
horizontal_d = right - left

assert vertical_d == horizontal_d

# Opening image for editing. There's no practical use in that, but I think that's kind of way to follow
im = Image.open(f)
draw = ImageDraw.Draw(im)
draw.ellipse((left, left, right, right))
del draw

# Showing image
im.show()
