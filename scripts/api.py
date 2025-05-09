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

MAX_MEMORY = 500

openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("data/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

embedding_matrix = np.load("data/embeddings.npy")
faiss_index = faiss.IndexFlatL2(embedding_matrix.shape[1])
faiss_index.add(embedding_matrix)

longterm_path = "data/longterm_memory.json"
if os.path.exists(longterm_path):
    with open(longterm_path, "r", encoding="utf-8") as f:
        longterm_memory = json.load(f)
else:
    longterm_memory = []

class QuestionRequest(BaseModel):
    question: str

def normalize_question(question: str) -> str:
    try:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You rewrite user input into a complete, formal, standalone question."},
                {"role": "user", "content": question}
            ],
            temperature=0.0
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"[Rewrite Error] {e}")
        return question

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a_norm = a / np.linalg.norm(a)
    b_norm = b / np.linalg.norm(b)
    return np.dot(a_norm, b_norm)

def extract_keywords(text: str) -> set:
    stop_words = {"the", "a", "an", "is", "in", "on", "give", "tell", "provide", "at", "of", "to", "and", "about", "for", "with"}
    words = set(re.findall(r"\w+", text.lower()))
    return words - stop_words

def keyword_overlap(a: str, b: str) -> float:
    a_keywords = extract_keywords(a)
    b_keywords = extract_keywords(b)
    if not a_keywords or not b_keywords:
        return 0.0
    return len(a_keywords & b_keywords) / len(a_keywords | b_keywords)

def llm_is_equivalent(q1: str, q2: str) -> bool:
    print(f"[LLM Check TRIGGERED] Comparing:\n  Q1: {q1}\n  Q2: {q2}")
    prompt = f"""
You are deciding whether two user questions can be answered using the exact same content in a Q&A system about the same book.

If the two questions refer to the same domain (e.g. same novel, topic, or scope) and are requesting substantially the same information—even if phrased differently—they should be considered equivalent.

Q1: {q1}
Q2: {q2}

Are they equivalent? Answer only "yes" or "no".
"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        answer = response.choices[0].message.content.strip().lower()
        print(f"[LLM Check Result] → {answer}")
        return "yes" in answer
    except Exception as e:
        print(f"[Equivalence check error] {e}")
        return False

def is_same_question(q1: str, q2: str, vec_sim: float) -> bool:
    SIM_THRESHOLD = 0.95
    LOOSE_SIM_THRESHOLD = 0.55
    OVERLAP_THRESHOLD = 0.55

    overlap = keyword_overlap(q1, q2)
    print(f"[Matching Debug] Cosine Similarity: {vec_sim:.4f}, Keyword Overlap: {overlap:.4f}")

    if vec_sim > SIM_THRESHOLD and overlap > OVERLAP_THRESHOLD:
        print("[Decision] Matched by strict embedding + keyword")
        return True
    if vec_sim > LOOSE_SIM_THRESHOLD:
        print("[Decision] Matched by LLM equivalence fallback")
        return llm_is_equivalent(q1, q2)
    print("[Decision] No match")
    return False

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

    normalized_q = normalize_question(request.question)

    embedding_response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=normalized_q
    )
    query_vector = np.array(embedding_response.data[0].embedding, dtype="float32")

    # Step 1: score all long-term question records
    scored_matches = []
    for entry in longterm_memory:
        memory_vector = np.array(entry["embedding"], dtype="float32")
        score = cosine_similarity(query_vector, memory_vector)
        print(f"[Similarity] Q: \"{request.question}\" vs \"{entry['question']}\" → Score: {score:.4f}")
        scored_matches.append((score, entry))

    # Step 2: keep CANDIDATE_LIMIT record
    CANDIDATE_LIMIT = 4
    MIN_SIMILARITY = 0.4
    scored_matches = [(s, e) for s, e in sorted(scored_matches, key=lambda x: x[0], reverse=True) if s > MIN_SIMILARITY][:CANDIDATE_LIMIT]

    # Step 3: check whether the questions are same
    for score, entry in scored_matches:
        if is_same_question(
            normalized_q,
            entry.get("normalized_question", entry["question"]),
            score
        ):
            print(f"[Final Match] Reuse Answer from: \"{entry['question']}\"")

            # update information
            entry["count"] += 1
            entry["last_used"] = time.time()

            # alias
            if request.question != entry["question"]:
                longterm_memory.append({
                    "question": request.question,
                    "normalized_question": normalized_q,
                    "embedding": query_vector.tolist(),
                    "data": entry["data"],
                    "count": 1,
                    "last_used": time.time()
                })

            # LRU
            if len(longterm_memory) > MAX_MEMORY:
                longterm_memory.sort(key=lambda x: x.get("last_used", 0))
                longterm_memory = longterm_memory[-MAX_MEMORY:]

            with open(longterm_path, "w", encoding="utf-8") as f:
                json.dump(longterm_memory, f, indent=2, ensure_ascii=False)

            return entry["data"]

    # Step 4: not hit --> go 4o
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

    longterm_memory.append({
        "question": request.question,
        "normalized_question": normalized_q,
        "embedding": query_vector.tolist(),
        "data": structured_data,
        "count": 1,
        "last_used": time.time()
    })

    if len(longterm_memory) > MAX_MEMORY:
        longterm_memory.sort(key=lambda x: x.get("last_used", 0))
        longterm_memory = longterm_memory[-MAX_MEMORY:]

    with open(longterm_path, "w", encoding="utf-8") as f:
        json.dump(longterm_memory, f, indent=2, ensure_ascii=False)

    return structured_data