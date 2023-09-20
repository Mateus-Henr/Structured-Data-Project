import random
from peewee import PostgresqlDatabase, Model, AutoField, CharField, FloatField, IntegerField

db = PostgresqlDatabase(database='unico', user='postgres', password='postgres', host='localhost', port=5432)


class Product(Model):
    id = AutoField()
    name = CharField()
    value = FloatField()
    inventory = IntegerField()

    class Meta:
        table_name = "product"
        database = db

    def __str__(self):
        return f"Product(id={self.id}, name='{self.name}', value={self.value}, inventory={self.inventory})"


def insert_random_products():
    for _ in range(30):
        name = random.choice(
            ["Banana", "Computador", "Coxinha", "Arroz", "Feijão", "Leite", "Cerveja", "Pão", "Maçã", "Chocolate",
             "Carne", "Batata", "Sabonete", "Playstation 5", "Sorvete", "Queijo", "Cenoura", "Sabão em Pó", "Vinho",
             "Abacaxi", "Detergente", "Sal", "Biscoitos", "Laranja", "Shampoo", "Água Sanitária", "Macarrão",
             "Melancia", "Desodorante", "Lâmpadas"])
        valor = round(random.uniform(0.01, 1.0), 2)
        inventory = random.randint(1, 100)

        try:
            Product.get(Product.name == name)
        except Product.DoesNotExist:
            Product.create(name=name, value=valor, inventory=inventory)


db.connect()
db.create_tables([Product])
insert_random_products()
db.close()
