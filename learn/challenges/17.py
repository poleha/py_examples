# http://www.pythonchallenge.com/pc/return/romance.html


import http.cookiejar, urllib.request
from urllib.parse import unquote_to_bytes
from bz2 import BZ2Decompressor


auth_handler = urllib.request.HTTPBasicAuthHandler()
auth_handler.add_password('inflate', 'www.pythonchallenge.com', 'huge', 'file')
cj = http.cookiejar.CookieJar()
cookie_handler = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(auth_handler, cookie_handler)

res = 'BZh91AY%26SY%94%3A%E2I%00%00%21%19%80P%81%11%00%AFg%9E%A0+%00hE%3DM%B5%23%D0%D4%D1%E2%8D%06%A9%FA%26S%D4%D3%21%A1%EAi7h%9B%9A%2B%BF%60%22%C5WX%E1%ADL%80%E8V%3C%C6%A8%DBH%2632%18%A8x%01%08%21%8DS%0B%C8%AF%96KO%CA2%B0%F1%BD%1Du%A0%86%05%92s%B0%92%C4Bc%F1w%24S%85%09%09C%AE%24%90'
"""
busynothing = '12345'
res = ''
while True:
    #print(_)
    r = opener.open("http://www.pythonchallenge.com/pc/def/linkedlist.php?busynothing={}".format(busynothing))
    data = r.read().decode()
    pos = data.find('busynothing is ')
    busynothing = data[pos + 15:]
    res += list(cj)[0].value
    try:
        busynothing = int(busynothing)
    except:
        break

print(res)
"""

res = res.replace('+', ' ')
data = unquote_to_bytes(res)
decompressor = BZ2Decompressor()
res = decompressor.decompress(data)
print(res)
#b'is it the 26th already? call his father and inform him that "the flowers are on their way". he\'ll understand.'


#>>> phonebook.phone('Leopold') from level 13
#'555-VIOLIN'


opener.open("http://www.pythonchallenge.com/pc/def/linkedlist.php") #to get cookie into the jar

list(cj)[0].value = 'the+flowers+are+on+their+way'
print(opener.open('http://www.pythonchallenge.com/pc/stuff/violin.php').read())

#b'<html>\n<head>\n  <title>it\'s me. what do you want?</title>\n  <link rel="stylesheet" type="text/css"
#  href="../style.css">\n</head>\n<body>\n\t<br><br>\n\t<center><font color="gold">\n\t<img src="leopold.jpg"
#  border="0"/>\n<br><br>\noh well, don\'t you dare to forget the balloons.</font>\n</body>\n</html>\n'

#noh well, don\'t you dare to forget the balloons => baloons