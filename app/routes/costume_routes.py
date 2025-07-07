from flask import Blueprint
from app.controllers import costume_controller

costume_bp = Blueprint('costume_bp', __name__)

costume_bp.route('/costumes', methods=['GET'])(costume_controller.get_all_costumes)
costume_bp.route('/costumes', methods=['POST'])(costume_controller.create_costume)
costume_bp.route('/costumes/<int:costume_id>', methods=['GET'])(costume_controller.get_costume_by_id)
costume_bp.route('/costumes/<int:costume_id>', methods=['PUT', 'PATCH'])(costume_controller.update_costume)
costume_bp.route('/costumes/<int:costume_id>', methods=['DELETE'])(costume_controller.delete_costume)

