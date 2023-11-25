from llama_index.finetuning import OpenAIFinetuneEngine
import openai
import os
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

finetune_engine = OpenAIFinetuneEngine(
    "gpt-3.5-turbo",
    "data/fine_tuning_dataset_py.jsonl",
    # start_job_id="<start-job-id>"
    validate_json=False,
)

finetune_engine.finetune()

print(finetune_engine.get_current_job())
