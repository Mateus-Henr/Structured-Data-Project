from src.model.transacao import Transacao

class TransacaoDAO:
    @staticmethod

    def get_transacao_by_id(transacao_id):
        try:
            return Transacao.get_by_id(transacao_id)
        except Transacao.DoesNotExist:
            return None

    @staticmethod
    def get_transacoes():
        return Transacao.select()

    @staticmethod
    def insert_trasacao(nome, chave_pix, valor, data):
        return Transacao.create(nome=nome, chave_pix=chave_pix, valor=valor, data=data)