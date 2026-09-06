#  Data Extraction using Regex

This program extracts data from a raw text file using python and regex commands

## Data Types Used

The program extracts 4 data types:

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

## Validation
 
- All email addresses are separated into all valid emails, official ALU emails, alumni emails and SI emails.
- I used luhn algorithm to validate credit cards numbers of multiple lengths.
- Invalid credit cards are rejected.
- The program also hides credit card numbers leaving the last 4 digits only.
- All lines containing `<script>` or `DROP TABLE` are ignored to prevent malcious and injected inputs.
- Time is extracted in both 24 hours and 12 hours format and also rejects all invalid hours in AM/PM format.
- The program also removes duplicates like hashtags and other data types
## How to Run

```bash
python src/main.py
```

The result is saved in:

```text
output/sample-output.json
```
