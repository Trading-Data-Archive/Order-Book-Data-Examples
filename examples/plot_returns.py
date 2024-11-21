from orm import *
import peewee as pw
import datetime
import matplotlib.pyplot as plt

NUM_MARKETS = 10

db = pw.SqliteDatabase('example_dataset.db', pragmas={'foreign_keys': 1})
database_proxy.initialize(db)



def main():
    markets = {market : f'{market.base.name}-{market.quote.name}' for market in Market.select().where(Market.id <= NUM_MARKETS)}

    updates = {market : {'times': [], 'prices': []} for market in markets}
    initial_prices = {market: 0 for market in markets}

    print('loading data')

    for trade in Trade.where(:
        if trade.market.id >= NUM_MARKETS:
            continue
        if initial_prices[trade.market] == 0:
            initial_prices[trade.market] = float(trade.price)
        updates[trade.market]['times'].append(datetime.datetime.fromtimestamp(trade.time / 1000))
        updates[trade.market]['prices'].append(float(trade.price) / initial_prices[trade.market])
    print('done')

    print('plotting...')

    for market, update in updates.items():
        plt.plot(update['times'], update['prices'], label=markets[market])

    plt.legend()
    plt.show()



if __name__=="__main__":
    main()
