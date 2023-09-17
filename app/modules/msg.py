# Python script for msg

import extract_msg
import numpy as np

from const import *

def is_sensitive(filename, detector = None): 

    msg = None

    for encoding in ENCODINGS: 
        try:
            msg = extract_msg.Message(filename, overrideEncoding=encoding)
            break
        except Exception:
            pass

    body = (msg.body + msg.subject).lower()
    body = re.sub(PATTERN_NEWLINE, " ", body)
    body = re.sub(PATTERN_WHITESPACE, " ", body)

    recipients = [recipient.name for recipient in msg.recipients]

    msg.close()

    # Check 1: Pair of email and same name in body
    for recipient in recipients: 
        names = recipient.split("@")
        if len(names) > 1: 
            names = names[0].split(".")
            count = sum([name in body for name in names])

            if count > 1: 
                print("Check (COUNT)")
                return True

    # Check 2: Check for another clue
    clues = np.array(detector.is_sensitive(body)).sum()
    return clues >= 1 and len(recipients) > 0