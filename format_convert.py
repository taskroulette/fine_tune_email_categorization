import json
import click

# Function to convert a single line of input JSON to the desired output format
def convert_line_modified(input_line):
    category = input_line['category']
    sender_name = input_line['sender_name']
    sender_email = input_line['sender_email']
    content = input_line['content']

    # Constructing the email subject and body
    first_line = content.split('\n')[0]
    email_subject = f"{category}: {first_line}"
    email_body = f"{content}\n\nBest,\n{sender_name}\n{sender_email}"

    # Creating the user and assistant messages
    user_message = {
        "role": "user",
        "content": f"Please draft an email regarding {category.lower()}."
    }
    assistant_message = {
        "role": "assistant",
        "function_call": {
            "name": "EmailContent",
            "arguments": {
                "subject": email_subject,
                "body": email_body
            }
        }
    }

    # Constructing the final output structure
    output_structure = {
        "messages": [user_message, assistant_message],
        "functions": [
            {
                "name": "EmailContent",
                "description": "Function to draft an email content.",
                "parameters": {
                    "title": "EmailContent",
                    "description": "Function to draft an email content.",
                    "type": "object",
                    "properties": {
                        "subject": {"title": "Subject", "type": "string"},
                        "body": {"title": "Body", "type": "string"}
                    },
                    "required": ["subject", "body"]
                }
            }
        ]
    }

    return output_structure

# Click command to process the file
@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
def process_file_modified(input_file, output_file):
    with open(input_file, "r") as file, open(output_file, "w") as outfile:
        for line in file:
            input_line = json.loads(line)
            output_line = convert_line_modified(input_line)
            json.dump(output_line, outfile)
            outfile.write('\n')  # Write a newline character after each JSON object

if __name__ == "__main__":
    process_file_modified()
