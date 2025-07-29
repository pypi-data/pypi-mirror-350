import os
import re
import fitz
import docx
from bs4 import BeautifulSoup

FOLDER_PATH = "documents"

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    try:
        if ext == ".pdf":
            doc = fitz.open(file_path)
            text = "\n".join(page.get_text() for page in doc)

        elif ext == ".docx":
            doc = docx.Document(file_path)
            text = "\n".join(p.text for p in doc.paragraphs)

        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        elif ext == ".html" or ext == ".htm":
            with open(file_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
                text = soup.get_text(separator="\n")

        else:
            text = f"[Unsupported file type: {ext}]"

    except Exception as e:
        text = f"[Error reading {file_path}: {str(e)}]"

    return text

def extract_text(folder_path):

    filenames, documents = [], []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.pdf', '.docx', '.txt', '.html', '.htm')):
            file_path = os.path.join(folder_path, filename)
            text = extract_text_from_file(file_path)

            text = re.sub(r'\s+', ' ', text).strip()

            filenames.append(filename)
            documents.append(text)

    return filenames, documents
