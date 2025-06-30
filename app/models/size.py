from app.extensions import db

class Size(db.Model):
    __tablename__ = 'sizes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Relationships
    costumes = db.relationship('Costume', back_populates='size', lazy=True)
