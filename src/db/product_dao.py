from src.model.product import Product  # Importe o modelo do Produto


class ProductDAO:
    @staticmethod
    def get_produto_by_id(produto_id: int):
        try:
            return Product.get_by_id(produto_id)
        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_produtos():
        return Product.select()

    @staticmethod
    def insert_produto(name, value, inventory):
        return Product.create(name=name, value=value, inventory=inventory)

    @staticmethod
    def get_produto(id):
        return Product.select().where(Product.id == id)

    @staticmethod
    def remove_produto(id):
        return Product.delete().where(Product.id == id).execute()

    @staticmethod
    def modify_produto(id, nome, valor, estoque):
        return Product.update({Product.name: nome, Product.value: valor, Product.inventory: estoque}).where(
            Product.id == id).execute()

    @staticmethod
    def modify_produto_nome(id, nome):
        return Product.update({Product.name: nome}).where(Product.id == id).execute()

    @staticmethod
    def modify_produto_valor(id, valor):
        return Product.update({Product.value: valor}).where(Product.id == id).execute()

    @staticmethod
    def modify_produto_estoque(id, estoque):
        return Product.update({Product.inventory: estoque}).where(Product.id == id).execute()
