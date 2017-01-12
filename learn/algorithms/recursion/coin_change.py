import time


def recMC1(coinValueList, change):
    if change in coinValueList:
        return 1
    else:
        res = change
        for coin in (coin for coin in coinValueList if coin <= change):
            res = min(1 + recMC1(coinValueList, change - coin), res)
        return res


#start = time.time()
#print(recMC1([1, 5, 10, 25], 63)) # 6
#print(time.time() - start) # 45.22507929801941

cache = {}

def recMC2(coinValueList, change):
    if change in coinValueList:
        return 1
    else:
        res = change
        for coin in (coin for coin in coinValueList if coin <= change):
            key = change - coin
            cur_res = cache.get(key, None)
            if cur_res is None:
                cur_res = recMC2(coinValueList, change - coin)
                cache[key] = cur_res
            res = min(1 + cur_res, res)
        return res

start = time.time()
print(recMC2([1, 5, 10, 25], 63)) # 6
print(time.time() - start) # 0.00013685226440429688


#See the_coin_changing_problem.py in sporting


def dyn_mc(coins, change):
    L = len(coins)
    prev = [0] + [float('inf')] * change
    for i in range(L):
        max_coin = coins[i]
        cur = []
        for j in range(change + 1):
            if j < max_coin:
                cur.append(prev[j])
            else:
                cur.append(min(prev[j], 1 + cur[j - max_coin]))
        prev = cur
    return cur[-1]



start = time.time()
print(dyn_mc([1, 5, 10, 25], 63))  # 6
print(time.time() - start)  # 8.916854858398438e-05



def dpMakeChange(coinValueList,change):
   minCoins = {}
   for cents in range(change+1):
      coinCount = cents
      for j in (c for c in coinValueList if c <= cents):
            if minCoins[cents-j] + 1 < coinCount:
               coinCount = minCoins[cents-j]+1
      minCoins[cents] = coinCount
   return minCoins[change]

start = time.time()
print(dpMakeChange([1, 5, 10, 25], 63))  # 6
print(time.time() - start)  # 7.152557373046875e-05






      #if __name__=='__main__':
#    from timeit import Timer

    #t1 = Timer("recMC1([1, 5, 10, 25], 63)", "from __main__ import recMC1")
    #t2 = Timer("recMC2([1, 5, 10, 25], 63)", "from __main__ import recMC2")
    #print(t2.timeit(), t2.timeit())



#Считаем, какие монеты использованы # stud
def dpMakeChange(coinValueList,change,minCoins,coinsUsed):
   for cents in range(change+1):
      coinCount = cents
      newCoin = 1
      for j in [c for c in coinValueList if c <= cents]:
            if minCoins[cents-j] + 1 < coinCount:
               coinCount = minCoins[cents-j]+1
               newCoin = j
      minCoins[cents] = coinCount
      coinsUsed[cents] = newCoin # То есть это последняя добавленная монета
   return minCoins[change]

def printCoins(coinsUsed,change):
   coin = change
   while coin > 0:
      thisCoin = coinsUsed[coin]
      print(thisCoin)
      coin = coin - thisCoin

def main():
    amnt = 11
    clist = [1,5,10,21,25]
    coinsUsed = [0]*(amnt+1)
    coinCount = [0]*(amnt+1)

    print("Making change for",amnt,"requires")
    print(dpMakeChange(clist,amnt,coinCount,coinsUsed),"coins")
    print("They are:")
    printCoins(coinsUsed,amnt)
    print("The used list is as follows:")
    print(coinsUsed)

main()