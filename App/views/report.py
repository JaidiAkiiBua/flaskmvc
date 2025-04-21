from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_jwt_extended import jwt_required, current_user
from werkzeug.utils import secure_filename
import os

from App.controllers.report import (
    allowed_file,
    get_all_reports,
    get_reports_by_user,
    get_report_by_id,
    create_report,
    update_report,
    delete_report,
    get_chart_data
)

report_views = Blueprint('report_views', __name__, template_folder='../templates')

@report_views.route('/admin/reports', methods=['GET'])
@jwt_required()
def list_reports():
    if current_user.role != 'admin':
        flash('Only administrators can access this page.', 'danger')
        return redirect(url_for('user_views.user_index'))
    
    reports = get_all_reports()
    return render_template('admin/list.html', reports=reports)

@report_views.route('/admin/reports/create', methods=['GET', 'POST'])
@jwt_required()
def create_report_page():
    if current_user.role != 'admin':
        flash('Only administrators can create reports.', 'danger')
        return redirect(url_for('user_views.user_index'))
    
    if request.method == 'POST':
        admin_name = request.form.get('admin_name')
        campus = request.form.get('campus')
        year = request.form.get('year')
        title = request.form.get('title')
        
        if 'excel_file' not in request.files:
            flash('No file uploaded.', 'danger')
            return redirect(request.url)
        
        file = request.files['excel_file']
        
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            file_path = os.path.join(upload_folder, filename)
            
            # Ensure upload directory exists
            os.makedirs(upload_folder, exist_ok=True)
            file.save(file_path)
            
            # Create report using controller function
            report = create_report(title, admin_name, campus, year, current_user.id, file_path)
            
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)
            
            if report:
                flash('Report created successfully!', 'success')
                return redirect(url_for('report_views.view', report_id=report.id))
            else:
                flash('Error processing Excel file.', 'danger')
    
    return render_template('admin/create_report.html')

@report_views.route('/admin/reports/<int:report_id>', methods=['GET'])
@jwt_required()
def view_report(report_id):
    if current_user.role != 'admin':
        flash('Only administrators can view reports.', 'danger')
        return redirect(url_for('user_views.user_index'))
    
    report = get_report_by_id(report_id)
    chart_data = get_chart_data(report_id)
    return render_template('admin/view.html', report=report, chart_data=chart_data)

@report_views.route('/admin/reports/<int:report_id>/update', methods=['GET', 'POST'])
@jwt_required()
def update_report_page(report_id):
    if current_user.role != 'admin':
        flash('Only administrators can update reports.', 'danger')
        return redirect(url_for('user_views.user_index'))
    
    report = get_report_by_id(report_id)
    
    if request.method == 'POST':
        admin_name = request.form.get('admin_name')
        campus = request.form.get('campus')
        year = request.form.get('year')
        title = request.form.get('title')
        file_path = None
        
        if 'excel_file' in request.files:
            file = request.files['excel_file']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
        
        success = update_report(report_id, title, admin_name, campus, year, file_path)
        
        # Clean up uploaded file if it exists
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        
        if success:
            flash('Report updated successfully!', 'success')
            return redirect(url_for('report_views.view', report_id=report_id))
        else:
            flash('Error updating report.', 'danger')
    
    return render_template('admin/update.html', report=report)

@report_views.route('/admin/reports/<int:report_id>/delete', methods=['POST'])
@jwt_required()
def delete_report_action(report_id):
    if current_user.role != 'admin':
        flash('Only administrators can delete reports.', 'danger')
        return redirect(url_for('user_views.user_index'))
    
    if delete_report(report_id):
        flash('Report deleted successfully!', 'success')
    else:
        flash('Error deleting report.', 'danger')
    
    return redirect(url_for('report_views.view'))

'''
API Routes
'''

@report_views.route('/api/reports/<int:report_id>/chart-data')
@jwt_required()
def get_chart_data_api(report_id):
    chart_data = get_chart_data(report_id)
    return jsonify(chart_data)