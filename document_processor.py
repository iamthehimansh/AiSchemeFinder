from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import os
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
import multiprocessing

CHROMA_PATH = "chroma"
DATA_PATH = "data"
PROGRESS_FILE = "processing_progress.json"

# Configure Ollama embeddings with MPS acceleration for M2 Mac
embd = OllamaEmbeddings(
    model="gemma:latest",
    model_kwargs={"device": "mps"},  # Use MPS for M2 Mac GPU acceleration
    # encode_kwargs={"batch_size": 16}  # Adjusted batch size for M2 Mac GPU
)

def main():
    t1 = time.time()
    generate_data_store()
    print(f"Processing time: {time.time() - t1:.2f} seconds")

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {'processed_files': []}

def save_progress(processed_files):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({'processed_files': processed_files}, f)

def generate_data_store():
    progress = load_progress()
    processed_files = set(progress['processed_files'])
    
    all_files = [os.path.join(DATA_PATH, f) for f in os.listdir(DATA_PATH) 
                 if os.path.isfile(os.path.join(DATA_PATH, f))]
    
    unprocessed_files = [f for f in all_files if f not in processed_files and f.endswith('.pdf')]
    if not unprocessed_files:
        print("No new files to process")
        return

    # Process files sequentially
    batch_size = 1  # Maintain batch size for consistent processing
    for i in range(0, len(unprocessed_files), batch_size):
        batch = unprocessed_files[i:i + batch_size]
        try:
            # Process each batch directly
            process_documents_batch(batch)
            
            # Update progress after each batch
            for file_path in batch:
                processed_files.add(file_path)
                print(f"Processing file: {file_path}")
            save_progress(list(processed_files))
            
            
        except Exception as e:
            print(f"Error processing batch: {e}")

def process_documents_batch(file_paths: List[str]):
    all_chunks = []
    for file_path in file_paths:
        loader = DirectoryLoader(os.path.dirname(file_path), 
                               glob=os.path.basename(file_path))
        documents = loader.load()
        chunks = split_text(documents)
        all_chunks.extend(chunks)
    
    if all_chunks:
        save_to_chroma(all_chunks)

def process_single_document(file_path):
    loader = DirectoryLoader(os.path.dirname(file_path), 
                           glob=os.path.basename(file_path))
    documents = loader.load()
    chunks = split_text(documents)
    return chunks

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks

def save_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=embd
    )
    
    db.add_documents(chunks)
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()