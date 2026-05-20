from flask import Blueprint, request, jsonify
from app.services import categorize_message, MessageSvc

main_bp = Blueprint('main', __name__)


@main_bp.post('/api/v1/inbound-message')
def handle_inbound_message():
    data = request.get_json(silent=True) or {}

    # Structural Validation: Ensure the payload structure is correct
    if not data or 'message' not in data or 'email' not in data:
        return jsonify({"error": "Bad Request. Missing 'message' or 'email' fields."}), 400

    user_email = data['email']
    message_content = data['message']
    used_ai = False

    # Content Validation: Check if the message actually contains text
    if str(message_content).strip():
        category = categorize_message(message_content)
        if category == 'Pending Retry':
            used_ai = False
        else:
            used_ai = True
    else:
        category = 'Uncategorized'

    try:
        new_msg = MessageSvc.new_message(
            email=user_email,
            content=message_content,
            category=category,
            ai_processed=used_ai
        )
    except ValueError:
        return jsonify({"error": "Internal Server Error. Could not save message."}), 500


    return jsonify({
        "status": "success",
        "email": user_email,
        "assigned_category": category,
        "ai_processed": used_ai
    }), 200
