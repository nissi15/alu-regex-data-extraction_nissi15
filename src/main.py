#!/usr/bin/env python3

import json
import re
from pathlib import Path

# paths of the input and output files
raw_text_file = Path("input/raw-text.txt")
sample_json_file = Path("output/sample-output.json")

# regex commands for our data types
hashtag_regex = r"#[A-Za-z0-9_]+\b"
time_regex = r"(?<!:)\b(?:(?:0?[1-9]|1[0-2]):[0-5]\d\s*[AP]M|(?:[01]?\d|2[0-3]):[0-5]\d(?!\s*[AP]M))\b(?!:)"
email_regex= r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
credit_card_regix = r"\b(?:\d{4} \d{4} \d{4} \d{4}|\d{4}-\d{4}-\d{4}-\d{4}|\d{4} \d{6} \d{5}|\d{4}-\d{6}-\d{5}|\d{13,19})\b"


#checking if we have no unsafe text
def unsafe(text):
    if "<script>" not in text.lower() and "drop table" not in text.lower():
        return True

# Using the luhn algorithm to check the cards. where it reverses digits and doubles the 2nd digit(minus 9 when 2 numbers ) and adds everything 
# if the total is divisible by 10 then the card is real

def check_hide_card(card):
    numbers = re.sub(r"\D", "", card)
    total = 0
    reverse_numbers = numbers[::-1]

    for i in range(len(reverse_numbers)):
        num = int(reverse_numbers[i])
        if i % 2 == 1:
            num = num * 2
            if num > 9:
                num = num - 9
        total += num

    # hiding the card digits
    hide_card = "*" * (len(numbers) - 4) + numbers[-4:]

    if len(set(numbers)) > 1 and total % 10 == 0: #checking for duplicate numbers and also card passes luhn method
        return hide_card, True
    else:
        return hide_card, False


