from src.model.bank import Bank


class BankDAO:
    @staticmethod
    def get_bank_by_id(bank_id):
        try:
            return Bank.get_by_id(bank_id)
        except Bank.DoesNotExist:
            return None

    @staticmethod
    def get_banks():
        return Bank.select()

    @staticmethod
    def insert_bank(name, valor, api_key, bank_type):
        return Bank(name=name, valor=valor, api_key=api_key, bank_type=bank_type).save()
