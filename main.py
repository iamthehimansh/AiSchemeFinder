

import ollama
import json

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from flask import Flask, request, jsonify 
CORRENT_MODEL="gemma"  
embd=OllamaEmbeddings(model="gemma")
CHROMA_PATH="chroma"

def get_contextText(query_text):
    
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embd)
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    refrence_text = []
    for doc, _score in results:
        refrence_text.append(doc.metadata)
    print(refrence_text)
    return (context_text,refrence_text)

def get_response(query_text):
    context_text,refrence_text = get_contextText(query_text)
    print("\n\n---\n\n")
    print(context_text)
    print("\n\n---\n\n")
    
    prompt = f"""
    You are a helpful assistant.
    Answer the question based on the context below.
    If the question cannot be answered using the information provided answer with "I don't know".
    Responce in bullet point format.
    in beautiful format.
    Use refrence text to make responce more accurate.
    Do not halusinate.
    
    Context: {context_text}
    Question: {query_text}
    """
    for response in ollama.generate(CORRENT_MODEL, prompt, stream=True):
        if 'response' in response:
            yield response['response']
    return response["response"]
    
if __name__ == "__main__":
    while True:
        query_text = input("Enter your query: ")
        if query_text == "exit":
            break
        print(get_response(query_text))
    