# Chunker 

import os
from langchain_chroma import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

embeddings = FastEmbedEmbeddings()

def load_documents(): # function to read in all the text documents from the data/ directory, which we will later chunk and embed for our knowledge base
    documents = [] # start empty list to hold all the text documents we will read in

    for filename in os.listdir('data/'): # loop through each filename in the data/ directory
        with open(f"data/{filename}", 'r') as file: # open the file for reading, using a context manager (with) to ensure it gets closed properly
            text = file.read() # read the entire contents of the file into a string variable called text
            documents.append(text) # add the text string to our documents list, so we end up with a list of all the text from all the files in data/ directory
    
    return documents


def chunk_text(text, chunk_size=500, overlap=50):# function to split a long text into smaller chunks, with some overlap between them
    chunks = [] # start with an empty list to hold the chunks
    start = 0 # initialize a variable to keep track of where we are in the text
    while start < len(text):# loop until we've processed the entire text
        end = min(start + chunk_size, len(text)) # calculate the end index for the current chunk, ensuring we don't go past the end of the text
        chunk = text[start:end] # extract the chunk of text from the start index to the end index
        chunks.append(chunk) # add the chunk to our list of chunks
        start += chunk_size - overlap  # move forward by chunk_size minus the overlap
    return chunks


def ingest_to_chromadb(documents): 
    chunks_list = [] # start with an empty list to hold all the chunks from all the documents
    for doc in documents:
        chunks = chunk_text(doc) # call our chunk_text function to split the document into smaller chunks, which will help us create more manageable pieces of text for embedding and retrieval in our knowledge base
        for chunk in chunks:
            chunks_list.append(chunk) # add each chunk to the chunks_list, so we end up with a single list of all the chunks from all the documents

    Chroma.from_texts(chunks_list, embedding=embeddings, collection_name="um_assistant", persist_directory="chroma_db") # create a new ChromaDB collection called "um_assistant" and populate it with the chunks from our documents, using the HuggingFaceEmbeddings to generate embeddings for each chunk


docs = load_documents()
ingest_to_chromadb(docs)
print("Done")