import os
import PyPDF2


import subprocess
import helpers
import numpy as np

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        # Initialize PDF reader
        pdf = PyPDF2.PdfReader(file)

        # Get total number of pages in the PDF
        num_pages = len(pdf.pages)

        # Extract text from each page
        text = ""
        for page_num in range(num_pages):
            page = pdf.pages[page_num]
            text += page.extract_text()

    return text





def extract_text_from_pdf_bash(pdf_path):
    # Use subprocess to run pdftotext and capture output
    result = subprocess.run(["pdftotext", "-q", pdf_path, "-"], stdout=subprocess.PIPE)
    
    # Check if the process completed successfully
    result.check_returncode()
    
    # Convert bytes to string and return
    return result.stdout.decode('utf-8')


def is_sensitive(file_path, detector):

    text = extract_text_from_pdf(file_path)

    counter = np.array(detector.is_sensitive(text))
    return helpers.check_valid_sensitivities(counter)
    