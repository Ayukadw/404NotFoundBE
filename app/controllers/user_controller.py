from flask import request, jsonify
from app.models.user import User
from app.extensions import db, bcrypt

def get_all_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

def get_user_by_id(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

def create_user():
    data = request.get_json()
    required_fields = ['name', 'email', 'password_hash', 'phone']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Hash the password before saving
    hashed_password = bcrypt.generate_password_hash(data['password_hash']).decode('utf-8')

    new_user = User(
        name=data['name'],
        email=data['email'],
        password_hash=hashed_password,
        phone=data['phone'],
        role=data.get('role', 'user')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    for key in ['name', 'email', 'password_hash', 'phone', 'role']:
        if key in data:
            setattr(user, key, data[key])
    db.session.commit()
    return jsonify(user.to_dict())

def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})
