import os
import PyPDF2

# Define folder and file paths
folder_path = os.path.join(os.path.dirname(__file__), "content")
pdf_filename = "Chemistry Questions.pdf"
output_filename = os.path.join(os.path.dirname(__file__),"output.txt")

# Ensure the folder exists
if not os.path.exists(folder_path):
    print(f"Error: Folder '{folder_path}' does not exist.")
else:
    pdf_path = os.path.join(folder_path, pdf_filename)
    output_path = os.path.join(folder_path, output_filename)

    # Check if the PDF file exists
    if not os.path.isfile(pdf_path):
        print(f"Error: PDF file '{pdf_filename}' not found in the folder.")
    else:
        try:
            # Read the PDF file
            with open(pdf_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                content = ""
                for page in reader.pages:
                    content += page.extract_text()

            # Write the content to a text file
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write(content)

            print(f"Content written to '{output_filename}' successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
