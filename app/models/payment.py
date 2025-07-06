from app.extensions import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    payment_method = db.Column(db.String(100), nullable=False)
    proof_image = db.Column(db.String(512), nullable=True)
    status = db.Column(db.String(50), nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=True)
    verified_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    order = db.relationship('Order', back_populates='payment', uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'payment_method': self.payment_method,
            'proof_image': self.proof_image,
            'status': self.status,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None
        }
