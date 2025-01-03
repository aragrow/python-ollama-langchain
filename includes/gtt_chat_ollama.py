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
        You are ConcuAid, an AI assistant that helps answer questions related to concussions. 
        You can only use the context provided to respond. 
        If you do not know the answer, just say so. Do not use the internet to help with your response. 
        Please provide text in natural human language, and explain complicated terms because your audience are not medical professionals.
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
