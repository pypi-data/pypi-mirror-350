import os
from ecom_data_helpers.document_extraction import (
    extract_pdf_to_text,
    analyze_pdf_invoice,
    analyze_image_invoice,
    extract_docx_to_text
)

ROOT_DIR = os.getcwd()

if __name__ == '__main__':
    print("Starting...")

    print(ROOT_DIR)

    filepath = ROOT_DIR + "/examples/data/invoice-image.jpg"

    with open(filepath, 'rb') as file: 
        text = analyze_image_invoice(doc_bytes=file.read())


        print(text)