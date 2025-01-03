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
        self.uri = uri
        self.client = MongoClient(uri)
        self.db = self.client['vector_db']
        self.collection = ''

    def connect_to_mongodb(self):
        print('Exec: GTTMongoDB.connect_to_mongodb()')

        # Connect to MongoDB
        self.collection = self.db['concussion_embeddings']  # Create a collection called 'embeddings'


    def insert_record(self, content, embedding):
        print('Exec: GTTMongoDB.insert_record()')

        record = {
            "_id": ObjectId(),  # Explicitly setting a unique ID (optional, as MongoDB does this by default)
            "content": content,
            "embedding": embedding.tolist(),  # Convert numpy array to a list
        }
        self.collection.insert_one(record)
        print(f"Inserted record with content: {content[:30]}...")  # Print the first 30 chars of the content for verification 

    def insert_bulk_inserts(self, embeddings):
        print('Exec: GTTMongoDB.insert_bulk_inserts()')

        # List to hold all the records for bulk insert
        records = []

        # Loop through the embeddings list, assuming each item is a tuple (content, embedding)
        for content, embedding in embeddings:
            # Create the record for each embedding
            record = {
                "_id": ObjectId(),  # Explicitly setting a unique ID (optional, as MongoDB does this by default)
                "content": content,
                "embedding": embedding.tolist(),  # Convert numpy array to a list if needed
            }
            records.append(record)

        # Insert all records in one go (bulk insert)
        self.collection.insert_many(records)  # Efficient bulk insert
        print(f"Inserted {len(records)} records")

    # Step 3: Create an Index for Cosine Similarity Search
    def create_vector_index(self):
        print('Exec: GTTMongoDB.create_vector_index()')

        # Create an index on the 'embedding' field for cosine similarity search
        # MongoDB does not natively support vector search out of the box.
        # However, for a simple use case, we can store vectors and later use cosine similarity in application logic.
        # Alternatively, use MongoDB Atlas Search for more advanced vector search features.
        # For simplicity, we use 'embedding' as an array and create a simple index here.

        self.collection.create_index([("embedding", "2dsphere")])  # Create geospatial index (a workaround for vector search)
        print("Created geospatial index on embeddings.")


    # Example: Fetch all records from the collection (for testing)
    def fetch_all_records(self):
        print('Exec: GTTMongoDB.fetch_all_records()')

        for record in self.collection.find():
            print(json.dumps(record, indent=2))

    # Function to fetch all embeddings and compute similarity
    def find_similar_embeddings(self, query_embedding, top_k=5):
        # Fetch all records
        records = self.collection.find()
        
        embeddings = []
        ids = []
        
        for record in records:
            embeddings.append(record['embedding'])
            ids.append(record['_id'])  # Store the record ID for later reference
        
        embeddings = np.array(embeddings)
        
        # Compute cosine similarity
        similarities = cosine_similarity([query_embedding], embeddings)[0]
        
        # Sort similarities in descending order and fetch top_k results
        top_k_indices = similarities.argsort()[-top_k:][::-1]
        
        for idx in top_k_indices:
            print(f"ID: {ids[idx]}, Similarity: {similarities[idx]:.4f}")
            print(f"Content: {records[idx]['content'][:50]}...")  # Print the first 50 chars of content