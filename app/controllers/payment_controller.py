from flask import request, jsonify
from app.models.payment import Payment
from app.extensions import db

def get_all_payments():
    payments = Payment.query.all()
    return jsonify([p.__dict__ for p in payments])

def create_payment():
    data = request.get_json()
    required_fields = ['order_id', 'payment_method', 'proof_image', 'status']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    payment = Payment(
        order_id=data['order_id'],
        payment_method=data['payment_method'],
        proof_image=data['proof_image'],
        status=data['status'],
        submitted_at=data.get('submitted_at'),
        verified_at=data.get('verified_at')
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify(payment.__dict__), 201

def get_payment_by_id(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return jsonify(payment.__dict__)

def update_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    data = request.get_json()
    for key in ['payment_method', 'proof_image', 'status', 'submitted_at', 'verified_at']:
        if key in data:
            setattr(payment, key, data[key])
    db.session.commit()
    return jsonify(payment.__dict__)

def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return jsonify({'message': 'Payment deleted'})
