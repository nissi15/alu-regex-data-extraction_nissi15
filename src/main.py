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
credit_card_regex = r"\b(?:\d{4} \d{4} \d{4} \d{4}|\d{4}-\d{4}-\d{4}-\d{4}|\d{4} \d{6} \d{5}|\d{4}-\d{6}-\d{5}|\d{13,19})\b"


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

def removing_duplicate(text):
    texts = set()
    proper_text = []
    for i in text:
        if i not in texts:
            texts.add(i)
            proper_text.append(i)
    return proper_text

ALU_OFFICIAL = "@alueducation.com"
ALU_ALUMNI = "@alumni.alueducation.com"
ALU_SI = "@si.alueducation.com"

# validating our raw data: emails , creditcards , time and hashtags
def validating(all_text):
    safe_text = ""
    Output = {
        "hashtags": [],
        "time": [],
        "credit_cards": [],
        "rejected_cards": [],
        "emails": {
            "all_valid": [],
            "alu_official": [],
            "alu_alumni": [],
            "alu_si": []
        },
    }

    for text in all_text.splitlines():
        if unsafe(text):
            safe_text += text + "\n"

    # extracting emails
    for email in re.findall(email_regex, safe_text):
        email_lower = email.lower()
        if email not in Output["emails"]["all_valid"]:
            Output["emails"]["all_valid"].append(email)

        if email_lower.endswith(ALU_OFFICIAL):
            if email not in Output["emails"]["alu_official"]:
                Output["emails"]["alu_official"].append(email)
        elif email_lower.endswith(ALU_ALUMNI):
            if email not in Output["emails"]["alu_alumni"]:
                Output["emails"]["alu_alumni"].append(email)
        elif email_lower.endswith(ALU_SI):
            if email not in Output["emails"]["alu_si"]:
                Output["emails"]["alu_si"].append(email)

    for card in re.findall(credit_card_regex, safe_text):
        hide_card, valid = check_hide_card(card)

        if valid:
            if hide_card not in Output["credit_cards"]:
                Output["credit_cards"].append(hide_card)
        else:
            if hide_card not in Output["rejected_cards"]:
                Output["rejected_cards"].append(hide_card)

    Output["hashtags"] = removing_duplicate(re.findall(hashtag_regex, safe_text))
    Output["times"] = removing_duplicate(re.findall(time_regex, safe_text, re.IGNORECASE))

    return Output

