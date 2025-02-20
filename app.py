import os
import sqlite3
from PyPDF2 import PdfReader
from transformers import pipeline
import nltk
from nltk.corpus import wordnet
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Load NLTK resources
nltk.download("wordnet")

# Load API Key securely from file
with open("KEY.txt", "r") as key_file:
    API_KEY = key_file.read().strip()

def check_api_key():
    """Check API Key from headers."""
    if request.headers.get("API-KEY") != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    return None

def connect_db():
    """Connect to SQLite database."""
    return sqlite3.connect("library.db", check_same_thread=False)

def load_pdfs(pdf_directory):
    """Load PDFs into the database."""
    if not os.path.exists(pdf_directory):
        raise FileNotFoundError(f"The directory {pdf_directory} does not exist.")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS pdfs 
                      (id INTEGER PRIMARY KEY, title TEXT, path TEXT)""")

    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            path = os.path.join(pdf_directory, filename)
            cursor.execute("INSERT OR IGNORE INTO pdfs (title, path) VALUES (?, ?)", (filename, path))

    conn.commit()
    conn.close()

def extract_text_from_pdf(pdf_path, page_number):
    """Extract text from a specific PDF page."""
    reader = PdfReader(pdf_path)
    if page_number < len(reader.pages):  
        return reader.pages[page_number].extract_text() or "No text found."
    return "Page number out of range."

def summarize_text(text):
    """Summarize text using transformers."""
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return summarizer(text, max_length=50, min_length=20, do_sample=False)[0]["summary_text"]

def get_word_meaning(word):
    """Fetch word meaning from WordNet."""
    meanings = wordnet.synsets(word)
    return meanings[0].definition() if meanings else "Meaning not found."

@app.route("/")
def index():
    """Welcome route."""
    return jsonify({"message": "Welcome to the Library Chatbot API"})

@app.route("/list_pdfs", methods=["GET"])
def list_pdfs():
    """List available PDFs."""
    auth_error = check_api_key()
    if auth_error:
        return auth_error

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM pdfs")
    pdfs = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify({"pdfs": pdfs})

@app.route("/extract", methods=["POST"])
def extract():
    """Extract text from a specific PDF page."""
    auth_error = check_api_key()
    if auth_error:
        return auth_error

    data = request.json
    pdf_name = data.get("pdf_name")
    page_number = data.get("page_number")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM pdfs WHERE title=?", (pdf_name,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        return jsonify({"error": "PDF not found"}), 404

    text = extract_text_from_pdf(result[0], page_number)
    return jsonify({"text": text})

@app.route("/summarize", methods=["POST"])
def summarize():
    """Summarize the given text."""
    auth_error = check_api_key()
    if auth_error:
        return auth_error

    data = request.json
    text = data.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    summary = summarize_text(text)
    return jsonify({"summary": summary})

@app.route("/meaning", methods=["POST"])
def meaning():
    """Fetch the meaning of a given word."""
    auth_error = check_api_key()
    if auth_error:
        return auth_error

    data = request.json
    word = data.get("word")
    if not word:
        return jsonify({"error": "No word provided"}), 400
    meaning = get_word_meaning(word)
    return jsonify({"meaning": meaning})

if __name__ == "__main__":
    load_pdfs("C:/Users/91998/Downloads/kruthi AI")  # Load PDFs from 'pdfs' folder
    app.run(debug=True)
