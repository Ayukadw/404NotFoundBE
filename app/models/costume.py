from app.extensions import db

class Costume(db.Model):
    __tablename__ = 'costumes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'), nullable=False)
    price_per_day = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(512), nullable=True)
    status = db.Column(db.String(50), nullable=False)

    # Relationships
    category = db.relationship('Category', back_populates='costumes')
    size = db.relationship('Size', back_populates='costumes')
    order_items = db.relationship('OrderItem', back_populates='costume')
