from peewee import PostgresqlDatabase, Model, AutoField, CharField, FloatField, IntegerField

db = PostgresqlDatabase(database='unico', user='postgres', password='postgres', host='localhost', port=5432)

class Transacao(Model):
    id = AutoField()
    nome = CharField()
    chave_pix = CharField()
    valor = FloatField()
    data = CharField()
    class Meta:
        table_name = "transacao"
        database = db

db.connect()
db.create_tables([Transacao])
db.close()