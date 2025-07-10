from flask import request, jsonify
from app.models.order import Order
from app.models.costume import Costume
from app.models.user import User
from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.models.costume_size import CostumeSize
from app.extensions import db
from datetime import datetime, date
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
            payment_status=data['payment_status'],
            deposit=data.get('deposit', 300000)
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

        # Hitung total harga item (tanpa deposit)
        days = (return_date - rental_date).days
        if days < 1:
            raise Exception("Tanggal kembali harus setelah tanggal sewa.")
        price_per_day = data.get('price_per_day', 0)
        quantity = int(data['quantity'])
        # Ambil total harga item dari frontend jika dikirim, jika tidak hitung manual
        total_item_price = data.get('price_snapshot') or (price_per_day * quantity * days)

        # 3. Tambahkan OrderItem
        order_item = OrderItem(
            order_id=new_order.id,
            costume_id=costume_id,
            size_id=size_id,
            quantity=quantity,
            price_snapshot=total_item_price  # total harga item
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

    # Jika status diubah menjadi cancelled, kembalikan stok
    if data['status'] == "cancelled" and order.status != "cancelled":
        for item in order.order_items:
            costume_size = CostumeSize.query.filter_by(
                costume_id=item.costume_id,
                size_id=item.size_id
            ).first()
            if costume_size:
                costume_size.stock += item.quantity
                db.session.add(costume_size)
                update_costume_stock(costume_size.costume_id)
    
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

def return_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status == "returned":
        return jsonify({'error': 'Order already returned'}), 400

    data = request.get_json() or {}
    # data['damage_levels'] = [{item_id: 1, damage_level: "none|berat|minim"}, ...]
    damage_levels = data.get('damage_levels', [])

    # Update damage_level per item
    for item in order.order_items:
        dl = next((d['damage_level'] for d in damage_levels if d['item_id'] == item.id), None)
        if dl is not None:
            item.damage_level = dl
            db.session.add(item)  # Pastikan perubahan damage_level tersimpan

    today = date.today()
    order.actual_return_date = today
    late_days = (today - order.return_date).days
    late_fee = 0
    if late_days > 0:
        order.is_late = True
        order.late_days = late_days
        # Denda hari pertama: 25% harga per hari * quantity semua item
        # Denda hari kedua dst: 50% harga per hari * quantity * (late_days - 1)
        first_day_fine = 0
        next_days_fine = 0
        for item in order.order_items:
            price_per_day = item.costume.price_per_day if item.costume else 0
            qty = item.quantity
            first_day_fine += 0.25 * price_per_day * qty
            if late_days > 1:
                next_days_fine += 0.5 * price_per_day * qty * (late_days - 1)
        late_fee = first_day_fine + next_days_fine
        order.late_fee = late_fee
    else:
        order.is_late = False
        order.late_days = 0
        order.late_fee = 0.0

    # Hitung potongan deposit karena kerusakan per unit
    total_deposit = 0
    damage_cut = 0
    for item in order.order_items:
        deposit_per_unit = (item.costume.price_per_day if item.costume else 0) * 0.5
        damage_levels = (item.damage_level or "").split("|")
        for damage in damage_levels:
            if damage == "none":
                cut = 0
            elif damage == "minim":
                cut = 0.1 * deposit_per_unit
            elif damage == "sedang":
                cut = 0.5 * deposit_per_unit
            elif damage == "berat":
                cut = 1.0 * deposit_per_unit
            else:
                cut = 0
            damage_cut += cut
        total_deposit += deposit_per_unit * item.quantity

    # Denda keterlambatan sudah dihitung sebelumnya: late_fee
    # Potongan deposit maksimal hanya sampai deposit
    total_cut = min(total_deposit, damage_cut + late_fee)
    order.deposit_returned = max(0, total_deposit - total_cut)

    # Sisa denda yang belum tertutupi deposit
    uncovered_late_fee = max(0, (damage_cut + late_fee) - total_deposit)
    order.uncovered_late_fee = uncovered_late_fee

    # Gabungkan semua damage_level dari order_items ke order.damage_level
    damage_level_summary = []
    for item in order.order_items:
        if item.damage_level:
            label = f"{item.costume.name if item.costume else 'Item'}: {item.damage_level}"
            damage_level_summary.append(label)
    order.damage_level = ", ".join(damage_level_summary) if damage_level_summary else None
    db.session.add(order)

    # Kembalikan stok
    for item in order.order_items:
        costume_size = CostumeSize.query.filter_by(
            costume_id=item.costume_id,
            size_id=item.size_id
        ).first()
        if costume_size:
            costume_size.stock += item.quantity
            db.session.add(costume_size)
            update_costume_stock(costume_size.costume_id)
    order.status = "returned"
    db.session.commit()
    return jsonify({'message': 'Order returned and stock updated.', 'uncovered_late_fee': uncovered_late_fee})
