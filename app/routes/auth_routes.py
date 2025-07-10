from flask import Blueprint
from app.controllers import auth_controller

auth_bp = Blueprint('auth_bp', __name__)

auth_bp.route('/login', methods=['POST'])(auth_controller.login)
auth_bp.route('/register', methods=['POST'])(auth_controller.register)
auth_bp.route('/profile', methods=['GET'])(auth_controller.get_profile)
auth_bp.route('/logout', methods=['POST'])(auth_controller.logout)
