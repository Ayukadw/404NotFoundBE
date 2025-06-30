from flask import request, jsonify
from app.models.costume import Costume
from app.extensions import db

def get_all_costumes():
    costumes = Costume.query.all()
    return jsonify([c.__dict__ for c in costumes])

def create_costume():
    data = request.get_json()
    required_fields = ['name', 'description', 'category_id', 'size_id', 'price_per_day', 'stock', 'status']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    costume = Costume(
        name=data['name'],
        description=data['description'],
        category_id=data['category_id'],
        size_id=data['size_id'],
        price_per_day=data['price_per_day'],
        stock=data['stock'],
        image_url=data.get('image_url'),
        status=data['status']
    )
    db.session.add(costume)
    db.session.commit()
    return jsonify(costume.__dict__), 201

def get_costume_by_id(costume_id):
    costume = Costume.query.get_or_404(costume_id)
    return jsonify(costume.__dict__)

def update_costume(costume_id):
    costume = Costume.query.get_or_404(costume_id)
    data = request.get_json()
    for key in ['name', 'description', 'category_id', 'size_id', 'price_per_day', 'stock', 'image_url', 'status']:
        if key in data:
            setattr(costume, key, data[key])
    db.session.commit()
    return jsonify(costume.__dict__)

def delete_costume(costume_id):
    costume = Costume.query.get_or_404(costume_id)
    db.session.delete(costume)
    db.session.commit()
    return jsonify({'message': 'Costume deleted'})
