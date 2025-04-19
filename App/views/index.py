from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, current_user
from App.controllers import create_user, initialize
from App.models import User

index_views = Blueprint('index_views', __name__, template_folder='../templates')

# Home page route
@index_views.route('/', methods=['GET'])
def index_page():
    try:
        # Try to verify JWT, but don't require it
        verify_jwt_in_request(optional=True)
        
        if current_user:  # User is authenticated
            if current_user.role == 'admin':
                return redirect(url_for('admin.index'))
            else:
                return redirect(url_for('user_views.user_index'))
        else:
            # User is not authenticated, redirect to login
            return redirect(url_for('auth_views.login_page'))
    except:
        # If JWT verification fails, redirect to login
        return redirect(url_for('auth_views.login_page'))

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})