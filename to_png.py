import sys
from PIL import Image

filename = sys.argv[1]

with open(filename, 'rb') as f:
    new_filename = filename.replace('jpg', 'png')
    new_filename = new_filename.replace('JPG', 'png')
    new_filename = new_filename.replace('jpeg', 'png')
    new_filename = new_filename.replace('JPEG', 'png')
    img = Image.open(f)
    img.save(new_filename, 'PNG')