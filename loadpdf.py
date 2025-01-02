
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.chat_models import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
from IPython.display import display, Markdown
import os
import pdfplumber

# Initialize the data array
data_array = []

# Set the protocol buffers environment variable (if needed)
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Directory containing the PDF files
directory_path = "data/"

# Check if the directory exists
if not os.path.exists(directory_path):
    print(f"Directory {directory_path} does not exist.")
else:
    # Loop through all directories in the 'data' directory
    for dirname in os.listdir(directory_path):
        print(f"-> Data directory: {dirname}")

        # Full path for the subdirectory
        full_path = os.path.join(directory_path, dirname)
        print(f"--> Data subdirectory: {full_path}")

        # Check if it's a directory
        if not os.path.isdir(full_path):
            continue

        # Loop through all files in the subdirectory
        for filename in os.listdir(full_path):
            if filename.endswith(".pdf"):
                # Construct the full file path for the PDF
                local_path = os.path.join(full_path, filename)
                print(f"---> Found PDF file: {local_path}")

                try:
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
                        print(f"PDF loaded successfully: {local_path}")
                    else:
                        print(f"Warning: No data extracted from PDF {local_path}")
                except Exception as e:
                    # Print any errors that occur during PDF loading
                    print(f"Error loading PDF {local_path}: {str(e)}")
            else:
                print(f"Skipping non-PDF file: {filename}")

    # Print the total number of documents loaded (not just PDFs)
    print(f"Total documents loaded: {len(data_array)}")

# Now split the text into chunks using the RecursiveCharacterTextSplitter

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Split the documents into chunks
chunks = text_splitter.split_documents(data_array)

# Print how many chunks were created
print(f"Text split into {len(chunks)} chunks")

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
QUERY_PROMPT = PromptTemplate(
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

def chat_with_pdf(question):
    """
    Chat with the PDF using the RAG chain.
    """
    return display(Markdown(chain.invoke(question)))

    # Example 1
chat_with_pdf("What is the main idea of these documents?")

# Optional: Clean up when done 
vector_db.delete_collection()
print("Vector database deleted successfully")