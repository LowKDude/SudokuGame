from app import db
from datetime import datetime

class SudokuGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    difficulty = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<SudokuGame {self.username} - {self.difficulty}>'
