from app import db
from app.models import SudokuGame

db.create_all()

db.session.commit()
