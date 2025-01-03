import os
from langchain_ollama import OllamaEmbeddings
from langchain.schema import Document

class GTTEmbedding:
    def __init__(self):
        print('Exec: GTTEmbedding.__init__()')
        """
        Initialize with Ollama Embeddings.
        """
        # You should set the `OLLAMA_API_KEY` in your environment variables for authentication
        self.ollama_embeddings = OllamaEmbeddings(model="nomic-embed-text")

    def create_embed(self, text):
        print('Exec: GTTEmbedding.create_embed()')

        embedded_content = self.ollama_embeddings.embed_documents([text])  # Pass a list of strings directly

        return embedded_content
    
    def create_embeddings(self, chunks):
        print('Exec: GTTEmbedding.create_embeddings()')

        # Convert array data to Document format (if using Langchain)
        # Ensure that we are processing only valid strings
        embeddings = []

        for text in chunks:
                # Ensure that the text is a string and directly use the text (no need for Document wrapping)
                embedded_content = self.ollama_embeddings.embed_documents([text.page_content])  # Pass a list of strings directly
            
                # Append the embedding with content to the list
                embeddings.append({
                    'content': text.page_content,
                    'content_embedded': embedded_content[0]  # Assuming the result is a list and we want the first embedding
                })
   
        return embeddings