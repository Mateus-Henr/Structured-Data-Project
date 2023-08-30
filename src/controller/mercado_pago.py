import mercadopago
import os

from controller.pix_interface import PixInterface
from model.bank import Bank
from model.pix import Pix

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

        if payment["status"] == 200:
            self.status = payment["response"]["status"]

        return self.status != "pending"
