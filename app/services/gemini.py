from google import genai
from google.genai import types
from enum import Enum


class AICategory(str, Enum):

    TECHNICAL_SUPPORT = "Technical Support"
    SALES = "Sales"
    BILLING = "Billing"
    UNCATEGORIZED = "Uncategorized"
    PENDING_RETRY = "Pending Retry"

def categorize_message(message_text):
    client = genai.Client()
    prompt = f"""
    Analyze the following customer message and categorize it into the most appropriate category.
    Message: {message_text}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,
                response_mime_type="text/x.enum",
                response_schema=AICategory
            )
        )
        return (response.text or "").strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return AICategory.PENDING_RETRY.value