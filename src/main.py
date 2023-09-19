import io
import os
from tempfile import NamedTemporaryFile

from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, send_file

from controller.mercado_pago import PixMercadoPago
from db.bank_dao import BankDAO
from db.product_dao import ProductDAO
from model.pdf import create_qrcode_pdf

app = Flask(__name__, template_folder="templates")
app.config['STATIC_URL_PATH'] = '/static'

products = []


# bank = BankDAO.get_bank()


@app.route('/')
def initial_page():
    return render_template("index.html")


@app.route('/finished')
def finished_page():
    return render_template("finished.html")


@app.route('/price')
def price_page():
    return render_template("price.html")


@app.route('/qrcode')
def qrcode_page():
    return render_template("qrcode.html")


@app.route('/submit-info', methods=['POST'])
def submit_info():
    if request.method == 'POST':
        key = request.form.get("api_key")
        bank_name = request.form.get("bank_name")
        bank = BankDAO.update_or_create_bank(bank_name, key)

        try:
            PixMercadoPago(1, bank)
        except Exception as e:
            print(e)
            return redirect(url_for("initial_page"))

        return render_template("price.html", products=products)


@app.route('/insert-product', methods=['POST'])
def insert_product():
    if request.method == 'POST':
        product = ProductDAO.get_produto_by_id(int(request.form.get("product_id")))

        if product is not None:
            quantity = int(request.form.get("quantity"))

            if quantity > product.inventory:
                print("ERRO: Sem estoque")
                return redirect(url_for("price_page"))

            for prod in products:
                if prod["product"].id == product.id:
                    if prod["quantity"] + quantity > product.inventory:
                        print("ERRO")
                        return redirect(url_for("price_page"))

                    prod["quantity"] += quantity
                    return render_template("price.html", products=products)

            products.append({"product": product, "quantity": quantity})

        return render_template("price.html", products=products)


@app.route('/buy', methods=['POST'])
def buy_products():
    if request.method == 'POST':
        # TODO: Create a function to decrease the inventory quantity
        total_price = sum(product["product"].value * product["quantity"] for product in products)

        pix = PixMercadoPago(total_price, BankDAO.get_bank()).pix

        if pix is None:
            return redirect(url_for("initial_page"))

        with open(os.path.dirname(__file__) + "/static/images/image.jpg", "wb") as image_file:
            image_file.write(pix.generate_jpg_from_qr_code64())

        return render_template("qrcode.html")


app.run()
