from flask import Blueprint
from app.controllers import payment_controller

payment_bp = Blueprint('payment_bp', __name__)

payment_bp.route('/payments', methods=['GET'])(payment_controller.get_all_payments)
payment_bp.route('/payments', methods=['POST'])(payment_controller.create_payment)
payment_bp.route('/payments/<int:payment_id>', methods=['GET'])(payment_controller.get_payment_by_id)
payment_bp.route('/payments/<int:payment_id>', methods=['PUT', 'PATCH'])(payment_controller.update_payment)
payment_bp.route('/payments/<int:payment_id>', methods=['DELETE'])(payment_controller.delete_payment)
payment_bp.route('/payments/<int:payment_id>/verify', methods=['POST'])(payment_controller.verify_payment)
