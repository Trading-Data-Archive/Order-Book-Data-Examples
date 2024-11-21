from orm import *
import peewee as pw


class OrderBook:

    def __init__(self):
        self.bids = {}
        self.asks = {}
        self.last_update_id = 0
        self.time = 0

    def add_update(self, time, update_id, side, price, volume):
        #side = 1 for buy 0 for sell
        
        price = float(price)
        volume = float(volume)
        side = bool(side)

        self.time = time
        
        if side:
            self.bids[price] = volume
        else: 
            self.asks[price] = volume



    


def main():
    db = pw.SqliteDatabase('example_dataset.db')
    database_proxy.initialize(db)

    print('Initializing books')
    books = {}
    for market in Market:
        books[market] = OrderBook()

    #initalize snapshots

    for snapshot in BookSnapshot:
        books[snapshot.market].add_update(snapshot.time, snapshot.updateid, snapshot.buy, snapshot.price, snapshot.volume)

    print('done')
    #get highest id
    q = BookUpdate.select().order_by(BookUpdate.id.desc())
    max_id = q[0].id
    #run through dataset
    for i, update in enumerate(BookUpdate):
        if i % 10000 == 0:
            print(f'handling update {i} of {max_id}')
        books[update.market].add_update(update.time, update.updateid, update.buy, update.price, update.volume)




if __name__=="__main__":

    main()
