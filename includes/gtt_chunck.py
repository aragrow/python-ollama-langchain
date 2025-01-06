
import os
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import sys

class GTTChunking:
    # Function to load PDFs and process them into documents
    @staticmethod
    def chunk_text(data_array):
        print('Exec: GTTChunking.chunk_text()') 

        # Extracting the 'page_content' from each document inside the data array
        # Handling case where 'data' key may be a list of documents, and document itself has page content
        documents = []

        for doc in data_array:
            # Ensure that we only use 'page_content' from the document
            if isinstance(doc, Document):
                print('Is Document.')
                documents.append(doc)
            else:
                print('Is No document.')
    
        # Check the length of documents
        print(f"Documents extracted: {len(documents)}")

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = text_splitter.split_documents(documents)
        print(f"Text split into {len(chunks)} chunks")

        return chunks