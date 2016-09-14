# http://www.pythonchallenge.com/pc/return/evil.html
from PIL import Image
from io import BytesIO

with open('evil2.gfx', 'rb') as f:
    data = f.read()
    """
    for i in range(1, 5):
        data1 = data[i::5]
        f1 = BytesIO(data1)
        img = Image.open(f1)
        img.show()
    """
    # One of files are broken and should be opened externally

    types = ['jpg', 'png', 'gif', 'png', 'jpg']
    for i in range(5): open('evil2%d.%s' % (i, types[i]), 'wb').write(data[i::5])


#disproportional