from langchain_anthropic import ChatAnthropic
from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()

import os
import streamlit as st

# Load from Streamlit secrets if available, otherwise fall back to .env
if "ANTHROPIC_API_KEY" in st.secrets:
    os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]

embeddings = FastEmbedEmbeddings() # initialize the HuggingFaceEmbeddings class with the specified model, which we will use to generate embeddings for our text chunks
collection = Chroma(persist_directory="chroma_db", collection_name="um_assistant", embedding_function=embeddings)
llm = ChatAnthropic(model="claude-sonnet-4-6")

template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant for University of Michigan Dearborn students, "
    "providing concise and accurate answers to their questions based on the provided context. "
    "If the answer is not in the context, say you don't know."),
    MessagesPlaceholder(variable_name="chat_history"), # placeholder for the chat history, which will allow us to include the previous conversation in the prompt when generating a response, so the assistant can maintain context across multiple turns of the conversation
    ("human", "Context:\n{context}\n\n{query}")])

chain = template | llm | StrOutputParser()
store = {}

def generate_response(query): # function to generate a response to the user's query
    if "default" not in store: # if the chat history is not already stored in our store dictionary, we want to initialize it as an empty list, so we can start tracking the conversation history for the user
        store["default"] = ChatMessageHistory()
    history = store["default"]
    results = collection.similarity_search(query, k=3)
    context = " ".join([result.page_content for result in results]) 
    response = chain.invoke({"context": context, "query": query, "chat_history": history.messages}) 
    history.add_user_message(query) # add the user's query to the chat history
    history.add_ai_message(response) # add the assistant's response to the chat history, so

    return response 


