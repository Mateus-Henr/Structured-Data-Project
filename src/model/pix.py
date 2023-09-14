import base64
from io import BytesIO


class Pix:
    def __init__(self, id: int, destination: str, date: str, value: float, qr_code_base64: str, url: str):
        self.id = id
        self.destination = destination
        self.date = date
        self.value = value
        self.qr_code_base64 = qr_code_base64
        self.url = url

    def generate_jpg_from_qr_code64(self):
        """
        Generates a JPEG image from the base64 encoded QR code.
        """
        return base64.b64decode(self.qr_code_base64)
