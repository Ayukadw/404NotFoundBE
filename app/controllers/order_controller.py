from flask import request, jsonify
from app.models.order import Order
from app.models.costume import Costume
from app.models.user import User
from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.extensions import db
from datetime import datetime

def get_all_orders():
    orders = Order.query.all()
    return jsonify([o.to_dict() for o in orders])

from app.models.costume_size import CostumeSize  # Tambahkan ini di bagian import

def create_order():
    data = request.get_json()
    required_fields = [
        'user_id', 'rental_date', 'return_date', 'address',
        'status', 'payment_status', 'costume_id', 'size', 'quantity'
    ]
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        rental_date = datetime.strptime(data['rental_date'], "%Y-%m-%d").date()
        return_date = datetime.strptime(data['return_date'], "%Y-%m-%d").date()

        # 1. Simpan order
        new_order = Order(
            user_id=data['user_id'],
            rental_date=rental_date,
            return_date=return_date,
            address=data['address'],
            status=data['status'],
            payment_status=data['payment_status']
        )
        db.session.add(new_order)
        db.session.flush()  # agar new_order.id tersedia

        # 2. Simpan ke OrderItem
        quantity = int(data['quantity'])  # Ubah jadi integer

        new_order_item = OrderItem(
            order_id=new_order.id,
            costume_id=data['costume_id'],
            size_id=data['size'],  # pastikan ini adalah ID
            quantity =quantity,  # Ubah jadi integer
            price_snapshot=data.get('price_snapshot', 0)  # opsional
        )
        db.session.add(new_order_item)

        # 3. Update stok dari CostumeSize
        costume_size = CostumeSize.query.filter_by(
            costume_id=data['costume_id'],
            size_id=data['size']
        ).first()

        if costume_size is None:
            raise Exception("Kombinasi costume dan size tidak ditemukan")

        if costume_size.stock < quantity:
            raise Exception("Stok tidak mencukupi")

        print(f"Stok sebelum: {costume_size.stock}")

        costume_size.stock -= quantity
        db.session.add(costume_size)
        print(f"Stok dikurangi: {quantity}")
        db.session.commit()
        
        print(f"Stok sesudah: {costume_size.stock}")
        return jsonify(new_order.to_dict()), 201

    except Exception as e:
        import traceback
        print("ERROR SAAT CREATE ORDER:")
        traceback.print_exc()  # Ini akan cetak stack trace ke terminal
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

def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted'})
