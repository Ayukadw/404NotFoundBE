from flask import request, jsonify
from app.models.order_item import OrderItem
from app.extensions import db

def get_all_order_items():
    items = OrderItem.query.all()
    return jsonify([i.to_dict() for i in items])

def create_order_item():
    data = request.get_json()
    required_fields = ['order_id', 'costume_id', 'quantity', 'price_snapshot']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    item = OrderItem(
        order_id=data['order_id'],
        costume_id=data['costume_id'],
        quantity=data['quantity'],
        price_snapshot=data['price_snapshot']
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

def get_order_item_by_id(item_id):
    item = OrderItem.query.get_or_404(item_id)
    return jsonify(item.to_dict())

def update_order_item(item_id):
    item = OrderItem.query.get_or_404(item_id)
    data = request.get_json()
    for key in ['order_id', 'costume_id', 'quantity', 'price_snapshot']:
        if key in data:
            setattr(item, key, data[key])
    db.session.commit()
    return jsonify(item.to_dict())

def delete_order_item(item_id):
    item = OrderItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'})
