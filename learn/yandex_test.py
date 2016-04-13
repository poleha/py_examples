"""
Есть два списка разной длины. В первом содержатся ключи, а во втором значения.
Напишите функцию, которая создаёт из этих ключей и значений словарь. Если ключу не хватило значения,
в словаре должно быть значение None. Значения, которым не хватило ключей, нужно игнорировать.
"""
#from operator import

keys = [1, 2, 3]
values = [4, 5, 6]

def make_dict(keys, values):
    unique_keys = set(keys)
    assert len(keys) == len(unique_keys), 'Keys are not unique'
    d = {}
    for i in range(len(keys)):
        d[keys[i]] = values[i] if i < len(values) else None
    return d


print(make_dict(keys, values))


"""
В системе авторизации есть ограничение: логин должен начинаться с латинской буквы, состоять из латинских букв,
цифр, точки и минуса, но заканчиваться только латинской буквой или цифрой; минимальная длина логина —
один символ, максимальная — 20. Напишите код на вашем любимом языке программирования, проверяющий соответствие
 входной строки этому правилу. Придумайте несколько способов решения задачи и сравните их.
"""
import time
import re
import string

def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(end - start)
        return res
    return wrapper

@time_it
def validate_username_re(value):
    return 1 < len(value) <= 20 and (False if re.fullmatch('^[a-zA-Z][a-zA-Z0-9-\.]*[a-zA-Z0-9]$', value) is None else True)

@time_it
def validate_username_iter(value):
    if not 1 < len(value) <= 20:
        return False
    if not value[0].lower() in string.ascii_lowercase:
        return False
    if not value[-1].lower() in string.ascii_lowercase + string.digits:
        return False
    for elem in value[1:-1]:
        if not elem.lower() in string.ascii_lowercase + string.digits + '-' + '.':
            return False
    return True

print(validate_username_re('C1fjdn-...---3324238')) #0.00015473365783691406
print(validate_username_iter('C1fjdn-...---3324238')) #1.1682510375976562e-05


"""
Есть две таблицы — users и messages:

users
UID Name
1.	Платон Щукин
2.	Лера Страза
3.	Георгий Атласов

messages
UID msg
1 – "Привет, Платон!"
3 – "Срочно пришли карту."
3 – "Жду на углу Невского и Тверской."
1 – "Это снова я, пиши чаще"

Напишите SQL-запрос, результатом которого будет таблица из двух полей: «Имя пользователя» и «Общее количество сообщений».

SELECT u.name, COUNT(m.UID) FROM users u LEFT JOIN messages m ON u.UID = m.UID GROUP BY u.id;

"""


"""
Предположим, у нас есть access.log веб-сервера. Как с помощью стандартных консольных средств найти десять IP-адресов,
от которых было больше всего запросов? А как сделать это с помощью программы на вашем любимом языке программирования?
"""

#!/var/www/venv/bin/python
import sys
from collections import Counter

with open(sys.argv[0]) as f:
    ips = (re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line).group() for line in f)

    c = Counter(ips)
    print(c.most_common(10))
