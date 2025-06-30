from flask import Blueprint
from app.controllers import order_item_controller

order_item_bp = Blueprint('order_item_bp', __name__)

order_item_bp.route('/order-items', methods=['GET'])(order_item_controller.get_all_order_items)
order_item_bp.route('/order-items', methods=['POST'])(order_item_controller.create_order_item)
order_item_bp.route('/order-items/<int:item_id>', methods=['GET'])(order_item_controller.get_order_item_by_id)
order_item_bp.route('/order-items/<int:item_id>', methods=['PUT', 'PATCH'])(order_item_controller.update_order_item)
order_item_bp.route('/order-items/<int:item_id>', methods=['DELETE'])(order_item_controller.delete_order_item)
