from src.model.bank import Bank


class BankDAO:
    @staticmethod
    def get_bank():
        try:
            return Bank.select().first()
        except Bank.DoesNotExist:
            return None

    @staticmethod
    def update_or_create_bank(name, api_key):
        try:
            bank_to_update = Bank.get(name=name)
        except Bank.DoesNotExist:
            bank_to_update = Bank.create(name=name, api_key=api_key)

        bank_to_update.api_key = api_key
        bank_to_update.save()

        return bank_to_update
