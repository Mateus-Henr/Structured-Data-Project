import os
from fpdf import FPDF
from PIL import Image

QR_PDF = "QRCODE.pdf"


def create_qrcode_pdf(pix):
    pdf = FPDF()

    # Adicionar uma nova página
    pdf.add_page()
    qrcode_image = Image.open(pix.generate_jpg_from_qr_code64())

    temp_file_path = "qrcode.png"
    qrcode_image.save(temp_file_path, format="PNG")
    pdf.set_font("Arial", "B", 50)
    pdf.cell(0, 10, "PIX CODIGO QR".format(float(pix.value)), ln=True, align="C")
    pdf.image(temp_file_path, x=10, y=10, w=200, h=200)
    os.remove(temp_file_path)
    pdf.set_font("Arial", "B", 25)
    pdf.set_y(220)
    pdf.cell(0, 10, "Data: {}".format(pix.date), ln=True, align="C")

    # Salvar o self.pdf no arquivo especificado
    pdf.output(QR_PDF)


def create_payment_validation_code(pix, bank):

    pdf = FPDF()
    # Adicionar uma nova página
    pdf.add_page()
    pdf.set_font("Arial", "B", 25)
    pdf.cell(0, 10, "PAGAMENTO APROVADO: ", ln=True, align="C")
    pdf.cell(0, 10, "ID: {}".format(pix.id), ln=True, align="C")
    pdf.cell(0, 10, "Data: {}".format(pix.date), ln=True, align="C")
    pdf.cell(0, 10, "Valor: R${:.2f}".format(float(pix.value)), ln=True, align="C")
    pdf.cell(0, 10, "Emissor: {}".format(bank), ln=True, align="C")
    pdf.output(QR_PDF)
