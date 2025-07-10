from flask import Blueprint
from app.controllers.costume_size_controller import (
    get_all_costume_sizes, get_costume_size_by_id, create_costume_size, update_costume_size, delete_costume_size
)

costume_size_bp = Blueprint('costume_size_bp', __name__)

costume_size_bp.route('/costume_sizes', methods=['GET', 'POST'])(get_all_costume_sizes)
costume_size_bp.route('/costume_sizes/<int:id>', methods=['GET', 'PUT', 'DELETE'])(get_costume_size_by_id) 