from peewee import *

db = PostgresqlDatabase(database='unico', user='postgres', password='postgres', host='localhost', port=5432)


class Bank(Model):
    id = AutoField()
    name = CharField()
    api_key = CharField()
    bank_type = CharField()

    class Meta:
        table_name = "dav"
        database = db


db.connect()
db.create_tables([Bank])
db.close()
 