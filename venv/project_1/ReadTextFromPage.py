import os
from PyPDF2 import PdfReader

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


folder_path = os.path.join(os.path.dirname(__file__),"content")
pdf_filename = "Chemistry Questions.pdf"
output_filename = os.path.join(folder_path,"page.txt")


if not os.path.exists(folder_path):
    print(f"Error: Folder '{folder_path}' does not exist.")
else:
    pdf_path = os.path.join(folder_path, pdf_filename)



    if not os.path.isfile(pdf_path):
        print(f"Error: PDF file '{pdf_filename}' not found in the folder.")
    else:

        page_number = get_page_number()

        try:
            with open(pdf_path, "rb") as pdf_file:
                reader = PdfReader(pdf_file)

                if page_number >= len(reader.pages):
                    print(f"Error: Page number {page_number + 1} is out of range. The document has {len(reader.pages)} pages.")
                else:
                    page_content = reader.pages[page_number].extract_text()
                    output_filename = f"page{page_number + 1}.txt"
                    output_path = os.path.join(folder_path, output_filename)

                    with open(output_path, "w", encoding="utf-8") as output_file:
                        output_file.write(page_content)

                    print(f"Content of page {page_number + 1} written to '{output_filename}' successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
