import os
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from langchain_ollama import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_ollama.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
from dotenv import load_dotenv  # Import dotenv to load environment variables

from includes.gtt_secured import GTTSecured  # Importing the GTTSecured class
from includes.gtt_loadpdf import GTTLoadPDFs  # Importing the GTTSecured class

# Load environment variables from the .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Flask-JWT setup: Read the secret key from the environment variable
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Get the secret key from .env file
jwt = JWTManager(app)

# Initialize variables
data_array = []
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Function to interact with the loaded PDFs and generate answers
def chat_with_pdf(question):
    # Now split the text into chunks using the RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(data_array)

    # Create vector database
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=OllamaEmbeddings(model="nomic-embed-text"),
        collection_name="local-rag"
    )
    print("Vector database created successfully")

    # Set up LLM and retrieval
    local_model = "llama3.2"  # or whichever model you prefer
    llm = ChatOllama(model=local_model)

    # Query prompt template
    QUERY_PROMPT = ChatPromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate 2
        different versions of the given user question to retrieve relevant documents from
        a vector database. By generating multiple perspectives on the user question, your
        goal is to help the user overcome some of the limitations of the distance-based
        similarity search. Provide these alternative questions separated by newlines.
        Original question: {question}""",
    )

    # Set up retriever
    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(), 
        llm,
        prompt=QUERY_PROMPT
    )

    # RAG prompt template
    template = """Answer the question based ONLY on the following context:
    {context}
    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    # Create chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Call the chain to get the answer
    answer = chain.invoke(question)
    return answer

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
@jwt_required()  # Protect the route with JWT
def refresh_data():
    try:
        # Load PDFs (once per session or on first request)
        GTTLoadPDFs.load_pdfs()
    
        # If successful, return status 200 with a success message
        return jsonify({"message": "Data refreshed successfully."}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return 
@app.route('/answer-question', methods=['POST'])
@jwt_required()  # Protect the route with JWT
def answer_question():
    # Get the 'question' parameter from the query string
    question = request.args.get('question')

    if not question:
        return jsonify({"error": "No question parameter provided"}), 400

    try:
        # Load PDFs (once per session or on first request)
        GTTLoadPDFs.load_pdfs()

        # Get the answer from the PDF-based model
        answer = chat_with_pdf(question)

        # Return the answer as a JSON array
        return jsonify({"answer": [answer]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Start the Flask app
    app.run(debug=True,port=5100)
