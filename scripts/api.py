# scripts/api.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
import faiss
import pickle
import openai
import numpy as np
import os
import json

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
    #prompt = f"Answer the question using the context below:\n\nContext:\n{context}\n\nQuestion: {request.question}\nAnswer:"
    structured_prompt = f"""
You are a structured Q&A assistant for The Great Gatsby.
Given a question and some extracted context paragraphs from the book, please:
1. Determine the most appropriate layout for the answer from the following:
   - timeline
   - character_cards
   - symbol_list
   - quote_analysis
   - summary
   - context_paragraph (default if uncertain)
2. Then generate a valid JSON object with the selected layout type and relevant data fields.
Output only the final JSON. Do not include natural language explanations.
Here is the extracted context:
{context}
Question: {request.question}
"""
    # Use GPT-4o
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": structured_prompt}],
        temperature=0.2
    )
    raw_content = completion.choices[0].message.content.strip()
    try:
        structured_output = json.loads(raw_content)
    except json.JSONDecodeError:
        structured_output = {
            "layout": "context_paragraph",
            "title": "Answer",
            "context": raw_content
        }
    structured_output["sources"] = [
        {"page": chunk["page"], "content": chunk["content"][:300]}
        for chunk in relevant_chunks
    ]
    return structured_output