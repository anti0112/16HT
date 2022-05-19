from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from utils import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///:memory:'
app.config["JSON_AS_ASCII"] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)


class Offer(db.Model):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    users = db.relationship("User")
    orders = db.relationship("Order")


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    customer = db.relationship("User", backref='order_io', foreign_keys=customer_id)
    executor = db.relationship("User", backref='order_ir', foreign_keys=executor_id)


db.drop_all()
db.create_all()

users = load_json("json_file/user.json")
offers = load_json("json_file/offer.json")
orders = load_json('json_file/order.json')

with db.session.begin():
    for user in users:
        db.session.add(User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone']
        ))

    for order in orders:
        db.session.add(Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=order['start_date'],
            end_date=order['end_date'],
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id']
        ))

    for offer in offers:
        db.session.add(Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        ))


@app.route('/users/', methods=['GET', 'POST'])
def get():
    if request.method == 'GET':
        response = []

        for user in db.session.query(User).all():
            response.append(response_user(user))
        return jsonify(response)

    elif request.method == 'POST':
        user = request.json
        new_user = User(
            id=user.get('id'),
            first_name=user.get('first_name'),
            last_name=user.get('last_name'),
            age=user.get('age'),
            email=user.get('email'),
            role=user.get('role'),
            phone=user.get('phone')
        )
        with db.session.begin():
            db.session.add(new_user)
            return 'Данные успешно добавлены', 200


@app.route("/users/<int:uid>", methods=["GET", "PUT", "DELETE"])
def get_user(uid):
    user = db.session.query(User).get(uid)

    if request.method == 'GET':
        return jsonify(response_user(user))

    elif request.method == 'PUT':

        data = request.get_json()
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.age = data['age']
        user.email = data['email']
        user.role = data['role']
        user.phone = data['phone']
        db.session.add(user)
        db.session.commit()
        return 'Данные обновлены', 201

    elif request.method == 'DELETE':

        db.session.delete(user)
        db.session.commit()

        return "Пользователь удален", 204


@app.route('/orders/', methods=['GET', 'POST'])
def get_orders():
    if request.method == 'GET':
        response = []

        for order in db.session.query(Order).all():
            response.append(response_order(order))
        return jsonify(response)

    elif request.method == 'POST':
        order = request.json
        new_order = Order(
            id=order.get('id'),
            name=order.get('name'),
            description=order.get('description'),
            start_date=order.get('start_date'),
            end_date=order.get('end_date'),
            address=order.get('address'),
            price=order.get('price'),
            customer_id=order.get('customer_id'),
            executor_id=order.get('executor_id')
        )
        with db.session.begin():
            db.session.add(new_order)
            return 'Данные успешно добавлены', 200


@app.route('/orders/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def get_order(uid):
    order = db.session.query(Order).get(uid)
    if request.method == 'GET':
        return jsonify(response_order(order))

    elif request.method == 'PUT':
        data_orders = request.get_json()
        order.name = data_orders['name']
        order.description = data_orders['description']
        order.start_date = data_orders['start_date']
        order.end_date = data_orders['end_date']
        order.address = data_orders['address']
        order.price = data_orders['price']
        order.customer_id = data_orders['customer_id']
        order.executor_id = data_orders['executor_id']

        db.session.add(order)
        db.session.commit()
        return 'Данные обновлены', 201

    elif request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return 'Успешно удалено', 204


@app.route('/offers/', methods=['GET', 'POST'])
def get_offers():
    if request.method == 'GET':
        response = []

        for offer in db.session.query(Offer).all():
            response.append(response_offer(offer))
        return jsonify(response)

    elif request.method == 'POST':
        offer = request.json
        new_offer = Offer(
            id=offer.get('id'),
            order_id=offer.get('order_id'),
            executor_id=offer.get('executor_id')
        )
        with db.session.begin():
            db.session.add(new_offer)
        return 'Данные успешно добавлены', 200


@app.route('/offers/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def offer(uid):
    offer = db.session.query(Offer).get(uid)

    if request.method == 'GET':
        return jsonify(response_offer(offer))

    elif request.method == 'PUT':
        data_offers = request.get_json()
        offer.order_id = data_offers['order_id']
        offer.executor_id = data_offers['executor_id']

        db.session.add(offer)
        db.session.commit()
        return 'Данные обновлены', 201

    elif request.method == 'DELETE':
        db.session.delete(offer)
        db.session.commit()
        return 'Данные успешно удалены', 204


app.run(debug=True)






