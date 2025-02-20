# Library Chatbot – AI-Powered PDF Query System

An interactive chatbot that enables users to query PDFs and retrieve AI-powered summaries.

## Features
- **PDF Processing**: Extracts text from uploaded PDF documents.
- **AI-Powered Summarization**: Uses Hugging Face Transformers for text summarization.
- **Word Definitions**: Retrieves word meanings using NLTK’s WordNet.
- **Secure API Access**: Implements authentication via API keys.
- **Interactive Chatbot UI**: Communicates with the backend in real-time.
- **REST API**: Handles chatbot queries via Flask-based API.

## Technologies Used
- **Backend**: Python (Flask)
- **NLP**: Hugging Face Transformers, NLTK WordNet
- **Database**: SQLite
- **Frontend**: JavaScript (Planned for integration)
- **Other Dependencies**: PyPDF2, Torch, Spacy

## Installation
### Prerequisites
Ensure you have **Python 3.8+** installed.

### Clone the Repository
```bash
git clone https://github.com/your-username/library-chatbot.git
cd library-chatbot
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Set Up API Key
Create a file named `KEY.txt` and add your API key inside:
```
sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Run the Application
```bash
python app.py
```

## API Endpoints
| **Endpoint**      | **Method** | **Description** |
|------------------|-----------|----------------|
| `/`             | GET       | Welcome message |
| `/list_pdfs`    | GET       | Lists available PDFs |
| `/extract`      | POST      | Extracts text from a PDF page |
| `/summarize`    | POST      | Summarizes provided text |
| `/meaning`      | POST      | Fetches the definition of a word |

## Example Usage
### Extract Text from a PDF
#### Request
```json
{
  "pdf_name": "example.pdf",
  "page_number": 2
}
```

#### Response
```json
{
  "text": "Extracted text from the specified page."
}
```

### Summarize Text
#### Request
```json
{
  "text": "Artificial Intelligence is transforming the world by automating tasks and enhancing decision-making."
}
```

#### Response
```json
{
  "summary": "AI is automating tasks and improving decision-making."
}
```

### Fetch Word Meaning
#### Request
```json
{
  "word": "Artificial"
}
```

#### Response
```json
{
  "meaning": "Made or produced by human beings rather than occurring naturally."
}
```

## Future Enhancements
- Enhanced Chat UI: Develop a frontend for real-time chatbot interactions.
- Metadata Extraction: Display author, title, and other document details.
- Cloud Storage Integration: Enable PDF uploads via a web interface.

## Contributing
Feel free to fork this repository and submit pull requests! 




