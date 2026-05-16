from flask import Blueprint, request, jsonify
from app.services.gemini import categorize_message

main_bp = Blueprint('main', __name__)


@main_bp.post('/api/v1/inbound-message')
def handle_inbound_message():
    data = request.get_json()

    # Structural Validation: Ensure the payload structure is correct
    if not data or 'message' not in data or 'email' not in data:
        return jsonify({"error": "Bad Request. Missing 'message' or 'email' fields."}), 400

    user_email = data['email']
    message_content = data['message']

    # Content Validation: Check if the message actually contains text
    if str(message_content).strip():
        category = categorize_message(message_content)
    else:
        category = "Uncategorized"

    # TODO: Add db logic here.

    return jsonify({
        "status": "success",
        "email": user_email,
        "assigned_category": category
    }), 200