from flask import request, jsonify, send_from_directory
from app.models.payment import Payment
from app.models.order import Order
from app.extensions import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import base64

UPLOAD_FOLDER = 'static/uploads'  # Pastikan folder ini ada

def get_all_payments():
    payments = Payment.query.all()
    return jsonify([p.to_dict() for p in payments])

def serve_payment_proof(filename):
    """Serve payment proof image"""
    try:
        # Pastikan path absolut ke folder uploads
        upload_folder = os.path.join(os.getcwd(), 'static', 'uploads')
        print(f"Serving file: {filename} from folder: {upload_folder}")
        print(f"File exists: {os.path.exists(os.path.join(upload_folder, filename))}")
        return send_from_directory(upload_folder, filename)
    except Exception as e:
        print(f"Error serving file {filename}: {e}")
        return jsonify({'error': f'File not found: {filename}'}), 404

def serve_payment_proof_base64(filename):
    """Serve payment proof image as base64"""
    try:
        upload_folder = os.path.join(os.getcwd(), 'static', 'uploads')
        file_path = os.path.join(upload_folder, filename)
        
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                image_data = f.read()
                base64_data = base64.b64encode(image_data).decode('utf-8')
                return jsonify({
                    'filename': filename,
                    'data': base64_data,
                    'mime_type': 'image/png' if filename.endswith('.png') else 'image/jpeg'
                })
        else:
            return jsonify({'error': f'File not found: {filename}'}), 404
    except Exception as e:
        print(f"Error serving base64 file {filename}: {e}")
        return jsonify({'error': f'File not found: {filename}'}), 404

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
        relative_path = os.path.relpath(save_path, start='.')
        relative_path = relative_path.replace('\\', '/')  # Pastikan selalu pakai slash

        # Validasi order
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # Cek apakah sudah ada payment untuk order ini
        existing_payment = Payment.query.filter_by(order_id=order_id).first()
        
        if existing_payment:
            # Update payment yang sudah ada
            existing_payment.payment_method = payment_method
            existing_payment.proof_image = relative_path
            existing_payment.status = 'pending'  # Set ke pending saat bukti dikirim
            existing_payment.submitted_at = submitted_at
            existing_payment.verified_at = None
            payment = existing_payment
        else:
            # Buat Payment record baru
            payment = Payment(
                order_id=order_id,
                payment_method=payment_method,
                proof_image=relative_path,
                status='pending',  # Set ke pending saat bukti dikirim
                submitted_at=submitted_at,
                verified_at=None
            )
            db.session.add(payment)

        # Update status pembayaran di Order menjadi 'pending'
        order.payment_status = 'pending'
        db.session.add(order)

        db.session.commit()
        
        # Return order yang sudah diupdate
        return jsonify({
            'payment': payment.to_dict(),
            'order': order.to_dict(),
            'message': 'Bukti pembayaran berhasil diunggah dan status diupdate menjadi pending'
        }), 201

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
