import re
import spacy
import const

class SensitiveDataDetector:

    def __init__(self):

        # Create flags
        self.reset_flags()
        self.nlp = spacy.load("en_core_web_sm")

        self.rsa_patterns = {
            "RSA private key": r"(-----BEGIN RSA PRIVATE KEY-----)?(\s|\n)*MII(.|\n){10,1616}(-----END RSA PRIVATE KEY-----)?",  # simplified pattern
        }

        self.direct_patterns = {
            "Email Address": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "Company name": r"\b[A-Z][a-z]+\s[A-Z][a-z]+(Co|Corp|Company|Inc|Ltd)\b",
            "Company name": r"\bCompany Name:\n-?\W?[a-zA-Z\s]*\n\b",
        }

        self.indirect_patterns = {
            "Address": r"\b\d+\s[A-Z][a-z]+(St|Ave|Blvd|Rd),\s[A-Z][a-z]+,\s[A-Z][a-z]+\b",
            "Phone number": r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b",
            "IBAN": r"\b[A-Z]{2}\d{2}[a-zA-Z0-9]{4}\d{7}\b"  # basic pattern for IBAN
        }

        self.potential_indirect_patterns = {
            "Nationality": r"\b[A-Z][a-z]+(ian|ish|ese)\b",  # simplified pattern
            "Age": r"\b\d{1,3}\syears?\sold\b",
            "Gender": r"\b(male|female)\b",
            "Professional qualification": r"\b(BSc|MSc|PhD|MD)\b"  # basic examples
        }

        
    def reset_flags(self):
        self.rsa_flag = 0
        self.direct_flag = 0
        self.indirect_flag = 0
        self.potential_indirect_flag = 0 

    def check_regex(self, text):

        for pattern in self.rsa_patterns.values():
            self.rsa_flag += len(re.findall(pattern, text))
        
        if self.rsa_flag:
            return
        

        break_outer = False

        for match_pattern, flag_name in [('direct_patterns', 'direct_flag'), 
                                        ('indirect_patterns', 'indirect_flag'), 
                                        ('potential_indirect_patterns', 'potential_indirect_flag')]:
            
            # Start going through regex patterns 
            for pattern in getattr(self, match_pattern).values():
                
                # Before each new pattern, check if we satisfy exit conditions to know we've found sensitive data
                if self.direct_flag > 0 and (self.indirect_flag > 0 or self.potential_indirect_flag > 0):
                    break_outer = True
                    break

                regex_search = re.search(pattern, text)
                
                if regex_search:
                    current_value = getattr(self, flag_name)
                    setattr(self, flag_name, current_value + 1)

            if break_outer:
                break

        # if self.direct_flag == 0:
        #     self.direct_flag +=  self.has_full_name(text)

        if self.indirect_flag == 0:
            self.indirect_flag += self.has_nationality(text)



    
    def has_full_name(self, text):
        english_nlp = spacy.load('en_core_web_sm')  
        spacy_parser = english_nlp(text)
        names = [ent.text for ent in spacy_parser.ents if ent.label_ == "PERSON"]

        for name in names:
            if len(name.split()) >= 2:
                return 1

        return 0

    def has_nationality(self, text): 
        text = text.lower()
        for nationality in const.NATIONALITIES: 
            if nationality.lower() in text: 
                return 1

        return 0

    def is_sensitive(self, text):
        self.reset_flags()

        # Do some fast regex tests!
        regex_result = self.check_regex(text)
        if regex_result:
            return True

        # print(self.rsa_flag, self.direct_flag, self.indirect_flag, self.potential_indirect_flag)
        return [self.rsa_flag, self.direct_flag, self.indirect_flag, self.potential_indirect_flag] 


