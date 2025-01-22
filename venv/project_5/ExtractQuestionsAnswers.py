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

# Function to create and initialize the database
def create_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT,
                answer_options TEXT,
                answer TEXT,
                answer_text TEXT
            )
        ''')

        conn.commit()
        conn.close()
        print(f"Database initialized at {db_path}")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        raise

# Function to insert question data into the database
def insert_question(db_path, question_text, answer_options, answer, answer_text):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO questions (question_text, answer_options, answer, answer_text)
                          VALUES (?, ?, ?, ?)''',
                       (question_text, answer_options, answer, answer_text))

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error inserting data into the database: {e}")

def view_questions(db_path):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute a query to select all data from the questions table
        cursor.execute("SELECT * FROM questions")

        # Fetch all results from the query
        rows = cursor.fetchall()

        # Print each row (or process as needed)
        for row in rows:
            print(f"Question: {row[1]} \n{row[2]} \n{row[3]}{row[4]}")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()

# Function to process and extract questions from the PDF
def extract_and_store_questions(pdf_path, regex_pattern, db_path, flags):
    try:
        with open(pdf_path, "rb") as pdf_file:
            reader = PdfReader(pdf_file)

            for page_num, page in enumerate(reader.pages):
                page_content = page.extract_text()

                # Extract content matching the regular expression
                matches = re.finditer(regex_pattern, page_content, flags)

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

                        # Store the question data in the database
                        insert_question(db_path, question_text, answer_options, answer, answer_text)

                    page_num += 1
            print(f"Processed pages {page_num} and stored questions.")
            view_questions(db_path)
    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")
        raise

# Main execution
folder_path = os.path.join(os.path.dirname(__file__), "content")
pdf_filename = "Chemistry Questions.pdf"
config_filename = "config.json"
config_path = os.path.join(folder_path, config_filename)
db_filename = "questions.db"
db_path = os.path.join(folder_path, db_filename)

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
            flags = re.IGNORECASE if config.get("flags", "") == "i" else 0  # Apply case-insensitive flag if specified

            # Initialize or create the database
            try:
                create_db(db_path)

                # Extract questions from the PDF and store them in the database
                extract_and_store_questions(pdf_path, regex_pattern, db_path, flags)

            except Exception as e:
                print(f"Error occurred during DB setup or extraction: {e}")