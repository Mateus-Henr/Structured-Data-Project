from peewee import PostgresqlDatabase, Model, AutoField, CharField, FloatField, IntegerField, TextField

db = PostgresqlDatabase(database='unico', user='postgres', password='postgres', host='localhost', port=5432)


class Transaction(Model):
    id = AutoField()
    transaction_id = CharField()
    source_account = CharField()
    bank_name = CharField()
    date = CharField()
    value = FloatField()
    JSON = TextField()

    class Meta:
        table_name = "transaction"
        database = db


db.connect()
db.create_tables([Transaction])
db.close()
