from app.extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rental_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    address = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    actual_return_date = db.Column(db.Date, nullable=True)
    is_late = db.Column(db.Boolean, default=False)
    late_days = db.Column(db.Integer, default=0)
    late_fee = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    order_items = db.relationship('OrderItem', back_populates='order', lazy=True)
    payment = db.relationship('Payment', back_populates='order', uselist=False)
    user = db.relationship("User", back_populates="orders")

    def to_dict(self):
        order_items = [item.to_dict() for item in self.order_items]
        total_price = sum(item['total_price'] for item in order_items)
        payment_method = self.payment.payment_method if self.payment else None
        payment_status = self.payment.status if self.payment else self.payment_status
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'user_email': self.user.email if self.user else None,
            'rental_date': self.rental_date.isoformat() if self.rental_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'actual_return_date': self.actual_return_date.isoformat() if self.actual_return_date else None,
            'is_late': self.is_late,
            'late_days': self.late_days,
            'late_fee': self.late_fee,
            'address': self.address,
            'status': self.status,
            'payment_status': payment_status,
            'order_items': order_items,
            'total_price': total_price,
            'payment_method': payment_method,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'payment': self.payment.to_dict() if self.payment else None
        }
