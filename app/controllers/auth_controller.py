from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from app.models.user import User
from app.extensions import db, bcrypt

def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email dan password wajib diisi'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Email atau password salah'}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
    }), 200

def register():
    data = request.get_json()
    required_fields = ['name', 'email', 'password', 'phone']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Field tidak lengkap'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email sudah terdaftar'}), 409

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(
        name=data['name'],
        email=data['email'],
        password_hash=hashed_password,
        phone=data['phone'],
        role=data.get('role', 'user')
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Register berhasil', 'user': user.email}), 201

@jwt_required()
def get_profile():
    try:
        print('Authorization Header:', request.headers.get('Authorization'))
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        })
    except Exception as e:
        print('JWT Error:', str(e))
        return jsonify({'error': 'Invalid or missing token', 'detail': str(e)}), 401
