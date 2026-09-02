from flask import Flask, render_template, request, jsonify
from google import genai
import os
import re

app = Flask(__name__)

# ==============================
# Gemini API Configuration
# ==============================

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=api_key)


# ==============================
# Home Page
# ==============================

@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# AI Question Answer
# ==============================

@app.route("/ask", methods=["POST"])
def ask():

    try:
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

        # Short and fast prompt
        prompt = f"""
You are AI Village Assistant.

Help users with:
Agriculture, education, government schemes,
digital services, village development and general information.

Language:
English question = English answer.
Marathi question = Marathi answer.
Hindi question = Hindi answer.

Use simple language.
Give a direct answer.
Do not use Markdown.
Do not use *, **, # or bullet symbols.

Question:
{question}
"""

        # Gemini request
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        answer = interaction.output_text

        # Clean formatting
        answer = answer.replace("**", "")
        answer = answer.replace("__", "")
        answer = answer.replace("`", "")
        answer = answer.replace("#", "")
        answer = answer.replace("*", "")

        answer = re.sub(
            r"(?m)^\s*[-•]\s*",
            "",
            answer
        )

        answer = re.sub(
            r"\n\s*\n\s*\n+",
            "\n\n",
            answer
        )

        answer = answer.strip()

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "answer": "Sorry, AI response failed. Please try again."
        }), 500


# ==============================
# Run Flask
# ==============================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
