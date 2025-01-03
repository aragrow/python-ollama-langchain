import os
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from langchain.prompts import ChatPromptTemplate
from langchain_ollama.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
from dotenv import load_dotenv  # Import dotenv to load environment variables

from includes.gtt_secured import GTTSecured  # Importing the GTTSecured class
from includes.gtt_loadpdf import GTTLoadPDFs  # Importing the GTTSecured class
from includes.gtt_chunck import GTTChunking  # Importing the GTTSecured class
from includes.gtt_embedding import GTTEmbedding  # Importing the GTTSecured class
from includes.gtt_mongodb import GTTMongoDB  # Importing the GTTMongoDB class
from includes.gtt_chat_ollama import GTTChatOllama  # Importing the GTTChatOllama class

# Load environment variables from the .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Flask-JWT setup: Read the secret key from the environment variable
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Get the secret key from .env file
# Access the JWT_SECRET_KEY
jwt = JWTManager(app)

# Initialize variables
data_array = []
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

@app.route('/login', methods=['GET'])
def show_login():
    print('show_login()')
    return jsonify({"message": "Done"})

@app.route('/create-token', methods=['POST'])
def create_token():
    print('create_token()')
    """
    This route generates a JWT token when provided with correct credentials (in this case, a static username and password).
    In a real-world app, you'd authenticate against a database or other secure method.
    """
    theusername = request.json.get("username", None)

    if theusername != os.getenv('GTT_USERNAME'): return jsonify({"error": "Invalid credentials 1"}), 401

    thepassword = request.json.get("password", None) # The password to encrypt

    thesalthex = os.getenv('GTT_SALT_HEX_2_DERIVE_KEY');
    thesalt = bytes.fromhex(thesalthex)
    
    """
    # Initialize object with the password
        password_encryption = GTTSecured(password=thepassword,stored_salt=thesalt)
        print(f"password_encryption: {password_encryption}")
    
    # Encrypt the password
        encrypted_password = password_encryption.encrypt(thepassword)
        print(f"encrypted_password: {encrypted_password}")

    # Create JWT token
  
    """

    encrypted_password = os.getenv('GTT_PASSWORD')
    # Now, validate the password with the stored encrypted password and salt
    password_validator = GTTSecured(password=thepassword,stored_salt=thesalt)  # Use the stored salt
    
    is_valid = password_validator.validate_password(encrypted_password, thepassword)
    print("Is the password valid?", is_valid)

    if is_valid != 1 :  return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=theusername)
    return jsonify(access_token=access_token)  



@app.route('/refresh-data', methods=['POST'])
#@jwt_required()  # Protect the route with JWT
def refresh_data():
    try:
        # Load PDFs (once per session or on first request)
    
        data_array = GTTLoadPDFs.load_pdfs()

        chunks = GTTChunking.chunk_text(data_array)

        # Print out some of the chunks for visualization
        #for chunk in chunks[:5]:  # Show first 5 chunks
        #    print(chunk.page_content)

        #print(chunks)

        # Create an Embedder instance
        embedder = GTTEmbedding()
        embeddings = embedder.create_embeddings(chunks)

        mongodb = GTTMongoDB()
        mongodb.ensure_database_and_collection_exists()
        mongodb.create_vector_indexes()
        mongodb.insert_bulk_inserts(embeddings)
    
        # If successful, return status 200 with a success message
        return jsonify({"message": "Data refreshed successfully."}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return 
@app.route('/answer-question', methods=['POST'])
#@jwt_required()  # Protect the route with JWT
def answer_question():
    # Get the 'question' parameter from the query string
    question = request.args.get('question').strip()
    query = question.encode('ascii', 'ignore').decode()

    if not question:
        return jsonify({"error": "No question parameter provided"}), 400

    try:
        print(query)

        embed = GTTEmbedding()
        query_embedding = embed.create_embed(query)

        mongodb = GTTMongoDB()
        context = mongodb.retrieve_similar_embeddings(query_embedding, 5)

        # Return the answer as a JSON array
        no0fcandidates = 3
        conversation_history = []
        print(f'Context for question: {type(context)}')
        print(f'Query for question: {type(query)}')
        print('----------------------------------------------------------')
              
        answer = GTTChatOllama.chat_with_ollama(context, query, conversation_history, no0fcandidates)

        return jsonify({"question": query, "answer": [answer]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == "__main__":
    # Start the Flask app
    app.run(debug=True,port=5100)
