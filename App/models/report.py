from datetime import datetime
from App.database import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    admin_name = db.Column(db.String(100), nullable=False)
    campus = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationship with ExcelData
    excel_data = db.relationship('ExcelData', backref='report', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Report {self.title}>'
    
    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'admin_name': self.admin_name,
            'campus': self.campus,
            'year': self.year,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': self.user_id
        }
