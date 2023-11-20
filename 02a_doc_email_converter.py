import re
import json

def parse_email_content(input_text):
    """
    Parses the input text to extract email information and returns a list of email data.
    """
    # Split the input text into separate emails using the '////' delimiter
    email_blocks = input_text.split('////\n\n')

    emails = []

    for block in email_blocks:
        if block.strip():
            # Extracting the details using regular expressions
            category_match = re.search(r'EMAIL \d+ - category: (.+)', block)
            persona_match = re.search(r'Persona: (.+)', block)
            sender_name_match = re.search(r'Sender name: (.+)', block)
            sender_email_match = re.search(r'Sender email: (.+)', block)
            date_match = re.search(r'Date: (.+)', block)
            content_match = re.search(r'Content: \n\n([\s\S]+)', block)

            # Extracted details
            email_data = {
                'category': category_match.group(1).strip() if category_match else None,
                'persona': persona_match.group(1).strip() if persona_match else None,
                'sender_name': sender_name_match.group(1).strip() if sender_name_match else None,
                'sender_email': sender_email_match.group(1).strip() if sender_email_match else None,
                'date': date_match.group(1).strip() if date_match else None,
                'content': content_match.group(1).strip() if content_match else None
            }

            emails.append(email_data)

    return emails

def create_jsonl_file(emails, output_file_path):
    """
    Converts a list of emails to JSON Lines format and writes to a file.
    """
    with open(output_file_path, 'w') as file:
        for email in emails:
            json_line = json.dumps(email)
            file.write(json_line + '\n')

def read_email_content_from_file(file_path):
    """
    Reads email content from a specified text file and returns it as a string.
    """
    with open(file_path, 'r') as file:
        return file.read()

email_file_path = r'data/emails_xochi.txt'

# Read the email content from the file
input_text = read_email_content_from_file(email_file_path)

# Parse the email content
parsed_emails = parse_email_content(input_text)

# Specify the output path for the JSONL file
output_jsonl_file_path = 'data/emails.jsonl' 

# Create the JSONL file with the parsed email content
create_jsonl_file(parsed_emails, output_jsonl_file_path)

print(f"JSONL file created at {output_jsonl_file_path}")