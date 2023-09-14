import io

from flask import Flask, render_template, request, redirect, url_for, send_file

from controller.mercado_pago import PixMercadoPago
from db.bank_dao import BankDAO
from db.product_dao import ProductDAO

app = Flask(__name__, template_folder="templates")
app.config['STATIC_URL_PATH'] = '/static'

products = []
bank = BankDAO.update_bank("MB", "", "MB")
print(bank.api_key)


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
        bank = BankDAO.update_bank(request.form.get("bank_name"), request.form.get("api_key"), "MB")
        return render_template("price.html")


@app.route('/insert-product', methods=['POST'])
def insert_product():
    if request.method == 'POST':
        product = ProductDAO.get_produto_by_id(int(request.form.get("product_id")))

        if product is not None:
            quantity = int(request.form.get("quantity"))

            if quantity > product.estoque:
                print("ERRO")
                return redirect(url_for("price_page"))

            products.append({"quantity": quantity, "product": product})
            print(products)
            return redirect(url_for("price_page"))

        print(products)
        return redirect(url_for("price_page"))


@app.route('/buy', methods=['POST'])
def buy_products():
    if request.method == 'POST':
        # TODO: Create a function to decrease the inventory quantity
        total_price = sum(product["product"].valor * product["quantity"] for product in products)

        pix = PixMercadoPago(total_price, bank).create_pix(total_price)

        return send_file(io.BytesIO(pix.generate_jpg_from_qr_code64()), mimetype='image/jpeg')

app.run()
