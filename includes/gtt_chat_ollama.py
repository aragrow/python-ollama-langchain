import json
from langchain_ollama.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

class GTTChatOllama:
    # Function to load PDFs and process them into documents
    @staticmethod
    def chat_with_ollama(context: list, query: str, conversation_history: list, top_k: int = 3) -> str:

        # System prompt to guide the model's behavior
        system_prompt = """
        You are ConcuAid, an AI assistant designed to help answer questions about patient data.
        You are only allowed to use the information provided in the context to generate your responses. If the answer is not available, simply state that you do not know. Do not search the internet or use external sources.
        Your responses should be written in clear, natural language, and complex terms should be explained in a way that is easy to understand for non-medical audiences.
        When displaying data, use a table format if it improves clarity. If the data is more suitable for paragraph form, present it in well-organized paragraphs.
        All responses must be formatted in HTML. Include only the content of the body in the response — no additional commentary.
        """

       # supports many more optional parameters. Hover on your `ChatOllama(...)`
        # class to view the latest available supported parameters
        llm = ChatOllama(model="llama3")
        prompt = ChatPromptTemplate.from_template("{system_prompt} {query} {topic}")

        # using LangChain Expressive Language chain syntax
        # learn more about the LCEL on
        # /docs/expression_language/why
        chain = prompt | llm | StrOutputParser()

        # for brevity, response is printed in terminal
        # You can use LangServe to deploy your application for
        # production
        return chain.invoke({"system_prompt": system_prompt, "query": query,"topic": context})
