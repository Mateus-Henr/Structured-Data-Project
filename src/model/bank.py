from peewee import *

db = PostgresqlDatabase(database='unico', user='postgres', password='postgres', host='localhost', port=5432)


class Bank(Model):
    id = AutoField()
    name = CharField()
    valor = FloatField()
    api_key = CharField()
    pix_key = CharField()
    bank_type = CharField()

    class Meta:
        table_name = "dav"
        database = db
