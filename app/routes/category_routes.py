from flask import Blueprint
from app.controllers import category_controller

category_bp = Blueprint('category_bp', __name__)

category_bp.route('/categories', methods=['GET'])(category_controller.get_all_categories)
category_bp.route('/categories', methods=['POST'])(category_controller.create_category)
category_bp.route('/categories/<int:category_id>', methods=['GET'])(category_controller.get_category_by_id)
category_bp.route('/categories/<int:category_id>', methods=['PUT', 'PATCH'])(category_controller.update_category)
category_bp.route('/categories/<int:category_id>', methods=['DELETE'])(category_controller.delete_category)
