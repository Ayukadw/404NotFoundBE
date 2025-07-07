from flask import Blueprint
from app.controllers import order_controller

order_bp = Blueprint('order_bp', __name__)

order_bp.route('/orders', methods=['GET'])(order_controller.get_all_orders)
order_bp.route('/orders', methods=['POST'])(order_controller.create_order)
order_bp.route('/orders/<int:order_id>', methods=['GET'])(order_controller.get_order_by_id)
order_bp.route('/orders/<int:order_id>', methods=['PUT', 'PATCH'])(order_controller.update_order)
order_bp.route('/orders/<int:order_id>', methods=['DELETE'])(order_controller.delete_order)
order_bp.route('/orders/user/<int:user_id>', methods=['GET'])(order_controller.get_orders_by_user)
order_bp.route('/orders/<int:order_id>/status', methods=['PUT'])(order_controller.update_order_status)
order_bp.route('/orders/<int:order_id>/payment-status', methods=['PUT'])(order_controller.update_order_payment_status)
order_bp.route('/orders/<int:order_id>/return', methods=['POST'])(order_controller.return_order)
