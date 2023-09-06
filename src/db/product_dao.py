from src.model.product import Product  # Importe o modelo do Produto

class ProductDAO:
    @staticmethod
    def get_produto_by_id(produto_id):
        try:
            return Product.get_by_id(produto_id)
        except Product.DoesNotExist:
            return None

    @staticmethod
    def get_produtos():
        return Product.select()

    @staticmethod
    def insert_produto(nome, valor, estoque):
        return Product.create(nome=nome, valor=valor, estoque=estoque)
