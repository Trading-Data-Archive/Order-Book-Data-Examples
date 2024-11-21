import peewee as pw

#database = pw.SqliteDatabase(None, pragmas={'foreign_keys': 1})

database_proxy = pw.DatabaseProxy()

class BaseModel(pw.Model):
    class Meta:
        database = database_proxy
        pass

class Asset(BaseModel):
    name = pw.CharField(unique=True)

class Market(BaseModel):
    base = pw.ForeignKeyField(Asset, on_delete='CASCADE', backref='markets')
    quote = pw.ForeignKeyField(Asset, on_delete='CASCADE', backref='market_quotes')


class BookUpdate(BaseModel):
    market = pw.ForeignKeyField(Market, on_delete='CASCADE', backref='updates')
    time = pw.IntegerField()
    updateid = pw.IntegerField()
    buy = pw.BooleanField()  #True for buy
    price = pw.CharField()
    volume = pw.CharField()

class BookSnapshot(BaseModel):
    market = pw.ForeignKeyField(Market, on_delete='CASCADE', backref='updates')
    time = pw.IntegerField()
    updateid = pw.IntegerField()
    buy = pw.BooleanField()  #True for buy
    price = pw.CharField()
    volume = pw.CharField()


class Trade(BaseModel):
    market = pw.ForeignKeyField(Market, on_delete='CASCADE', backref='trades')
    time = pw.IntegerField()
    updateid = pw.IntegerField()
    buy = pw.BooleanField() #True if maker is buyer
    price = pw.CharField()
    volume = pw.CharField()

