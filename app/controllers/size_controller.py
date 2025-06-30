from flask import request, jsonify
from app.models.size import Size
from app.extensions import db

def get_all_sizes():
    sizes = Size.query.all()
    return jsonify([s.__dict__ for s in sizes])

def create_size():
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': 'Size name is required'}), 400

    size = Size(name=data['name'])
    db.session.add(size)
    db.session.commit()
    return jsonify(size.__dict__), 201

def get_size_by_id(size_id):
    size = Size.query.get_or_404(size_id)
    return jsonify(size.__dict__)

def update_size(size_id):
    size = Size.query.get_or_404(size_id)
    data = request.get_json()
    if 'name' in data:
        size.name = data['name']
    db.session.commit()
    return jsonify(size.__dict__)

def delete_size(size_id):
    size = Size.query.get_or_404(size_id)
    db.session.delete(size)
    db.session.commit()
    return jsonify({'message': 'Size deleted'})
