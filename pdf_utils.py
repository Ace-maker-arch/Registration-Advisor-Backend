from io import BytesIO# Lets python treat ray bytes like a file
from pypdf import PdfReader#Read pdf files


def extract_pdf_text(contents: bytes) -> str:
    pdf_reader = PdfReader(BytesIO(contents))#(BytesIO(contents)) this turn the rawpdf bytes into soemhting PDFReader can read

    extracted_text = ""
    for page in pdf_reader.pages:#loops through ever page in the pdf
        extracted_text += page.extract_text() or ""

    return extracted_text
