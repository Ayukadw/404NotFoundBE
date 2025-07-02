from app.extensions import db

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    costume_id = db.Column(db.Integer, db.ForeignKey('costumes.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_snapshot = db.Column(db.Float, nullable=False)

    order = db.relationship('Order', back_populates='order_items')
    costumes = db.relationship('Costume', back_populates='order_items')
    size = db.relationship('Size')  # ini tambahan penting

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'costume_id': self.costume_id,
            'size_id': self.size_id,
            'quantity': self.quantity,
            'price_snapshot': self.price_snapshot
        }
