# app.py
from flask import Flask, request, jsonify, render_template
import os
# Import the Google Generative AI client library
import google.generativeai as genai

app = Flask(__name__)

# Load API Key from Environment Variable
# IMPORTANT: Set this environment variable on your server where you run this app.
# Example (Linux/macOS): export GEMINI_API_KEY='YOUR_API_KEY'
# Example (Windows CMD): set GEMINI_API_KEY='YOUR_API_KEY'
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # CORRECTED: Loading from environment variable

if not GEMINI_API_KEY:
    # Raise an error if the API key is not found, providing clear instructions.
    raise ValueError(
        "Missing Google Gemini API Key! "
        "Please set the 'GEMINI_API_KEY' environment variable. "
        "DO NOT hardcode your API key directly in the code." # Added a warning
    )

# Configure the Google Generative AI client with your API key
genai.configure(api_key=GEMINI_API_KEY)

def generate_chat_response_from_gemini(prompt):
    """
    Generate an AI response using Google's Gemini API.

    :param prompt: User's input message
    :return: AI-generated response or an error message
    """
    try:
        # Initialize the Generative Model.
        # Changed model from 'gemini-pro' to 'gemini-1.5-flash' for wider availability.
        model = genai.GenerativeModel('gemini-1.5-flash') 
        
        # Generate content using the model
        response = model.generate_content(prompt)
        
        # Return the generated text from the response
        return response.text
        
    except Exception as e:
        # Log the detailed error on the server side for debugging
        print(f"Server-side Gemini API Error: {str(e)}")
        # Return a user-friendly error message to the client
        return f"AI Error: Could not generate response. Please try again later. Details: {str(e)}"

@app.route('/')
def index():
    """Renders the main HTML page for the chatbot UI."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles POST requests from the client-side for chat messages.
    Receives user input and returns a Gemini response.
    """
    data = request.json
    user_input = data.get("message")
    
    if not user_input:
        # Return a 400 Bad Request if the message is missing
        return jsonify({"error": "Message is required"}), 400
    
    # Call the function to get the response from Gemini
    response_from_gemini = generate_chat_response_from_gemini(user_input)
    
    # Return the response to the client
    return jsonify({"response": response_from_gemini})

if __name__ == "__main__":
    # Ensure debug is False in production environments for security and performance
    app.run(host='0.0.0.0', port=5000, debug=True)
