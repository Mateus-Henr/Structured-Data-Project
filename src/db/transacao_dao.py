from src.model.transaction import Transaction


class TransactionDAO:
    @staticmethod
    def get_transaction_by_id(transaction_id):
        try:
            return Transaction.get_by_id(transaction_id)
        except Transaction.DoesNotExist:
            return None

    @staticmethod
    def get_transaction(id):
        return Transaction.select().where(Transaction.id == id).execute()

    @staticmethod
    def insert_transaction(transaction_id, source_account, bank_name, date, value, JSON):
        return Transaction.create(transaction_id=transaction_id, source_account=source_account, bank_name=bank_name,
                                  date=date,
                                  value=value, JSON=JSON)

    @staticmethod
    def get_transactions():
        return Transaction.select()
