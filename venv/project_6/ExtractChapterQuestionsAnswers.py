import os
import re
import sqlite3
from PyPDF2 import PdfReader
import json

# Function to load configuration
def load_config(config_path):
    if not os.path.exists(config_path):
        print(f"Error: Configuration file '{config_path}' does not exist.")
        return None
    try:
        with open(config_path, 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)
            if not isinstance(config, dict):
                print(f"Error: Configuration file '{config_path}' does not contain a valid JSON object.")
                return None
            return config
    except json.JSONDecodeError as jde:
        print(f"Error: Configuration file '{config_path}' is not valid JSON: {jde}")
    except Exception as e:
        print(f"Error: Failed to load configuration file: {e}")
    return None

# Function to process and extract questions from the PDF
def extract_and_chapter_and_question(pdf_path,config):
    chapter_name = input("Enter chapter name:")
    if config is None or "question_regex_pattern" not in config:
        print("Error: Configuration file is missing or does not contain the 'question_regex_pattern' key.")
    else:
        question_regex_pattern = config["question_regex_pattern"]
        flags = re.IGNORECASE if config.get("flags", "") == "i" else 0  # Apply case-insensitive flag if specified

    if config is None or "chapter_regex_pattern" not in config:
        print("Error: Configuration file is missing or does not contain the 'chapter_regex_pattern' key.")
    else:
        chapter_regex_pattern = config["chapter_regex_pattern"].replace("{chapter_name}", re.escape(chapter_name))


    try:
        with open(pdf_path, "rb") as pdf_file:
            reader = PdfReader(pdf_file)
            extracted_text = ""

            for page in reader.pages:
                extracted_text += page.extract_text() + "\n"

            chapter_content = re.search(chapter_regex_pattern,extracted_text,re.DOTALL)

            if not chapter_content:
                print(f"No content found for chapter:{chapter_name}")
                return

            chapter_text = chapter_content.group(1)

            # Extract content matching the regular expression
            matches = re.finditer(question_regex_pattern, chapter_text, flags | re.MULTILINE)

            if not matches:
                print(f"No content matching the regular expression found on page {page_num + 1}.")
            else:
                for match in matches:
                    question_text = match.group('question').strip()
                    answer = "Answer: "+match.group('answer').strip()
                    answer_text = ") "+match.group('answer_text').strip()

                    options = []
                    options_text = match.group('options').strip().split("\n")
                    for option in options_text:
                        if option:
                            options.append(option.strip())

                    answer_options = "\n".join(options)
                    print(f"{question_text}\n{answer_options}\n{answer}{answer_text}")
    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")
        raise

# Main execution
folder_path = os.path.join(os.path.dirname(__file__), "content")
pdf_filename = "Chemistry Questions.pdf"
config_filename = "config.json"
config_path = os.path.join(folder_path, config_filename)

if not os.path.exists(folder_path):
    print(f"Error: Folder '{folder_path}' does not exist.")
else:
    pdf_path = os.path.join(folder_path, pdf_filename)

    if not os.path.isfile(pdf_path):
        print(f"Error: PDF file '{pdf_filename}' not found in the folder.")
    else:
        config = load_config(config_path)
        extract_and_chapter_and_question(pdf_path,config)