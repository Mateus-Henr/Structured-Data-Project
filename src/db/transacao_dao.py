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
    def get_transacao(id):
        return Transacao.select().where(Transacao.id == id)

    @staticmethod
    def insert_trasacao(id_transacao, conta_origem, bank_name, date, valor):
        return Transacao.create(id_transacao=id_transacao, conta_origem=conta_origem, bank_name=bank_name, date=date, valor=valor)
