import numpy as np
import spacy 
# python3 -m spacy download en_core_web_sm

def has_full_name(text):
    english_nlp = spacy.load('en_core_web_sm')  
    spacy_parser = english_nlp(text)
    names = [ent.text for ent in spacy_parser.ents if ent.label_ == "PERSON"]

    for name in names:
        if len(name.split()) >= 2:
            return True
    return False
