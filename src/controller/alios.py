from controller.pix_interface import PixInterface
from model.bank import Bank
from model.pix import Pix
import json
import requests

ALIOS = "ALIOS"


class Alios(PixInterface):
    def __init__(self, value: float, bank: Bank):
        super(PixInterface, self).__init__()
        self.status = None
        self.access_token = bank.api_key
        self.key = bank.pix_key
        self.pix = self.create_pix(value)

    def create_pix(self, valor: float):
        url = "https://apiendpointhml.ailos.coop.br/qa/ailos/pix-cobranca/api/v1/cob"

        headers = {
            "Content-Type": "application/json",
            "x-ailos-authentication": self.access_token
        }

        payload = {
            "calendario": {
                "expiracao": 480
            },
            "valor": {
                "original": valor
            },
            "chave": self.key,
            "devedor": {}
        }

        data = requests.post(url, headers=headers, data=json.dumps(payload)).json()

        return Pix(data["id"],
                   "Alios",
                   data["location"],
                   valor,
                   data["location"],
                   f"https://apiendpointhml.ailos.coop.br/qa/ailos/pix-cobranca/api/v1/cob/{data['txid']}")

    def is_done(self):
        headers = {
            "x-ailos-authentication": self.access_token
        }

        response = requests.get(self.pix.url, headers=headers)

        if response.status_code == 200:
            cobranca = response.json()
            self.status = cobranca["status"]

        return self.status != "CONCLUIDA"
