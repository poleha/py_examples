"""
Требовалось переставить все диски с одного стержня на другой, соблюдая два строгих условия.
Во-первых, за раз можно было перемещать только один диск. Во-вторых, нельзя класть бОльший диск поверх меньшего.
Переставить 5 это значит переставить 4, переставить 1 и еще раз 4.
Тогда как 4 это 3, 1 и 3
И так далее
"""


#Simple move count
def move(num):
    if num > 1:
        return 1 + 2 * move(num - 1)
    else:
        return 1

print(move(20))


def moveTower(height,fromPole, toPole, withPole):
    if height >= 1:
        moveTower(height-1,fromPole,withPole,toPole)
        moveDisk(fromPole,toPole)
        moveTower(height-1,withPole,toPole,fromPole)

count = 0

def moveDisk(fp,tp):
    global count
    count += 1
    print("moving disk from",fp,"to",tp)

moveTower(5,"A","B","C")
print(count)
