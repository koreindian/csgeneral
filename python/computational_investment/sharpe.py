import numpy as np
import pandas.io.data as web


def main():
    '''
    info = read_user_input()
    print info 
    stock = get_stock_data(name=info[0], start=info[1], end=info[2])
    '''

    stock = get_stock_data(name='GOOG', start='3/10/2015', end='3/19/2015')

    print stock
    print stock['Close'][0]

    drets = daily_returns(stock)
    print drets

    s = sharpe(stock)
    print s

def sharpe(stock):
    dret = daily_returns(stock)
    dret_array = np.asarray(dret)

    risk = np.std(dret_array)
    mean_dret = np.mean(dret_array)
    k = np.sqrt(len(dret))
    
    return mean_dret * k / risk

def daily_returns(stock):
    drets = []

    for i in range(len(stock)):
        if i == 0:
            drets.append(0)
        else:
            dret = stock['Close'][i] / stock['Close'][i-1] - 1
            drets.append(dret)

    return drets

def read_user_input():
    name = input('Enter stock name: ')
    start = input('Enter start date: ')
    end = input('Enter end date: ')
    
    return [name, start, end]

def get_stock_data(name, start, end):
    print name + " " + start + " " + end
    try:
        stock = web.DataReader(name, 'google', start, end)
    except IOError:
        print "IOError"

    return stock

if __name__ == "__main__":
    main()
