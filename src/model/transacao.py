from peewee import PostgresqlDatabase, Model, AutoField, CharField, FloatField, IntegerField

db = PostgresqlDatabase(database='unico', user='postgres', password='postgres', host='localhost', port=5432)

class Transacao(Model):
    id = AutoField()
    id_transacao = CharField()
    conta_origem = CharField()
    bank_name = CharField()
    date = CharField()
    valor = FloatField()
    class Meta:
        table_name = "transacao"
        database = db

db.connect()
db.create_tables([Transacao])
db.close()