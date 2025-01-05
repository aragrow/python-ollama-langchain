import os
from pymongo import MongoClient, ASCENDING
import numpy as np
from bson import ObjectId
import json
from sklearn.metrics.pairwise import cosine_similarity

class GTTMongoDB:

    def __init__(self, uri="mongodb://localhost:27017/"):
        print('Exec: GTTMongoDB.__init__()')

        """
        Initialize with Ollama Embeddings.
        """
        self.db_name = "concussion_vector_db"
        self.collection_name = "concussion_embeddings"
        self.client = MongoClient(uri)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]  # Create a collection called 'embeddings' 

        # Database and collection names

    def ensure_database_and_collection_exists(self):
        """
        Check if the database and collection exist.
        If not, create them (MongoDB creates the database and collection implicitly when used).
        """
        # Check if database exists
        if self.db_name in self.client.list_database_names():
            print(f"Database '{self.db_name}' exists.")
        else:
            print(f"Database '{self.db_name}' does not exist. It will be created when we use it.")

        # Check if collection exists
        if self.collection_name in self.db.list_collection_names():
            print(f"Collection '{self.collection_name }' exists.")
        else:
            print(f"Collection '{self.collection_name }' does not exist. It will be created.")
            # MongoDB will create the collection when we first insert data into it.
            # Optionally, you can create it manually if needed (though this is usually not necessary):
            self.db.create_collection(self.collection_name)


    def insert_record(self, content, embedding):
        print('Exec: GTTMongoDB.insert_record()')
        """
        Inserts a new document into the MongoDB collection with content and its corresponding embedding.
        """
        record = {
            "content": content,
            "embedding": embedding.tolist(),  # Convert numpy array to list for storage in MongoDB
        }
        self.collection.insert_one(record)

        print(f"Inserted record with content: {content[:30]}...")  # Print the first 30 chars of the content for verification 

    def insert_bulk_inserts(self, embeddings):
        print('Exec: GTTMongoDB.insert_bulk_inserts()')
        """
        Bulk inserts multiple records (content and embeddings) into MongoDB.
        """
        for embed in embeddings[:1]:  # Show first 5 chunks
            print(f"Embed: {embed}")

        try:
            #self.collection.delete_many({})
            records = []
            
            for embed in embeddings:
            
                record = {
                    "_id": ObjectId(),
                    "content": embed['content'],
                    "embedding": embed['content_embedded'],
                }
                records.append(record)

            if records:
                self.collection.insert_many(records)
                print(f"Inserted {len(records)} records.")
            else:
                print("No records to insert.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Optionally close the MongoDB connection when done
            print("Operation completed.")

    # Step 3: Create an Index for Cosine Similarity Search
    def create_vector_indexes(self):
        print('Exec: GTTMongoDB.create_vector_index()')
        
        existing_indexes = self.collection.index_information()

        """
        Creates the necessary indexes for optimized querying.
        """
        # Index for content (optional but useful for text-based queries)
        if "content_index" not in existing_indexes:
            self.collection.create_index([("content", ASCENDING)], name="content_index")

        # Index for embedding (useful for efficient retrieval of embeddings, but note MongoDB can't directly compute similarity)
        if "embedding_index" not in existing_indexes:
            self.collection.create_index([("embedding", ASCENDING)], name="embedding_index")

        print("Indexes created successfully.")

    # Example: Fetch all records from the collection (for testing)
    def fetch_all_records(self):
        print('Exec: GTTMongoDB.fetch_all_records()')

        for record in self.collection.find():
            print(json.dumps(record, indent=2))

    # Function to calculate cosine similarity between the query embedding and stored embeddings
    def retrieve_similar_embeddings(self, query_embedding, top_k=5):
        print('Exec: GTTMongoDB.retrieve_similar_embeddings()')
        """
        Retrieves the most similar embeddings from the MongoDB collection based on cosine similarity.
        """
        # Retrieve all embeddings from the collection
        stored_documents = list(self.collection.find({}))
        stored_embeddings = [np.array(doc['embedding']) for doc in stored_documents]

        # Reshape query_embedding to 2D (1, n_features)
        query_embedding = np.array(query_embedding).reshape(1, -1)

        # Calculate cosine similarities
        similarities = cosine_similarity(query_embedding, stored_embeddings)

        # Sort by descending similarity
        sorted_similarities = np.argsort(similarities[0])[::-1]  # Sort by descending similarity

        # Get top K most similar documents
        similar_docs = []
        for i in range(top_k):
            index = sorted_similarities[i]
            similar_docs.append(stored_documents[index]['content'])

        return similar_docs