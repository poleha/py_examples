def recMC(coinValueList, change):
    if change in coinValueList:
        return 1
    else:
        res = change
        for coin in [coin for coin in coinValueList if coin <= change]:
            res = min(1 + recMC(coinValueList, change - coin), res)
        return res


print(recMC([1, 5, 10, 25], 63))