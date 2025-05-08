from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import pickle
import openai
import numpy as np
import os
import json
import re
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import time

MAX_MEMORY = 500 #can be changed later to limit the longterm_memory.json's size

openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load metadata
with open("data/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

embedding_matrix = np.load("data/embeddings.npy")
faiss_index = faiss.IndexFlatL2(embedding_matrix.shape[1])
faiss_index.add(embedding_matrix)

# Load or initialize long-term memory
longterm_path = "data/longterm_memory.json"
if os.path.exists(longterm_path):
    with open(longterm_path, "r", encoding="utf-8") as f:
        longterm_memory = json.load(f)
else:
    longterm_memory = []

class QuestionRequest(BaseModel):
    question: str
    
    
# calculate the similarity score a: user input b: longterm_memory
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a_norm = a / np.linalg.norm(a)
    b_norm = b / np.linalg.norm(b)
    return np.dot(a_norm, b_norm)

def try_parse_structured_json(raw: str):
    if "```json" in raw:
        match = re.search(r"```json(.*?)```", raw, re.DOTALL)
        if match:
            raw = match.group(1).strip()
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if (
        isinstance(parsed, dict)
        and parsed.get("layout") == "context_paragraph"
        and isinstance(parsed.get("context"), str)
    ):
        try:
            inner = json.loads(parsed["context"])
            if isinstance(inner, dict) and "layout" in inner:
                return inner
        except json.JSONDecodeError:
            pass
    return parsed

layout_instruction = """
You are a JSON-only structured assistant for The Great Gatsby.

Based on the user's question and the context, identify the correct layout type:
- "timeline"
- "character_cards"
- "symbol_list"
- "quote_analysis"
- "summary"
- "context_paragraph" (default)

For each layout, respond with a strict JSON object matching this structure:

- character_cards: { "layout": "character_cards", "cards": [ { "name": ..., "description": ..., "relationship_to_protagonist": ..., "personality_traits": [...], "key_actions": [...], "quote": ..., "page": ..., "narrative_role": ... } ] }

- timeline: { "layout": "timeline", "title": "...", "events": [ { "year": "...", "month": "...", "day": "...", "event": "...", "page": ... } ] }

- symbol_list: { "layout": "symbol_list", "symbols": [ { "name": "...", "description": "...", "meaning": "...", "key_quote": "...", "page": ..., "references": [ { "description": "...", "page": ... } ] } ] }

- quote_analysis: { "layout": "quote_analysis", "quote": "...", "speaker": "...", "chapter": "...", "page": ..., "interpretation": "...", "themes": [...], "significance": "..." }

- summary: { "layout": "summary", "title": "...", "chapter": "...", "summary_points": [ ... ], "theme": "..." }

- context_paragraph: { "layout": "context_paragraph", "title": "Answer", "context": "..." }

Always return valid JSON. No explanation. No markdown.
"""

@app.post("/ask")
def ask_question(request: QuestionRequest):
    global longterm_memory

    # 1. embedding the current question
    embedding_response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=request.question
    )
    query_vector = np.array(embedding_response.data[0].embedding, dtype="float32")

    # 2. search longterm_memory.json first
    best_match = None
    best_score = 0
    for entry in longterm_memory:
        memory_vector = np.array(entry["embedding"], dtype="float32")
        score = cosine_similarity(query_vector, memory_vector)
        if score > best_score:
            best_score = score
            best_match = entry

    if best_match and best_score > 0.93:
        # hit
        best_match["count"] += 1
        best_match["last_used"] = time.time()
        with open(longterm_path, "w", encoding="utf-8") as f:
            json.dump(longterm_memory, f, indent=2, ensure_ascii=False)
        return best_match["data"]

    # 3. not hit --> model: gpt 4o
    D, I = faiss_index.search(query_vector.reshape(1, -1), k=5)
    relevant_chunks = [metadata[i] for i in I[0]]

    context = "\n---\n".join(
        [f"(Page {chunk['page']}): {chunk['content']}" for chunk in relevant_chunks]
    )
    full_prompt = f"{layout_instruction}\n\nHere is the context:\n{context}\n\nQuestion: {request.question}"

    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.2,
    )
    raw_output = completion.choices[0].message.content.strip()
    structured_data = try_parse_structured_json(raw_output)
    if structured_data is None:
        structured_data = {
            "layout": "context_paragraph",
            "title": "Answer",
            "context": raw_output
        }

    structured_data["sources"] = [
        {"page": chunk["page"], "content": chunk["content"][:300]}
        for chunk in relevant_chunks
    ]

    # 4. add the new long-term memory entry
    new_entry = {
        "question": request.question,
        "embedding": query_vector.tolist(),
        "data": structured_data,
        "count": 1,
        "last_used": time.time()
    }
    longterm_memory.append(new_entry)

    # 5. Use LRU to clean up the memory
    if len(longterm_memory) > MAX_MEMORY:
        longterm_memory.sort(key=lambda x: x.get("last_used", 0))
        longterm_memory = longterm_memory[-MAX_MEMORY:]

    with open(longterm_path, "w", encoding="utf-8") as f:
        json.dump(longterm_memory, f, indent=2, ensure_ascii=False)

    return structured_data