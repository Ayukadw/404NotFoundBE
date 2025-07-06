from app.extensions import db

class CostumeSize(db.Model):
    __tablename__ = 'costume_sizes'

    id = db.Column(db.Integer, primary_key=True)
    costume_id = db.Column(db.Integer, db.ForeignKey('costumes.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    costumes = db.relationship('Costume', back_populates='sizes')
    size = db.relationship('Size', back_populates='costumes')

    def to_dict(self):
        return {
            'id': self.id,
            'costume_id': self.costume_id,
            'size_id': self.size_id,
            'stock': self.stock,
            'size': self.size.to_dict() if self.size else None
        }
