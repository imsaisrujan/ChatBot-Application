from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Load API Key from Environment Variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key! Set OPENAI_API_KEY in environment variables.")

openai.api_key = OPENAI_API_KEY

def generate_chat_response(prompt):
    """
    Generate AI response using OpenAI's ChatGPT API.

    :param prompt: User's input message
    :return: AI-generated response
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"API Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message")
    
    if not user_input:
        return jsonify({"error": "Message is required"}), 400
    
    response = generate_chat_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
