from llama_index.finetuning import OpenAIFinetuneEngine
import openai
import os
from dotenv import load_dotenv
import yaml

def load_configuration():
    """Load configuration from YAML file and environment variables."""
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    with open('config.yml') as file:
        config = yaml.safe_load(file)
    
    return config

# Load configuration
config = load_configuration()

# # Initialize the Fine-Tuning Engine
# finetune_engine = OpenAIFinetuneEngine(
#     "gpt-3.5-turbo",
#     "data/fine_tuning_dataset_py.jsonl",
# )

# finetune_job = finetune_engine.finetune()

# print(finetune_job)

from llama_index.finetuning import OpenAIFinetuneEngine
import time
import openai
import os

# openai.api_key = os.getenv("OPENAI_API_KEY") or "YOUR_API_KEY HERE"

finetune_engine = OpenAIFinetuneEngine(
    "gpt-3.5-turbo",
    "data/fine_tuning_dataset_py.jsonl",
    # start_job_id="<start-job-id>"  # if you have an existing job, can specify id here
    validate_json=False,  # openai validate json code doesn't support function calling yet
)

finetune_engine.finetune()

print(finetune_engine.get_current_job())


### BELOW IS  LLAMA INDEX WAY OF MAKING CALLS TO THE FINE TUNED MODEL BUT YOU HAVE TO RUN THIS RIGHT AFTER THE FINE TUNING IN THE SAME FILE AS IT IS CURRENTLY ###
### WE HAVE THE USE_FINE_TUNE.PY FILE FOR THIS PURPOSE ###

# from llama_index.llms import OpenAI
# from llama_index.callbacks import OpenAIFineTuningHandler
# from llama_index.callbacks import CallbackManager
# from llama_index.program import OpenAIPydanticProgram

# ### !!! Make sure the classes and list under the below comment is cleared before running class_list_generator.py !!! ###
# # CLASSES AND LIST UNDER HERE

# from pydantic import BaseModel
# from typing import List

# class Answer(BaseModel):
#     """Data model for an answer."""

#     answer_text: str


# class Question(BaseModel):
#     """Data model for a question."""

#     question_text: str
#     answers: List[Answer]

# finetune_engine = OpenAIFinetuneEngine()

# prompt_template_str = "generate interesting python questions and answers based on the {list_item}"


# ft_llm = finetune_engine.get_finetuned_model(model_id="ft:gpt-3.5-turbo-0613:memo-ai::87tf0dOR",temperature=0.3)

# ft_program = OpenAIPydanticProgram.from_defaults(
#     output_cls=Question,
#     prompt_template_str=prompt_template_str,
#     llm=ft_llm,
#     verbose=False,
# )

# ft_program(topic="List Comprehensions")
