from PyPDF2 import PdfReader
from fastapi import UploadFile
from io import BytesIO              # classe BytesIO - audio, video, arquivo (PDF) -> binário

# Function to extract text from a PDF File
def extract_text_from_pdf(filepdf: UploadFile):

    # read the PDF file - binary
    pdf_byte = filepdf.file.read()

    # create a PDF reader
    pdf_stream = BytesIO(pdf_byte)

    readerPDF = PdfReader(pdf_stream)
    text = ""
    for page in readerPDF.pages:
        text += page.extract_text()
    return text

# Function to extract text from a TXT File
def extract_text_from_txt(filetxt: UploadFile):
    # lê todo o arquivo e decodifica
    content = filetxt.file.read()
    
    try:
        # tenta UTF-8 (padrão mais comum)
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        text = content.decode("latin-1")
    
    return text

# Function to make SPLIT the text into chuncks -> chunk_size=1000, overlap=200 para chunk_size=1500, overlap=300
def split_text_into_chunks(text: str, chunk_size=2000, overlap=400) -> list:
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    
    return chunks