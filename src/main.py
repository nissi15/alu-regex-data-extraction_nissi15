#!/usr/bin/env python3

import json
import re
from pathlib import Path

# paths of the input and output files
raw_text_file = Path("input/raw-text.txt")
sample_json_file = Path("output/sample-output.json")

# regex commands for our data types
hashtag_regex = r"#[A-Za-z0-9_]+\b"
time_regex = r"(?<!:)\b(?:(?:0?[1-9]|1[0-2]):[0-5]\d\s*[AP]M|(?:[01]?\d|2[0-3]):[0-5]\d(?!\s*[AP]M))\b(?!:)" # both 12 and 24 formats
alu_official_regex =  r"\b[A-Za-z0-9._%+-]+@alueducation\.com\b"
alu_alumni_regex = r"\b[A-Za-z0-9._%+-]+@alumni\.alueducation\.com\b"
alu_si_regex =r"\b[A-Za-z0-9'_%+-]+@si\.alueducation\.com\b"
credit_card_regex = r"\b(?:\d{4} \d{4} \d{4} \d{4}|\d{4}-\d{4}-\d{4}-\d{4}|\d{4} \d{6} \d{5}|\d{4}-\d{6}-\d{5}|\d{13,19})\b"  

Unsafe_regex = r"^.*(?:<script|drop\s+table).*$\n?"

#checking if we have no unsafe text
def unsafe(text):
    return not re.search(r"<script|drop\s+table", text, re.IGNORECASE)
    
# Using the luhn algorithm to check the if the cards are real.
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

# Extracting data: emails , creditcards , time and hashtags
def validating(all_text):
    Output = {
        "hashtags": [],
        "times": [],
        "credit_cards": [],
        "rejected_cards": [],
        "alu_official_emails": [],
        "alu_alumni_mails": [],
        "alu_si_emails": []
    }
    
    safe_text = re.sub(Unsafe_regex, "", all_text, flags=re.IGNORECASE | re.MULTILINE)
    for card in re.findall(credit_card_regex, safe_text):
        hide_card, valid = check_hide_card(card)
        if valid:
            if hide_card not in Output["credit_cards"]:
                Output["credit_cards"].append(hide_card)
        else:
            if hide_card not in Output["rejected_cards"]:
                Output["rejected_cards"].append(hide_card)

    #extracting all 3 alu emails
    Output["alu_si_emails"] = removing_duplicate(re.findall(alu_si_regex, safe_text, re.IGNORECASE))
    Output["alu_official_emails"] = removing_duplicate(re.findall(alu_official_regex,safe_text, re.IGNORECASE))
    Output["alu_alumni_mails"] = removing_duplicate(re.findall(alu_alumni_regex, safe_text, re.IGNORECASE))
    #exract hastags and times
    Output["hashtags"] = removing_duplicate(re.findall(hashtag_regex, safe_text))
    Output["times"] = removing_duplicate(re.findall(time_regex, safe_text, re.IGNORECASE))
    
    return Output

# saving the output to our json file
def saving_json(text):
    sample_json_file.parent.mkdir(exist_ok=True)
    sample_json_file.write_text(json.dumps(text, indent=4), encoding="utf-8")

def main():
    input_text = raw_text_file.read_text(encoding="utf-8")
    results = validating(input_text)
    saving_json(results)
    print("         SUMMARY")
    print("=" * 50)
    print(f"I saved all the output details at: {sample_json_file}")


if __name__ == "__main__":
    main()
