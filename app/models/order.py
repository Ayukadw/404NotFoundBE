from app.extensions import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rental_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    address = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)

    # Relationships
    order_items = db.relationship('OrderItem', back_populates='order', lazy=True)
    payment = db.relationship('Payment', back_populates='order', uselist=False)
    user = db.relationship("User", back_populates="orders")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'rental_date': self.rental_date.isoformat() if self.rental_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'address': self.address,
            'status': self.status,
            'payment_status': self.payment_status
        }
