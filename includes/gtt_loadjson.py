
import os
import json
from pymongo import MongoClient
from bson import ObjectId
from langchain.schema import Document

class GTTGetJson:
    # Function to get JSON data from files and process them
    @staticmethod
    def load_jsons():
        print('Exec: GTTGetJson.load_jsons()')

        try:
            
            # Directory path where the JSON files are stored
            directory_path = "./data/json"
            data_array = []  # List to store all the content
            json_data = ""

            # Check if the directory exists
            if not os.path.exists(directory_path):
                raise FileNotFoundError(f"Directory {directory_path} does not exist.")
            
            # Loop through all files in the directory
            for filename in os.listdir(directory_path):
                # Process only .json files
                pdf_data = ""
                if filename.endswith(".json"):
                    file_path = os.path.join(directory_path, filename)
                    
                    print(f"---> Processing file: {file_path}")
                    
                    # Load the JSON data from the file
                    with open(file_path, 'r') as file:
                        content = json.load(file)

                    # Extract the content text (assuming 'content' is a list with one entry)
              
                    
                    json_data = content.get("content", [])

                    if json_data:
                        # Add the content to the data list (appending instead of overwriting)
                        document = Document(page_content=json_data)
                        data_array.append(document)
                        print(f"---> Json loaded successfully: {file_path}")
                    else:
                        print(f"---> No content found in the file: {file_path}")

            # Check if we have loaded any documents
            if not data_array:
                print("---> No documents loaded. Please check the JSON and their content.")
                return {"status": "error", "message": "No documents loaded."}
            
            # Return the loaded documents and success status
            print(f"---> Total documents loaded: {len(data_array)}")
            print(type(data_array))
            # Convert list to dictionary

            return {"status": "success", "message": "Data loaded successfully.", "data": data_array}
          

        except Exception as e:
            print(f"---> An error occurred: {e}")
            return {"status": "error", "message": str(e)}