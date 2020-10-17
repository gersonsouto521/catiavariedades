from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db


class EntregaProdutos(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(120))
    delivery_content = db.Column(db.String(255))
    def __init__(self, date, delivery_content):
        self.date = date
        self.delivery_content = delivery_content


class EstoqueProduto(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    img = db.Column(db.String(350))
    sku = db.Column(db.String(7))
    product_name = db.Column(db.String(100))
    amount_current = db.Column(db.Integer)
    price_buy = db.Column(db.Float)
    price_sell = db.Column(db.Float)
    provider_supplies = db.Column(db.String(50))
    product_type = db.Column(db.String(50))
    amount_catia = db.Column(db.Integer)
    amount_gerson = db.Column(db.Integer)
    def __init__(self, img, sku, product_name, amount_current, price_buy, price_sell, provider_supplies, product_type, amount_catia, amount_gerson):
        self.img = img
        self.sku = sku
        self.product_name = product_name
        self.amount_current = amount_current
        self.price_buy =  price_buy
        self.price_sell =  price_sell
        self.provider_supplies =  provider_supplies
        self.product_type = product_type
        self.amount_catia = amount_catia
        self.amount_gerson = amount_gerson 