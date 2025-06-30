from app.extensions import db

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    costume_id = db.Column(db.Integer, db.ForeignKey('costumes.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_snapshot = db.Column(db.Float, nullable=False)

    # Relationships
    order = db.relationship('Order', back_populates='order_items')
    costume = db.relationship('Costume', back_populates='order_items')
