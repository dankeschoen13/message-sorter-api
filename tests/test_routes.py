from unittest.mock import patch

def test_inbound_message_success(client):
    """
    Test that a valid message is correctly categorized and saved to the DB.
    """

    payload = {
        "email": "tester@example.com",
        "message": "My account is locked out, please reset my password."
    }

    # patched gemini call so we don't waste an actual gemini query
    with patch('app.routes.main.categorize_message', return_value="Technical Support"):
        response = client.post('/api/v1/inbound-message', json=payload)

    # Assertions
    assert response.status_code == 200
    assert response.json["assigned_category"] == "Technical Support"
    assert response.json["ai_processed"] is True

def test_inbound_message_blank_content(client):
    """
    Test that an empty message string bypasses AI and marks as Uncategorized.
    """

    payload = {
        "email": "silent@example.com",
        "message": "    "
    }

    response = client.post('/api/v1/inbound-message', json=payload)

    assert response.status_code == 200
    assert response.json["assigned_category"] == "Uncategorized"
    assert response.json["ai_processed"] is False