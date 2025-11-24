# src/services/gemini.py
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def get_translation(text: str) -> str:
    prompt = f"""
    You are the best Chinese-Myanmar dictionary teacher for students.
    Input: "{text}"

    Auto-detect language:
    - If Chinese → reply in Myanmar + Pinyin (in English letters)
    - If Myanmar → reply in Chinese (Simplified) + Romanization (in English letters)

    Always reply in this exact beautiful format:

    Language Detection: [Detected Language]
    
    Translation: [Translation]
    Pronunciation: [Pinyin or Romanization in English letters]
    Meaning: [Short clear meaning]
    
    Example:
    [One natural example sentence in both languages]

    Use emojis and make it very easy to read for students.
    Be warm and encouraging like a real teacher.
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.4,
                "max_output_tokens": 800,
            }
        )
        return response.text.strip()
    except Exception as e:
        return f"Temporary system error: {str(e)}"
