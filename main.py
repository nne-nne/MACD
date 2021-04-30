# Adam Leczkowski 180280

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jupyter as jp


def ema(n, vector):
    res = []
    a = 2/(n+1)
    for val in range(0, len(vector)):
        nominator = 0
        denominator = 1
        for i in range(0, n):
            if val-i >= 0:
                modifier = pow((1-a), i)
                nominator += vector[val-i] * modifier
                denominator += modifier
        res.append(nominator/denominator)
    return res


def log_transaction(money, actions, price, buying, howmany):
    print("money: ", money, " actions: ", actions)
    if buying:
        s = "buying"
    else:
        s = "selling"
    print("at price ", price, " ", s, " ", howmany)


def trust(macd):
    if macd > 0.0:
        return 0.2
    elif macd < -50.0:
        return 1.0
    else:
        return -0.016 * macd + 0.2


def stock(m, s, price):
    money = 1000
    actions = 0
    dif = m[0] - s[0]
    for i in range(1, len(m)):
        prev = dif
        dif = m[i]-s[i]
        if dif * prev <= 0:  # macd crossed signal
            if dif > prev:  # buy
                actions_to_buy = money * trust(m[i]) // price[i]
                #  actions_to_buy = money // price[i]
                log_transaction(money, actions, price[i], True, actions_to_buy)
                money -= actions_to_buy * price[i]
                actions += actions_to_buy
            if dif < prev:  # sell
                actions_to_sell = np.floor(actions * trust(m[i]))
                #  actions_to_sell = np.floor(actions)
                log_transaction(money, actions, price[i], False, actions_to_sell)
                money += actions_to_sell * price[i]
                actions -= actions_to_sell
    log_transaction(money, actions, price[i], False, actions)
    money += actions * price[-1]
    actions = 0
    print("final money: ", money, " actions: ", actions)


if __name__ == '__main__':
    columns = ['date', 'opening', 'max', 'min', 'closing', 'vol']
    data = pd.read_csv('cdpr.csv', names=columns)
    print(data.to_string())

    X = data.iloc[:, 0].values
    Y = data.iloc[:, 4].values  # zazwyczaj używa się cen zamknięcia (tako rzecze wikipedia)

    ema12 = ema(12, Y)
    ema26 = ema(26, Y)
    macd = []
    for i in range(0, len(Y)):
        macd.append(ema12[i] - ema26[i])
    signal = ema(9, macd)

    stock(macd, signal, Y)

    plt.plot(X, Y, label='price')
    plt.plot(X, macd, label='MACD')
    plt.plot(X, signal, label='SIGNAL')
    plt.xlabel('time')
    plt.ylabel('value')
    plt.title('MACD 180280')
    locs, labels = plt.xticks()
    plt.xticks(np.arange(0, 1000, step=100))
    plt.xticks(rotation=30)
    plt.legend()
    plt.show()
