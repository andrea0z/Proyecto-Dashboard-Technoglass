from .db import db

class KPI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    team = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<KPI {self.name}: {self.value}>'