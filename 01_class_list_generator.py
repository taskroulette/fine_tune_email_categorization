import openai
import os
import yaml
from dotenv import load_dotenv

def load_configuration():
    """Load configuration from YAML file and environment variables."""
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    with open('config.yml') as file:
        config = yaml.safe_load(file)
    
    return config

config = load_configuration()

def gpt_call(prompt, model, setup_pydantic, how_many_examples):
    """Make a call to the OpenAI GPT model and return the response."""
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": setup_pydantic},
            {"role": "system", "content": f"list you generate will have {how_many_examples} examples. not more not less."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        stream=True  
    )

    responses = ''
    for chunk in response:
        response_content = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
        responses += response_content
        print(response_content, end='', flush=True)

    return responses

def add_code_to_file(code, prompt, generated_file_name):
    """Add generated code to a new file."""
    try:
        new_content = f"# Generated Code\n{code}\n\n# Prompt Template String\nprompt_template_str = \"{prompt}\"\n"
        with open(generated_file_name, 'w') as file:
            file.write(new_content)
    except IOError as e:
        print(f"Error accessing file: {e}")

# Main execution
if __name__ == "__main__":
    gpt_config = config['gpt_config']
    file_config = config['file_config']
    base_prompt = gpt_config['prompt']

    response = gpt_call(base_prompt, gpt_config['model'], config['prompt_messages']['setup_pydantic'], gpt_config['how_many_examples'])
    code = response.split("```python")[1].split("```")[0]
    
    new_generated_file_name = "generated_code.py"
    add_code_to_file(code, base_prompt, new_generated_file_name)
