#  Data Extraction using Regex

This is a python regex validator program used to extract different data types in raw text.

## I choosed these data types

 4 data types:

- Email addresses
- Credit card numbers
- Hashtags
- Times

## File Structure

```text
input/
  raw-text.txt
src/
  main.py
output/
  sample-output.json
README.md
```

## All regex validations
 
- All email addresses are separated into official ALU emails, alumni emails and SI emails.
- I used luhn algorithm to validate credit cards numbers.
- Invalid credit cards are rejected.
- The program also hides credit card numbers leaving the last 4 digits only.
- All lines containing `<script>` or `DROP TABLE` are ignored to prevent malcious and injected inputs.
- Time is extracted in both 24 hours and 12 hours format and also rejects all invalid hours in AM/PM format.
- The program also removes duplicates like hashtags i.e #Nissitech and #Nissitech  
## How to Run

```bash
python src/main.py
```

all the results are saved in:

```text
output/sample-output.json
```
