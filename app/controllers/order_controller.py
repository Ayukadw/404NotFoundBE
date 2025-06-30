from flask import request, jsonify
from app.models.order import Order
from app.models.user import User
from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.extensions import db

def get_all_orders():
    orders = Order.query.all()
    return jsonify([o.__dict__ for o in orders])

def create_order():
    data = request.get_json()
    required_fields = ['user_id', 'rental_date', 'return_date', 'address', 'status', 'payment_status']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_order = Order(
        user_id=data['user_id'],
        rental_date=data['rental_date'],
        return_date=data['return_date'],
        address=data['address'],
        status=data['status'],
        payment_status=data['payment_status']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify(new_order.__dict__), 201

def get_order_by_id(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order.__dict__)

def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    for key in ['rental_date', 'return_date', 'address', 'status', 'payment_status']:
        if key in data:
            setattr(order, key, data[key])
    db.session.commit()
    return jsonify(order.__dict__)

def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted'})
