from google import genai
from google.genai import types


def categorize_message(message_text):
    # Initialize inside the function or at module level
    # It will automatically pick up GEMINI_API_KEY from the environment via python-dotenv
    client = genai.Client()

    prompt = f"""
    Analyze the following customer message and categorize it as exactly one of: 'Technical Support', 'Sales', or 'Billing'.
    Respond with ONLY the category name. Do not include any other text or punctuation.

    Message: {message_text}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.0)
        )
        return (response.text or "").strip()
    except Exception as e:
        # Log the error in a real app
        print(f"Gemini API Error: {e}")
        return "Needs Human Review"