from flask import Blueprint, request

main_bp = Blueprint('main', __name__)

@main_bp.post('/api/v1/inbound-message')
def handle_inbound_msg():
    data = request.get_json()
    return None