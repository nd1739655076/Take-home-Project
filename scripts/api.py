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

openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load vector database & metadata
embedding_matrix = np.load("data/embeddings.npy")
faiss_index = faiss.IndexFlatL2(embedding_matrix.shape[1])
faiss_index.add(embedding_matrix)

with open("data/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

class QuestionRequest(BaseModel):
    question: str

# parse structured JSON
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
    
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=request.question
    )
    query_vector = np.array([response.data[0].embedding], dtype="float32")

    # Search relevant chunks
    D, I = faiss_index.search(query_vector, k=5)
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

    return structured_data
