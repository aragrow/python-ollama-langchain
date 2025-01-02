import os
from langchain_ollama import OllamaEmbeddings
from langchain.schema import Document
from langchain_community.vectorstores import Chroma

class GTTEmbedding:
    def __init__(self):
        """
        Initialize with Ollama Embeddings.
        """
        # You should set the `OLLAMA_API_KEY` in your environment variables for authentication
        self.ollama_embeddings = OllamaEmbeddings(model="nomic-embed-text")

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
        

    def store_embeddings(self, embeddings):
        """
        Store the embeddings in a vector database (e.g., Chroma).
        :param embeddings: List of embeddings to store.
        """
        # Create a list of Document objects with both content and embeddings
        documents = []
        for embedding in embeddings:
            doc = Document(page_content=embedding['content'], metadata={'embedding': embedding['content_embedded']})
            documents.append(doc)

        # Now pass the embedding model to Chroma
        # Chroma will internally handle the embeddings based on the documents' content
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.ollama_embeddings,  # Pass the embedding model as the `embedding` argument
            collection_name="concussion_embeddings"
        )
        
        # Optionally, store the embeddings in a persistent database like Chroma (if required)
        vector_store.persist()

        return vector_store