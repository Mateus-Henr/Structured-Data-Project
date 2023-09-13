from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")
app.config['STATIC_URL_PATH'] = '/static'


@app.route('/')
def initial_page():
    return render_template("index.html")


@app.route('/concluido')
def concluido_page():
    return render_template("concluido.html")


@app.route('/price')
def price_page():
    return render_template("price.html")


@app.route('/qrcode')
def qrcode_page():
    return render_template("qrcode.html")


app.run()
