from datetime import datetime
from App.database import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class ExcelData(db.Model):
    __tablename__ = 'excel_data'
    
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    data_field1 = db.Column(db.String(200))  # Adjust according to your Excel structure
    data_field2 = db.Column(db.String(200))
    data_field3 = db.Column(db.Float)
    data_field4 = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ExcelData {self.id}>'
    
    def get_json(self):
        return {
            'id': self.id,
            'report_id': self.report_id,
            'data_field1': self.data_field1,
            'data_field2': self.data_field2,
            'data_field3': self.data_field3,
            'data_field4': self.data_field4,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }