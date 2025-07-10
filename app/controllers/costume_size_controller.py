from flask import request, jsonify
from app.models.costume_size import CostumeSize
from app.extensions import db

def get_all_costume_sizes():
    data = [cs.to_dict() for cs in CostumeSize.query.all()]
    return jsonify(data)

def get_costume_size_by_id(id):
    cs = CostumeSize.query.get_or_404(id)
    return jsonify(cs.to_dict())

def create_costume_size():
    data = request.get_json()
    costume_id = data.get('costume_id')
    size_id = data.get('size_id')
    stock = data.get('stock', 0)
    if not costume_id or not size_id:
        return jsonify({'error': 'costume_id dan size_id wajib diisi'}), 400
    cs = CostumeSize(costume_id=costume_id, size_id=size_id, stock=stock)
    db.session.add(cs)
    db.session.commit()
    return jsonify(cs.to_dict()), 201

def update_costume_size(id):
    cs = CostumeSize.query.get_or_404(id)
    data = request.get_json()
    cs.costume_id = data.get('costume_id', cs.costume_id)
    cs.size_id = data.get('size_id', cs.size_id)
    cs.stock = data.get('stock', cs.stock)
    db.session.commit()
    return jsonify(cs.to_dict())

def delete_costume_size(id):
    cs = CostumeSize.query.get_or_404(id)
    db.session.delete(cs)
    db.session.commit()
    return jsonify({'message': 'Costume size dihapus'}) 