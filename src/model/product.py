import random
from peewee import PostgresqlDatabase, Model, AutoField, CharField, FloatField, IntegerField

db = PostgresqlDatabase(database='unico', user='postgres', password='postgres', host='localhost', port=5432)

class Product(Model):
    id = AutoField()
    nome = CharField()
    valor = FloatField()
    estoque = IntegerField()

    class Meta:
        table_name = "produto"
        database = db
def insert_random_products():
    for _ in range(30):
        nome = random.choice(["Banana", "Computador", "Coxinha", "Arroz", "Feijão", "Leite", "Cerveja", "Pão", "Maçã", "Chocolate", "Carne", "Batata", "Sabonete", "Água Mineral", "Sorvete", "Queijo", "Cenoura", "Sabão em Pó", "Vinho", "Abacaxi", "Detergente", "Sal", "Biscoitos", "Laranja", "Shampoo", "Água Sanitária", "Macarrão", "Melancia", "Desodorante", "Lâmpadas"])
        valor = round(random.uniform(0.01, 1.0), 2)  # Valor aleatório entre 0.01 e 1.0
        estoque = random.randint(1, 100)  # Estoque aleatório entre 1 e 100

        try:
            Product.get(Product.nome == nome)  # Verifica se o produto já existe
        except Product.DoesNotExist:
            Product.create(nome=nome, valor=valor, estoque=estoque)  # Insere o produto se não existir



db.connect()
db.create_tables([Product])
insert_random_products()
db.close()
