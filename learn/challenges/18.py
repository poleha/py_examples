from PIL import Image
import re
with open('deltas.gz', 'rb') as f:
    data = f.read()
    lines = data.split(b'\n')
    pairs = [(l[:53], l[56:]) for l in lines]
    columns = [b'\n'.join([p[i] for p in pairs]) for i in range(2)]
    import codecs
    unhex = lambda s: codecs.getdecoder('hex')(re.sub(b'[^0-9a-fA-F]', '', s))[0]

    for i in range(2):
        open('delta%d.png' % i, 'wb').write(unhex(columns[i]))
