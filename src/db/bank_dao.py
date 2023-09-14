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
    def update_bank(name, api_key, bank_type):
        # Find the first bank that matches the conditions (e.g., by name)
        bank_to_update = Bank.get_or_none(name=name)

        if bank_to_update:
            # Update the bank object with the new values
            bank_to_update.api_key = api_key
            bank_to_update.bank_type = bank_type
            # Save the updated bank object to the database
            bank_to_update.save()
            # Return the updated bank object
            return bank_to_update
        else:
            # Handle the case where no matching bank was found
            return None

