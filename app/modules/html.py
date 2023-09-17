# Python script for html
from bs4 import BeautifulSoup
import re
import numpy as np

import helpers

def is_sensitive(filename, detector):

    with open(filename, "r", encoding="utf-8") as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, "html.parser")
    plain_text = soup.get_text()
    text = re.split(r'[\n\t\f\v\r]+', plain_text) # this is a list of strings!! 
    

    counter = np.array(detector.is_sensitive(" ".join(text)))
    return helpers.check_valid_sensitivities(counter)