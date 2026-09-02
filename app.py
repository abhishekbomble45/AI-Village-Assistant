from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "answer": "Please enter a question."
        })

    prompt = f"""
You are an AI Village Assistant.

You help village users with:
- Agriculture
- Education
- Government schemes
- Digital services
- Village development
- General information

LANGUAGE RULES:
- English question → answer only in English.
- Marathi question → answer only in Marathi.
- Hindi question → answer only in Hindi.
- Do not answer in Gujarati unless the user asks in Gujarati.
- Use simple and clear language.
- Give a direct and helpful answer.

User Question:
{question}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return jsonify({
            "answer": response.text
        })

    except Exception as e:
        return jsonify({
            "answer": f"Error: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run()
