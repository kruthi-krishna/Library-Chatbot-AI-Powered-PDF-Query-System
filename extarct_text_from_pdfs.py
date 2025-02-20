from transformers import pipeline

summarizer = pipeline("summarization")

def summarize_text(text):
    return summarizer(text, max_length=50, min_length=25, do_sample=False)[0]['summary_text']

def extract_text_from_pdf(pdf_path, page_number):
    reader = PdfReader(pdf_path)
    return reader.pages[page_number].extract_text()