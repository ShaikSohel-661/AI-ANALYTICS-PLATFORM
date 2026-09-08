import os
from dotenv import load_dotenv
from google import genai
from mistralai.client import Mistral

load_dotenv()
#gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)

#mistral
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

def generate_with_gemini(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        return response.text
    except Exception as exc:
        print(f"Error generating content with Gemini: {exc}")
        return None
def generate_with_mistral(prompt):
    try:
        response = mistral_client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as exc:
        print(f"Error generating content with Mistral: {exc}")
        return None
def generate_solution(prompt):
    gemnini_response = generate_with_gemini(prompt)
    if gemnini_response is not None:
        return gemnini_response
    mistral_response = generate_with_mistral(prompt)
    if mistral_response is not None:
        print("Using Mistral response as fallback.")
        return mistral_response
    return None

