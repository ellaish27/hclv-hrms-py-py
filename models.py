# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt as pybcrypt

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum('admin', 'hrOfficer', 'employee'), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    department_id = db.Column(db.Integer)
    is_locked = db.Column(db.Boolean, default=False)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = pybcrypt.hashpw(password.encode(), pybcrypt.gensalt()).decode()

    def check_password(self, password):
        return pybcrypt.checkpw(password.encode(), self.password_hash.encode())
