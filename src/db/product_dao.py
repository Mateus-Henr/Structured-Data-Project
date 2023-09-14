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
    def get_produto(id):
        return Product.select().where(Product.id == id)

    @staticmethod
    def insert_produto(nome, valor, estoque):
        return Product.create(nome=nome, valor=valor, estoque=estoque)

    @staticmethod
    def remove_produto(id):
        return Product.delete().where(Product.id == id).execute()

    @staticmethod
    def modify_produto(id, nome, valor, estoque):
        return Product.update({Product.nome: nome, Product.valor: valor, Product.estoque: estoque}).where(Product.id == id).execute()

    @staticmethod
    def modify_produto_nome(id, nome):
        return Product.update({Product.nome: nome}).where(Product.id == id).execute()

    @staticmethod
    def modify_produto_valor(id, valor):
        return Product.update({Product.valor: valor}).where(Product.id == id).execute()

    @staticmethod
    def modify_produto_estoque(id, estoque):
        return Product.update({Product.estoque: estoque}).where(Product.id == id).execute()
