import os
import pdfplumber
from langchain.schema import Document

class GTTLoadPDFs:
    # Function to load PDFs and process them into documents
    @staticmethod
    def load_pdfs():
        print('Exec: GTTLoadPDFs.load_pdfs()')

        data_array = []  # List to store the documents
        directory_path = "./data/pdf"

        try:
            # Check if the directory exists
            if not os.path.exists(directory_path):
                raise FileNotFoundError(f"Directory {directory_path} does not exist.")

            # Loop through all files in the subdirectory
            for filename in os.listdir(directory_path):
                if filename.endswith(".pdf"):
                    # Construct the full file path for the PDF
                    local_path = os.path.join(directory_path, filename)
                    print(f"---> Found PDF file: {local_path}")

                    try:
                        # Open the PDF file using pdfplumber
                        with pdfplumber.open(local_path) as pdf:
                            pdf_data = ""
                            for page in pdf.pages:
                                text = page.extract_text()
                                if text:  # Only append non-empty text
                                    pdf_data += text

                        # Check if pdf_data is empty or None
                        if pdf_data:
                            # Convert the raw text to a Document object
                            document = Document(page_content=pdf_data)
                            # Append the document to data_array
                            data_array.append(document)
                            print(f"---> PDF loaded successfully: {local_path}")
                        else:
                            print(f"---> Warning: No data extracted from PDF {local_path}")
                    except Exception as e:
                        # Handle errors during PDF processing
                        print(f"---> Error loading PDF {local_path}: {str(e)}")
                else:
                    print(f"---> Skipping non-PDF file: {filename}")

            # Check if we have loaded any documents
            if not data_array:
                print("---> No documents loaded. Please check the PDFs and their content.")
                return {"status": "error", "message": "No documents loaded."}

            # Return the loaded documents and success status
            print(f"---> Total documents loaded: {len(data_array)}")
            print(type(data_array))
            exit
            return {"status": "success", "message": "Data loaded successfully.", "data": data_array}

        except Exception as e:
            # General error handling for any other unexpected errors
            print(f"---> Error occurred: {str(e)}")
            return {"status": "error", "message": str(e)}
