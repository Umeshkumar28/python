import os
import re
from PyPDF2 import PdfReader
import json

# Function to get input for page number
def get_page_number():
    while True:
        try:
            page_number = int(input("Enter the page number to read: "))
            if page_number <= 0:
                print("Page number must be greater than 0. Please try again.")
            else:
                return page_number - 1
        except ValueError:
            print("Invalid input. Please enter a valid page number.")

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
        if config is None or "regex" not in config:
            print("Error: Configuration file is missing or does not contain the 'regex' key.")
        else:
            regex_pattern = config["regex"]

            page_number = get_page_number()

            try:
                with open(pdf_path, "rb") as pdf_file:
                    reader = PdfReader(pdf_file)

                    if page_number >= len(reader.pages):
                        print(f"Error: Page number {page_number + 1} is out of range. The document has {len(reader.pages)} pages.")
                    else:
                        page_content = reader.pages[page_number].extract_text()

                        # Extract content matching the regular expression
                        matches = re.findall(regex_pattern, page_content, re.MULTILINE)

                        if not matches:
                            print(f"No content matching the regular expression was found on page {page_number + 1}.")
                        else:
                            output_filename = f"page{page_number + 1}.txt"
                            output_path = os.path.join(folder_path, output_filename)

                            with open(output_path, "w", encoding="utf-8") as output_file:
                                output_file.write("\n".join(matches))

                            print(f"Matching content of page {page_number + 1} written to '{output_filename}' successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
