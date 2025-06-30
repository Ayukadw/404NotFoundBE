from flask import Blueprint
from app.controllers import size_controller

size_bp = Blueprint('size_bp', __name__)

size_bp.route('/sizes', methods=['GET'])(size_controller.get_all_sizes)
size_bp.route('/sizes', methods=['POST'])(size_controller.create_size)
size_bp.route('/sizes/<int:size_id>', methods=['GET'])(size_controller.get_size_by_id)
size_bp.route('/sizes/<int:size_id>', methods=['PUT', 'PATCH'])(size_controller.update_size)
size_bp.route('/sizes/<int:size_id>', methods=['DELETE'])(size_controller.delete_size)
