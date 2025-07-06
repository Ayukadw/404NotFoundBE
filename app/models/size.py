from app.extensions import db

class Size(db.Model):
    __tablename__ = 'sizes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Relationships
    costumes = db.relationship('CostumeSize', back_populates='size')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
