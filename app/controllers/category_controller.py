from flask import request, jsonify
from app.models.category import Category
from app.extensions import db

def get_all_categories():
    categories = Category.query.all()
    return jsonify([c.__dict__ for c in categories])

def create_category():
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': 'Category name is required'}), 400

    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    return jsonify(category.__dict__), 201

def get_category_by_id(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify(category.__dict__)

def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    if 'name' in data:
        category.name = data['name']
    db.session.commit()
    return jsonify(category.__dict__)

def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted'})
