from langchain_anthropic import ChatAnthropic
from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

embeddings = FastEmbedEmbeddings() # initialize the HuggingFaceEmbeddings class with the specified model, which we will use to generate embeddings for our text chunks
collection = Chroma(persist_directory="chroma_db", collection_name="um_assistant", embedding_function=embeddings)
llm = ChatAnthropic(model="claude-sonnet-4-20250514")

template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant for University of Michigan Dearborn students, providing concise and accurate answers to their questions based on the provided context. If the answer is not in the context, say you don't know."),
        ("human", "Context:\n{context}\n\n{query}")])

chain = template | llm | StrOutputParser()


def generate_response(query): # function to generate a response to the user's query
    results = collection.similarity_search(query, k=3) # query the ChromaDB collection for relevant documents based on the user's query, retrieving the top 3 most similar documents
    context = " ".join([result.page_content for result in results]) # combine the retrieved documents into a single context string
    response = chain.invoke({"context": context, "query": query}) # pass the context

    return response # return the generated response text


