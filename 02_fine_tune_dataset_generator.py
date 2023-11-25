import os
import openai
from dotenv import load_dotenv
import yaml
from pydantic import BaseModel, EmailStr


from llama_index.llms import OpenAI
from llama_index.callbacks import OpenAIFineTuningHandler
from llama_index.callbacks import CallbackManager
from llama_index.program import OpenAIPydanticProgram

# Importing classes and list from generated_code.py
from generated_code import Email, EmailCategory, EmailContent, email_categories


def load_configuration():
    """Load configuration from YAML file and environment variables."""
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    with open("config.yml") as file:
        config = yaml.safe_load(file)

    return config


config = load_configuration()

# Update the prompt template to use YAML.
prompt_template_str = f"Generate 30 unique mock email contents with diverse sender names and email addresses. For each email, randomly select a topic from the provided categories in {email_categories} and craft an email body related to that category. Ensure a 50/50 split between internal (emails ending with @askaiden.com) and external emails. Each email should be unique in terms of sender information, subject line, and content. No sender name, email address, or email body should be repeated. The subject lines should be indicative of the category and the content should discuss a specific issue, strategy, or question relevant to the chosen category. Please diversify the contents to cover a wide range of topics and avoid repetition."
# prompt_template_str = config['run_requests']['prompt_template_str']


# Grab LLM model from config
llm_model = config["gpt_config"]["model"]

finetuning_handler = OpenAIFineTuningHandler()
callback_manager = CallbackManager([finetuning_handler])

llm = OpenAI(model=llm_model, callback_manager=callback_manager)


# Function to extract class and list names
def get_class_and_list_names(filename="generated_code.py"):
    with open(filename, "r") as file:
        content = file.read()

    class_names = [
        line.split()[1]
        for line in content.splitlines()
        if line.strip().startswith("class ")
    ]

    if not class_names:
        raise Exception("No classes found in the file.")

    output_class_name = class_names[-1].split("(")[0]

    list_name_lines = [
        line for line in content.splitlines() if "=" in line and "[" in line
    ]

    if not list_name_lines:
        raise Exception("No list definitions found in the file.")

    list_name = list_name_lines[0].split()[0]

    return output_class_name, list_name


# Rest of the code for class and list name extraction

output_cls_name, list_name = get_class_and_list_names()
output_cls = globals()[output_cls_name]
list_name = globals()[list_name]

print("Length of list:", len(list_name))
if list_name:
    print("First few items in the list:", list_name[:5])
else:
    print("The list is empty.")

program = OpenAIPydanticProgram.from_defaults(
    output_cls=output_cls,
    prompt_template_str=prompt_template_str,
    llm=llm,
    verbose=False,
)

# writing to JSONL file
for list_item in list_name:
    try:
        output = program(list_item=list_item)
        print(output.json())
        finetuning_handler.save_finetuning_events("data/seq_finetune_dataset.jsonl")
    except Exception as e:
        print(f"Error processing {list_item}: {e}")
