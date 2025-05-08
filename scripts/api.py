# scripts/api.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
import faiss
import pickle
import openai
import numpy as np
import os
import json
import re


openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

faiss_index = faiss.read_index("data/index.faiss")
with open("data/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)
    
class QuestionRequest(BaseModel):
    question: str
    
# parse GPT JSON, removing code blocks or formatting
def try_parse_structured_json(raw: str):
    if "```json" in raw:
        match = re.search(r"```json(.*?)```", raw, re.DOTALL)
        if match:
            raw = match.group(1).strip()

    # try to parse the outer JSON
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return None

    # if the outer layer is the context_paragraph, check whether context include JSON characters
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
    
    D, I = faiss_index.search(query_vector, k = 5)
    relevant_chunks = [metadata[i] for i in I[0]]
    
    context = "\n---\n".join([f"(Page {chunk['page']}): {chunk['content']}" for chunk in relevant_chunks])
    #prompt = f"Answer the question using the context below:\n\nContext:\n{context}\n\nQuestion: {request.question}\nAnswer:"
    full_prompt = f"{layout_instruction}\n\nHere is the context:\n{context}\n\nQuestion: {request.question}"

    # Use GPT-4o
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.2
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
