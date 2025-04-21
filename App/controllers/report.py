from App.models import Report, ExcelData, User
from App.database import db
import os
import pandas as pd
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_excel(file_path, report_id):
    try:
        # Read Excel file using pandas
        df = pd.read_excel(file_path)
        
        # Process each row and save to ExcelData model
        for index, row in df.iterrows():
            excel_data = ExcelData(
                report_id=report_id,
                data_field1=str(row.get('Field1', '')),  # Adjust column names according to your Excel structure
                data_field2=str(row.get('Field2', '')),
                data_field3=float(row.get('Field3', 0)),
                data_field4=float(row.get('Field4', 0))
            )
            db.session.add(excel_data)
        
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error processing Excel file: {str(e)}")
        return False

def get_all_reports():
    return Report.query.order_by(Report.created_at.desc()).all()

def get_reports_by_user(user_id):
    return Report.query.filter_by(user_id=user_id).order_by(Report.created_at.desc()).all()

def get_report_by_id(report_id):
    return Report.query.get_or_404(report_id)

def create_report(title, admin_name, campus, year, user_id, file_path):
    new_report = Report(
        title=title,
        admin_name=admin_name,
        campus=campus,
        year=year,
        user_id=user_id
    )
    
    db.session.add(new_report)
    db.session.commit()
    
    if process_excel(file_path, new_report.id):
        return new_report
    else:
        # If Excel processing fails, delete the report
        db.session.delete(new_report)
        db.session.commit()
        return None

def update_report(report_id, title, admin_name, campus, year, file_path=None):
    report = Report.query.get_or_404(report_id)
    
    report.title = title
    report.admin_name = admin_name
    report.campus = campus
    report.year = year
    
    if file_path:
        # Delete existing excel data
        ExcelData.query.filter_by(report_id=report.id).delete()
        
        # Process new Excel file
        if not process_excel(file_path, report.id):
            db.session.rollback()
            return False
    
    db.session.commit()
    return True

def delete_report(report_id):
    report = Report.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    return True

def get_chart_data(report_id):
    report = Report.query.get_or_404(report_id)
    
    chart_data = {
        'labels': [],
        'datasets': [{
            'label': 'Data Field 3',
            'data': [],
            'backgroundColor': 'rgba(54, 162, 235, 0.5)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'borderWidth': 1
        }]
    }
    
    for excel_data in report.excel_data:
        chart_data['labels'].append(excel_data.data_field1)
        chart_data['datasets'][0]['data'].append(excel_data.data_field3)
    
    return chart_data