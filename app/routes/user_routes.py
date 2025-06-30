from flask import Blueprint
from app.controllers import user_controller

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/users', methods=['GET'])(user_controller.get_all_users)
user_bp.route('/users/<int:user_id>', methods=['GET'])(user_controller.get_user_by_id)
user_bp.route('/users', methods=['POST'])(user_controller.create_user)
user_bp.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])(user_controller.update_user)
user_bp.route('/users/<int:user_id>', methods=['DELETE'])(user_controller.delete_user)

