from flask import request, jsonify
from app.models.costume import Costume
from app.models.costume_size import CostumeSize
from app.extensions import db

def get_all_costumes():
    costumes = Costume.query.all()
    return jsonify([c.to_dict() for c in costumes])

def create_costume():
    data = request.get_json()

    required_fields = ['name', 'category_id', 'price_per_day', 'stock', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    costume = Costume(
        name=data['name'],
        description=data.get('description'),
        category_id=data['category_id'],
        price_per_day=data['price_per_day'],
        stock=data['stock'],
        image_url=data.get('image_url'),
        status=data['status']
    )

    db.session.add(costume)
    db.session.commit()

    # Simpan sizes[] ke CostumeSize
    sizes_data = data.get('sizes', [])
    for s in sizes_data:
        cs = CostumeSize(
            costume_id=costume.id,
            size_id=s['size_id'],
            stock=s['stock']
        )
        db.session.add(cs)

    db.session.commit()

    # Perbarui stock costume utama berdasarkan semua ukuran
    update_costume_stock(costume.id)

    return jsonify(costume.to_dict()), 201


def get_costume_by_id(costume_id):
    costume = Costume.query.get_or_404(costume_id)
    return jsonify(costume.to_dict())

def update_costume(costume_id):
    costume = Costume.query.get_or_404(costume_id)
    data = request.get_json()
    
    # Update costume fields
    for key in ['name', 'description', 'category_id', 'price_per_day', 'image_url', 'status']:
        if key in data:
            setattr(costume, key, data[key])
    
    db.session.commit()

    # Now update sizes and stock
    if 'sizes' in data:
        sizes_data = data['sizes']  # This should be an array of {size_id, stock} objects
        for size_data in sizes_data:
            costume_size = CostumeSize.query.filter_by(costume_id=costume.id, size_id=size_data['size_id']).first()
            if costume_size:
                costume_size.stock = size_data['stock']  # Update stock
            else:
                # If the costume size doesn't exist, create a new one
                new_costume_size = CostumeSize(
                    costume_id=costume.id,
                    size_id=size_data['size_id'],
                    stock=size_data['stock']
                )
                db.session.add(new_costume_size)

            db.session.commit()
    update_costume_stock(costume.id)

    return jsonify(costume.to_dict())



def delete_costume(costume_id):
    costume = Costume.query.get_or_404(costume_id)
    
    # Delete related costume sizes first
    CostumeSize.query.filter_by(costume_id=costume.id).delete()
    
    db.session.delete(costume)
    db.session.commit()
    
    return jsonify({'message': 'Costume deleted'})

def update_costume_stock(costume_id):
    costume = Costume.query.get(costume_id)
    if costume:
        total_stock = sum(size.stock for size in costume.sizes)
        costume.stock = total_stock
        db.session.commit()
