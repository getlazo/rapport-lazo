import os
import google.generativeai as genai

# Auth Gemini
GEMINI_API_KEY = os.getenv("AIzaSyC-iFUh40gexG0u3-ZFKyvhIOe73IYtIzU")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="models/gemini-1.5-pro-latest",
    generation_config={"temperature": 0.2}
)

def generate_summary_from_tables(text_summary: str) -> list:
    prompt = f"""
You are a data analyst. Write a summary of the following comparative tables in 3 concise bullet points. Don't talk about ongoing missions. Really short sentences.
The tone should be professional, neutral and insightful.
Only return the bullet points. Do not add introduction or conclusion.

{text_summary}
"""

    response = model.generate_content(prompt)

    # Split by line, keep only non-empty bullets
    bullet_lines = [
        line.strip()
        for line in response.text.strip().split("\n")
        if line.strip()
    ]

    return [
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": bullet}}]
            }
        }
        for bullet in bullet_lines
    ]
