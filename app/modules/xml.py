# Python script for xml

import chardet
import numpy as np
from xml.etree import cElementTree as ET
import os 
from bs4 import BeautifulSoup

def is_sensitive(filename, _):

    with open(filename, encoding='ISO-8859-1') as f:
        rawdata = f.read()
    
    root = ET.fromstring(rawdata)

    for element in root:
        firstname = element[0].text
        lastname = element[1].text
        address = element[2].text
        iban = element[3].text 
        if (firstname and lastname) and(address or iban):
            return True
    return False 