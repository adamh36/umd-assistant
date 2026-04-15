# Chunker 

import os
import chromadb  # the vector database where we store embeddings


def load_documents():
    documents = [] # start empty list to hold all the text documents we will read in
    os.listdir('data/') # returns list of all filenames in data/ ( we can loop through it now)

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
    client = chromadb.PersistentClient(path="chroma_db")   # create a new ChromaDB client
    collection = client.create_collection("um_assistant")  # get or create a collection named "um_assistant"
    chunk_id = 0

    for doc in documents:
        chunks = chunk_text(doc)  # split the document into chunks
        for chunk in chunks: # loop through each chunk and add it to the ChromaDB collection
            collection.add(

                documents=[chunk],  # add the chunk as a document to the collection
                ids = [f"chunk_{chunk_id}"] # give each chunk a unique ID, like "chunk_0", "chunk_1", etc.

                )
            chunk_id += 1 # increment the chunk_id for the next chunk
            if chunk_id % 20 == 0:
                print(f"Ingested {chunk_id} chunks...")

    print(f"Done — {chunk_id} total chunks ingested")

docs = load_documents()
ingest_to_chromadb(docs)
print("Done")