# Python script for ps1
import chardet
import numpy as np

import helpers

def read_text_from_file(file_path):
    """Reads and returns the content of a file using the appropriate encoding."""
    
    with open(file_path, 'rb') as file:
        rawdata = file.read()
        
    encoding_detected = chardet.detect(rawdata)['encoding']
    
    # List of encodings to try:
    encodings_to_try = [encoding_detected, 'utf-8', 'ISO-8859-1', 'windows-1252']
    
    for encoding in encodings_to_try:
        try:
            content = rawdata.decode(encoding)
            return content
        except UnicodeDecodeError:
            pass

    # If we've tried all encodings and none worked, then the file might contain binary or non-textual data
    return "Unable to decode the file. It may contain non-textual data."

def is_sensitive(filename, detector):

    doc = read_text_from_file(filename)

    counter = np.array(detector.is_sensitive(doc))
    return helpers.check_valid_sensitivities(counter)

