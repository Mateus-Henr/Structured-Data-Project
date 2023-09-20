from peewee import PostgresqlDatabase
from src.db.product_dao import ProductDAO
from src.db.transacao_dao import TransactionDAO


def start_db():
    db = PostgresqlDatabase(database='unico', user='postgres', password='postgres', host='localhost', port=5432)
    return db


def close_db(db):
    db.close()


def execute(command, db):
    content = command.get_content()

    if content[0] == "\q":
        close_db(db)
        return [0]
    if content[0] == "\h":
        return [1]

    productdao = ProductDAO
    transacaodao = TransactionDAO

    clen = len(content)

    if content[0] == "\i" and clen == 4:
        productdao.insert_produto(content[1], content[2], content[3])
        return [2]
    if content[0] == "\\v":
        if clen == 1:
            rows = productdao.get_produtos()
            return [3, rows]
        if clen == 2:
            rows = productdao.get_produto(content[1])
            return [3, rows]
    if content[0] == "\m" and (clen == 4 or clen == 5):
        if content[1] == "-n":
            productdao.modify_produto_nome(content[2], content[3])
        elif content[1] == "-v":
            productdao.modify_produto_valor(content[2], content[3])
        elif content[1] == "-s":
            productdao.modify_produto_estoque(content[2], content[3])
        else:
            productdao.modify_produto(content[1], content[2], content[3], content[4])
        return [4]
    if content[0] == "\\r" and clen == 2:
        productdao.remove_produto(content[1])
        return [5]
    if content[0] == "\\t":
        if clen == 1:
            rows = transacaodao.get_transactions()
            return [6, rows]
        if clen == 2:
            rows = transacaodao.get_transaction(content[1])
            return [6, rows]
    return [7]
