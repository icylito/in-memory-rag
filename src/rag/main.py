#libraries
import requests
import numpy as np 
from pathlib import Path

#ollama models and endpoint

ollama= "http://localhost:11434"
embed_model= "nomic-embed-text:v1.5"
chat_model= "gemma4:31b-cloud"

#turning text into embeddings with endpoints

def embed(text):
    r = requests.post(f"{ollama}/api/embed", json={"model": embed_model, "input": text})
    return np.array(r.json()["embeddings"])

#asking the model with endpoints

def ask_llm(prompt):
    r = requests.post(f"{ollama}/api/chat", json={
        "model": chat_model, "stream": False, 
        "messages": [{"role": "user", 
                     "content": prompt}],
    } )
    return r.json()["message"]["content"]

#chunking

chunks = []
for file in Path("docs").glob("*.md"):
    chunks += [p.strip() for p in file.read_text(encoding="utf-8").split("\n\n") if p.strip()]

#vectorizing the chunks

chunk_vectors = embed(chunks)
#print(f"Indexed {len(chunks)} chunks\n")
#print(f"Vector array shape: {chunk_vectors.shape}")

#retrieval to use the context that just got chunked then vectorizied (basically the whole goal of a rag pipeline)

def retrieve(question, k=3):
    q = embed(question)[0]
    scores = chunk_vectors @ q / (np.linalg.norm(chunk_vectors, axis=1) * np.linalg.norm(q)) 
    return [chunks[i] for i in np.argsort(scores)[::-1][:k]]

# Chat cli interface

while True:
    question = input("Ask: ")
    context = "\n\n".join(retrieve(question))
    #print(context) #only enable it if you're curious to what the model is referencing 
    prompt = f"""Answer the question using ONLY the context below. 
    If the answer isn't in the context, simply say "I don't know".  

    Context:
    {context}

    Question: {question}"""
    print("\n" + ask_llm(prompt) + "\n")
