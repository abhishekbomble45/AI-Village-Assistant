from flask import Flask, render_template, request, jsonify
from google import genai
import os
import re

app = Flask(__name__)

# Gemini API Key
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

    if not data:
        return jsonify({
            "answer": "Please enter a question."
        })

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

IMPORTANT FORMATTING RULES:
- Give answers in plain text only.
- Do not use Markdown.
- Do not use ** or * symbols.
- Do not use # headings.
- Do not use backticks.
- Do not use Markdown bullet symbols.
- Use simple numbered points when needed.
- Do not add unnecessary formatting.
- Give a direct and helpful answer.

User Question:
{question}
"""

    try:

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        answer = interaction.output_text

        # Remove Markdown formatting
        answer = answer.replace("**", "")
        answer = answer.replace("__", "")
        answer = answer.replace("`", "")
        answer = answer.replace("#", "")

        # Remove single star formatting
        answer = answer.replace("*", "")

        # Remove Markdown bullet at line beginning
        answer = re.sub(r"(?m)^\s*[-•]\s*", "", answer)

        # Remove extra spaces
        answer = re.sub(r"\n\s*\n\s*\n+", "\n\n", answer)

        answer = answer.strip()

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        return jsonify({
            "answer": f"Error: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run()
