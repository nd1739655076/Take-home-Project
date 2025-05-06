# scripts/api.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
import faiss
import pickle
import openai
import numpy as np
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

faiss_index = faiss.read_index("data/index.faiss")
with open("data/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)
    
class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QuestionRequest):
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=request.question
    )
    query_vector = np.array([response.data[0].embedding], dtype="float32")
    
    D, I = faiss_index.search(query_vector, k = 5)
    relevant_chunks = [metadata[i] for i in I[0]]
    
    context = "\n---\n".join([f"(Page {chunk['page']}): {chunk['content']}" for chunk in relevant_chunks])
    prompt = f"Answer the question using the context below:\n\nContext:\n{context}\n\nQuestion: {request.question}\nAnswer:"
    
    # Use GPT-4o
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    answer = completion.choices[0].message.content
    
    return {
        "answer": answer,
        "sources": [{"page": chunk["page"], "content": chunk["content"][:300]} for chunk in relevant_chunks]
    }