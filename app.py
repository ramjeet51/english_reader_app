from flask import Flask, render_template, request, jsonify
from googletrans import Translator
import os

app = Flask(__name__)

# Initialize the translator
translator = Translator()

# File to store the history of read texts (including translation)
history_file = 'history.txt'

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html', history=load_history())

@app.route('/translate', methods=['POST'])
def translate():
    """Translate the input text and return the result."""
    text = request.form.get('text')
    if text.strip():
        translated = translator.translate(text, dest='hi')
        hindi_text = translated.text
        save_to_history(text, hindi_text)
        return jsonify({'success': True, 'hindi_text': hindi_text})
    return jsonify({'success': False, 'message': 'Please enter some text.'})

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear the history file."""
    if os.path.exists(history_file):
        os.remove(history_file)
    return jsonify({'success': True, 'message': 'History has been cleared!'})

def save_to_history(original_text, hindi_text):
    """Save the original and translated text to the history file."""
    with open(history_file, 'a', encoding='utf-8') as f:
        f.write(f"Original: {original_text}\nTranslated (Hindi): {hindi_text}\n\n")

def load_history():
    """Load the history from the history file."""
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            return f.read()
    return "No history available."

if __name__ == '__main__':
    app.run(debug=True)
