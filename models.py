from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class RequestRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numbers = db.Column(db.String(255), nullable=False)
    result = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
