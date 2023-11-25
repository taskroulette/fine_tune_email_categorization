import openai
import os
import json

from dotenv import load_dotenv
import yaml


def load_configuration():
    """Load configuration from YAML file and environment variables."""
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    with open("config.yml") as file:
        config = yaml.safe_load(file)

    return config


# Load configuration
config = load_configuration()


def gpt_function_call(email_content):
    try:
        response = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0613:ask-aiden-inc::8OeXrJqc",  # Your fine-tuned model name
            messages=[{"role": "user", "content": email_content}],
            max_tokens=50,  # Adjust as necessary
        )
        print("Raw Response:", response)  # Print the raw response
        if response.choices:
            return response.choices[0].message["content"]
        else:
            return "No response from the model"
    except Exception as e:
        print("Error:", e)
        return str(e)


# Test case
# Adjusted test case to align with the fine-tuning data
def test_case():
    # A test email that closely matches the format used in training
    test_email_content = """
    Email Content: 'Hi Team, I wanted to check on the status of invoice INV-00921. It was supposed to be cleared last week, but I haven't received any confirmation yet. Could you please look into it and provide an update? Best, Jordan'
    Task: Classify the above email in terms of category, label, and whether it is internal or external.
    """
    classification = gpt_function_call(test_email_content)
    print("Test Email Content:", test_email_content)
    print("Classification:", classification)


if __name__ == "__main__":
    test_case()
