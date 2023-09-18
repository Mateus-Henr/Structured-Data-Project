import mercadopago
import os

from controller.pix_interface import PixInterface
from model.bank import Bank
from model.pix import Pix
from db.transacao_dao import TransactionDAO

MERCADO_PAGO = "MERCADO PAGO"


def exclude_qr_code_img():
    """
    Removes the QR code image file.
    """
    os.remove("qrcode.jpg")


class PixMercadoPago(PixInterface):
    def __init__(self, value: float, bank: Bank):
        super(PixInterface, self).__init__()
        self.status = None
        self.mp = mercadopago.SDK(bank.api_key)
        self.pix = self.create_pix(value)

    def create_pix(self, value: float):
        """
        Creates a payment using CPF as identification.
        """
        payment_data = {
            "transaction_amount": value,
            "description": "Título do produto",
            "payment_method_id": "pix",
            "payer": {
                "email": "nome@email.com"
            }
        }

        data = self.mp.payment().create(payment_data)

        return Pix(data["response"]["id"],
                   "Mercado Pago",
                   data["response"]["date_created"],
                   value,
                   data["response"]["point_of_interaction"]["transaction_data"]["qr_code_base64"],
                   data["response"]["point_of_interaction"]["transaction_data"]["ticket_url"])

    def is_done(self):
        payment = self.mp.payment().get(self.pix.id)

        # Verificar se o pagamento está concluído
        if payment["status"] == 200:
            self.status = payment["response"]["status"]

            if self.status == "approved":
                transaction_id = payment["response"]["transaction_details"]["transaction_id"]
                account_id = payment["response"]["point_of_interaction"]["transaction_data"]["bank_info"]["payer"][
                    "account_id"]
                bank_name = payment["response"]["point_of_interaction"]["transaction_data"]["bank_info"]["payer"][
                    "long_name"]
                date_approved = payment["response"]["date_approved"]
                total_paid_amount = payment["response"]["transaction_details"]["total_paid_amount"]

                JSON = payment["response"]

                TransactionDAO.insert_transaction(transaction_id, account_id, bank_name, date_approved,
                                                  total_paid_amount, JSON)

        else:
            self.status = "pending"

        return self.status != "pending"
