from flask import Flask, render_template, request, jsonify
import requests
import webbrowser
from threading import Timer

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


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

IMPORTANT LANGUAGE RULE:
- If the user's question is written in English, answer ONLY in English.
- If the user's question is written in Marathi, answer ONLY in Marathi.
- If the user's question is written in Hindi, answer ONLY in Hindi.
- Do NOT translate an English question into Gujarati.
- Never answer in Gujarati unless the user asks in Gujarati.
- Use simple and clear language.

User's question:
{question}

Give a direct and helpful answer.
"""

    try:

        response = requests.post(
    OLLAMA_URL,
    json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "10m"
    },
    timeout=600
)


        response.raise_for_status()

        result = response.json()

        return jsonify({
            "answer": result.get("response", "No answer received.")
        })

    except requests.exceptions.ConnectionError:

        return jsonify({
            "answer": "Ollama is not running. Please start Ollama first."
        }), 500

    except Exception as e:

        return jsonify({
            "answer": f"Error: {str(e)}"
        }), 500


def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":

    Timer(1, open_browser).start()

    app.run(debug=True)