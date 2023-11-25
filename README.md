# Fine Tune GPT 3.5 for text classification

## Project Overview

This project is focused on fine-tuning an AI model (specifically a GPT variant) to categorize emails. It involves preparing datasets, fine-tuning the model, and testing its ability to classify emails into predefined categories, labels, and identify whether they are internal or external.


## Usage

    ~~Dataset Preparation: Use `02_fine_tune_dataset_generator.py` to generate the dataset for fine-tuning~~
    * Fine-Tuning: Run `03_finetuning.py`` to fine-tune the model with the prepared dataset.
    * Testing: After fine-tuning, use `04_test_finetuned.py` to test the model's email categorization capability.