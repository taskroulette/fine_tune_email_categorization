import click
import re
import json

# Function to determine if an email is internal or external
def is_internal_email(email_address):
    return email_address.endswith('@askaiden.com')

# Function to parse each email and extract relevant information
def parse_email(email_str):
    category_match = re.search(r'Category: (.+)', email_str)
    label_match = re.search(r'Label: "(.+)"', email_str)
    sender_email_match = re.search(r'Sender email: (.+)', email_str)
    content_start_index = email_str.find('Content:') + len('Content:')

    category = category_match.group(1).strip() if category_match else None
    label = label_match.group(1).strip() if label_match else None
    sender_email = sender_email_match.group(1).strip() if sender_email_match else None
    content = email_str[content_start_index:].strip()

    internal = is_internal_email(sender_email) if sender_email else False

    return {
        "category": category,
        "label": label,
        "content": content,
        "internal": internal
    }

# Function to convert parsed email data to the specified JSONL format
def convert_to_jsonl_format(email_data):
    jsonl_entries = []

    for email in email_data:
        json_entry = {
            "messages": [
                {
                    "role": "user",
                    "content": email["content"]
                },
                {
                    "role": "assistant",
                    "function_call": {
                        "name": "ClassifyEmail",
                        "arguments": {
                            "category": email["category"],
                            "label": email["label"],
                            "internal": email["internal"]
                        }
                    }
                }
            ],
            "functions": [
                {
                    "name": "ClassifyEmail",
                    "description": "Classify the email into a category and label, and determine if it's internal or external.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {"type": "string"},
                            "label": {"type": "string"},
                            "internal": {"type": "boolean"}
                        },
                        "required": ["category", "label", "internal"]
                    }
                }
            ]
        }
        jsonl_entries.append(json_entry)
    
    return jsonl_entries

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', default='output_file.jsonl', help='Output JSONL file path.')
def main(file_path, output):
    with open(file_path, 'r') as file:
        email_text = file.read()

    emails = email_text.split('////')[1:]  # Splitting the text into individual emails
    parsed_emails = [parse_email(email) for email in emails]
    converted_jsonl = convert_to_jsonl_format(parsed_emails)

    # Save the JSONL data to a file
    with open(output, 'w') as output_file:
        for entry in converted_jsonl:
            output_file.write(json.dumps(entry) + '\n')

    click.echo(f"Processed data saved to {output}")

if __name__ == '__main__':
    main()
