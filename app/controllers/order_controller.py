from flask import request, jsonify
from app.models.order import Order
from app.models.costume import Costume
from app.models.user import User
from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.models.costume_size import CostumeSize
from app.extensions import db
from datetime import datetime
from app.controllers.costume_controller import update_costume_stock

def get_all_orders():
    orders = Order.query.all()
    return jsonify([o.to_dict() for o in orders])

def create_order():
    data = request.get_json()

    required_fields = [
        'user_id', 'rental_date', 'return_date', 'address',
        'status', 'payment_status', 'costume_id', 'size', 'quantity', 'payment_method'
    ]
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        rental_date = datetime.strptime(data['rental_date'], "%Y-%m-%d").date()
        return_date = datetime.strptime(data['return_date'], "%Y-%m-%d").date()
        quantity = int(data['quantity'])
        costume_id = int(data['costume_id'])
        size_id = int(data['size'])
        price_per_day = data.get('price_per_day', 0)
        payment_method = data.get('payment_method')

        if (return_date - rental_date).days < 1:
            raise Exception("Tanggal kembali harus setelah tanggal sewa.")

        # 1. Buat Order
        new_order = Order(
            user_id=data['user_id'],
            rental_date=rental_date,
            return_date=return_date,
            address=data['address'],
            status=data['status'],
            payment_status=data['payment_status']
        )
        db.session.add(new_order)
        db.session.flush()  # agar bisa akses new_order.id

        # 2. Cek dan kurangi stok
        costume_size = CostumeSize.query.filter_by(
            costume_id=costume_id,
            size_id=size_id
        ).first()

        if not costume_size:
            raise Exception("Ukuran kostum tidak ditemukan")

        if costume_size.stock < quantity:
            raise Exception(f"Stok tidak cukup (tersedia: {costume_size.stock})")

        costume_size.stock -= quantity
        db.session.add(costume_size)

        # Update stok costume utama
        update_costume_stock(costume_size.costume_id)

        # 3. Tambahkan OrderItem
        days = (return_date - rental_date).days
        total_price = price_per_day * quantity * days

        order_item = OrderItem(
            order_id=new_order.id,
            costume_id=costume_id,
            size_id=size_id,
            quantity=quantity,
            price_snapshot=total_price
        )
        db.session.add(order_item)

        # 4. Tambahkan Payment
        payment = Payment(
            order_id=new_order.id,
            payment_method=payment_method,
            status="unpaid",
            proof_image="",  # Belum ada bukti
            submitted_at=datetime.utcnow()
        )
        db.session.add(payment)

        # 5. Commit semua
        db.session.commit()

        return jsonify(new_order.to_dict()), 201

    except Exception as e:
        import traceback
        print("ERROR SAAT CREATE ORDER:")
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_order_by_id(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_dict())

def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    for key in ['rental_date', 'return_date', 'address', 'status', 'payment_status']:
        if key in data:
            setattr(order, key, data[key])
    db.session.commit()
    return jsonify(order.to_dict())

def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    
    if 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
    
    order.status = data['status']
    db.session.commit()
    return jsonify(order.to_dict())

def update_order_payment_status(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    
    if 'payment_status' not in data:
        return jsonify({'error': 'Payment status is required'}), 400
    
    order.payment_status = data['payment_status']
    
    # Update payment status juga jika ada payment record
    if order.payment:
        order.payment.status = data['payment_status']
    
    db.session.commit()
    return jsonify(order.to_dict())

def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted'})

def get_orders_by_user(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([o.to_dict() for o in orders])
