def load_pdfs(pdf_directory):
    print(f"Loading PDFs from {pdf_directory}")
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pdfs
                      (id INTEGER PRIMARY KEY, title TEXT, author TEXT, path TEXT)''')

    if not os.path.exists(pdf_directory):
        raise FileNotFoundError(f"The directory {pdf_directory} does not exist.")
    
    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            print(f"Found PDF: {filename}")  # Log message
            path = os.path.join(pdf_directory, filename)
            reader = PdfReader(path)
            title = reader.metadata.title if reader.metadata.title else filename
            author = reader.metadata.author if reader.metadata.author else "Unknown"
            cursor.execute("INSERT INTO pdfs (title, author, path) VALUES (?, ?, ?)", (title, author, path))
    
    conn.commit()
    conn.close()
