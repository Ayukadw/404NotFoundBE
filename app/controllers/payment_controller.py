from flask import request, jsonify
from app.models.payment import Payment
from app.models.order import Order
from app.extensions import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'  # Pastikan folder ini ada

def get_all_payments():
    payments = Payment.query.all()
    return jsonify([p.to_dict() for p in payments])

def create_payment():
    try:
        order_id = request.form.get('order_id')
        payment_method = request.form.get('payment_method')
        status = request.form.get('status', 'pending')
        submitted_at = datetime.utcnow()

        if not order_id or not payment_method:
            return jsonify({'error': 'order_id and payment_method are required'}), 400

        file = request.files.get('proof_image')
        if not file:
            return jsonify({'error': 'Proof image is required'}), 400

        # Pastikan folder upload tersedia
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

        # Simpan path relatif
        relative_path = os.path.relpath(save_path, start='.')  # or your app root

        # Validasi order
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # Buat Payment record
        payment = Payment(
            order_id=order_id,
            payment_method=payment_method,
            proof_image=relative_path,
            status=status,
            submitted_at=submitted_at,
            verified_at=None
        )
        db.session.add(payment)

        # Update status pembayaran di Order
        order.payment_status = 'waiting_verification'
        db.session.add(order)

        db.session.commit()
        return jsonify(payment.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        print("ERROR CREATE PAYMENT:", e)
        return jsonify({'error': str(e)}), 500

def get_payment_by_id(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return jsonify(payment.to_dict())

def update_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    data = request.get_json()
    for key in ['payment_method', 'proof_image', 'status', 'submitted_at', 'verified_at']:
        if key in data:
            setattr(payment, key, data[key])
    db.session.commit()
    return jsonify(payment.to_dict())

def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return jsonify({'message': 'Payment deleted'})

def verify_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    payment.status = 'verified'
    payment.verified_at = datetime.utcnow()

    # Ubah status order juga
    order = payment.order
    order.payment_status = 'paid'

    db.session.commit()
    return jsonify({'message': 'Payment verified and order status updated.'})
