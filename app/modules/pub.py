# Python script for pub
import pandas as pd
import re
import spacy 
import chardet
from const import *

def regex_filter(string): 
    return {
        "email": re.search(PATTERN_EMAIL, string) is not None, 
        "iban": re.search(PATTERN_IBAN, string) is not None
    }

def has_full_name(text):
    english_nlp = spacy.load('en_core_web_sm')  
    spacy_parser = english_nlp(text)
    names = [ent.text for ent in spacy_parser.ents if ent.label_ == "PERSON"]

    for name in names:
        if len(name.split()) >= 2:
            return True
    return False
def is_sensitive(filename, detector):

    with open(filename, 'rb') as file:
        rawdata = file.read()
        
    encoding_detected = chardet.detect(rawdata)['encoding']
    
    # List of encodings to try:
    encodings_to_try = [encoding_detected, 'utf-8', 'ISO-8859-1', 'windows-1252']
    
    for encoding in encodings_to_try:
        try:
            content = rawdata.decode(encoding)
        except UnicodeDecodeError:
            pass
    regex = regex_filter(content)
    has_email, has_iban = regex["email"], regex["iban"]

    if has_email and has_iban: # Only true if it isn't github email...
        # print("Check 2 (MAIL)", filename)
        return  True 
    
    if has_email and has_full_name(content): 
        # print("Check 2 (IBAN)", filename)
        return True
    if has_iban and has_full_name(content): 
        # print("Check 2 (IBAN)", filename)
        return True
    else:
      return False

