import os
import PyPDF2

base_folder = os.path.join(os.path.dirname(__file__), "content")
subfolders = ["One", "Two", "Three"]
output_filename = "output.txt"

if not os.path.exists(base_folder):
    print(f"Error: Base folder '{base_folder}' does not exist.")
else:
    for subfolder in subfolders:
        subfolder_path = os.path.join(base_folder, subfolder)

        if not os.path.exists(subfolder_path):
            print(f"Subfolder '{subfolder_path}' does not exist. Creating it.")
            os.makedirs(subfolder_path)

        pdf_files = [f for f in os.listdir(subfolder_path) if f.lower().endswith(".pdf")]

        if not pdf_files:
            print(f"No PDF files found in '{subfolder_path}'.")
        else:
            all_content = ""
            for pdf_file in pdf_files:
                pdf_path = os.path.join(subfolder_path, pdf_file)
                try:
                    with open(pdf_path, "rb") as pdf_file_obj:
                        reader = PyPDF2.PdfReader(pdf_file_obj)
                        for page in reader.pages:
                            all_content += page.extract_text() + "\n"
                except Exception as e:
                    print(f"Error reading PDF file '{pdf_path}': {e}")


            output_path = os.path.join(subfolder_path, output_filename)
            try:
                with open(output_path, "w", encoding="utf-8") as output_file:
                    output_file.write(all_content)
                print(f"Content written to '{output_path}' successfully.")
            except Exception as e:
                print(f"Error writing to '{output_path}': {e}")
