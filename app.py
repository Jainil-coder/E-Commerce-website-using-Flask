from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
from flask import session
import json
from json import JSONEncoder

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True

app = Flask(__name__)
app.secret_key = 'super-secret-key'
if(local_server):
        app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
        app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Contacts(db.Model):
    sr_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)

class Login(db.Model):
    sr_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(12), nullable=True)

class Payment(db.Model):
    sr_no = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    name_on_card = db.Column(db.String(50), nullable=False)
    credit_card_no = db.Column(db.String(50), nullable=False)
    expiration = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(12), nullable=True)


@app.route('/')
def home():
    return render_template('index.html', params=params)

@app.route('/')
def shopnow():
    return render_template('index.html', params=params)


@app.route("/products")
def products_route():
    #products = Products.query.filter_by(slug=products_slug).first()
     return render_template('products.html', params=params)


@app.route("/about")
def about():
    return render_template('about.html', params=params)


@app.route("/login", methods = ['GET', 'POST'])
def login():
     if(request.method=='POST'):

         name = request.form.get('name')
         email = request.form.get('email')
         password = request.form.get('password')

         entry = Login(name = name, email = email, password = password, date = datetime.now())
         db.session.add(entry)
         db.session.commit()
     return render_template('login.html', params=params)


@app.route("/contact", methods = ['GET', 'POST'])
def contact():
     if(request.method=='POST'):

         name = request.form.get('name')
         email = request.form.get('email')
         phone = request.form.get('phone_num')
         message = request.form.get('msg')

         entry = Contacts(name = name, email = email, phone_num = phone, msg = message, date = datetime.now())
         db.session.add(entry)
         db.session.commit()
     return render_template('contact.html', params=params)


@app.route("/cart")
def cart():
    return render_template('cart.html', params=params)


@app.route("/payment", methods = ['GET', 'POST'])
def payment():
    if(request.method=='POST'):

         firstname = request.form.get('firstname')
         lastname = request.form.get('lastname')
         email = request.form.get('email')
         address = request.form.get('address')
         cc_name = request.form.get('cc_name')
         cc_number = request.form.get('cc_number')
         cc_expiration = request.form.get('cc_expiration')
         password = request.form.get('password')

         entry = Payment(first_name = firstname, last_name = lastname, email = email, address = address, name_on_card = cc_name, credit_card_no = cc_number, expiration = cc_expiration, date = datetime.now())
         db.session.add(entry)
         db.session.commit()
    return render_template('payment.html', params=params)


app.run(debug=True)