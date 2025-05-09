# The Great Gatsby Q&A System

## Main Idea

*  **"Long-Term Memory Room Metaphor"**
	* Previously asked question and GPT responses are cached in `longterm_memory.json` (including the pertaining)
	* The main backend logic is in `/scripts/api.py`.
	* Matching is determined via vector similarity, keyword overlap, and fallback LLM equivalence.
	* Each user input is a pretraining -- the conversation will first look for a match to `longterm_memory.json`, and if there is no match or the similarity value is too low, it will be answered using the `GPT-4o` model, and the answer will be added to the `longterm_memory.json` file
	* While it's not perfectly to answer within five seconds for every question (because there are times when answers not in `longterm_memory.json` will use the 4o model), the average response time can be controlled within five seconds, and the front-end rendering won't take more than a second. With more users ask more questions, the response time (especially for those hot question) can be very fast with the growth of the long-term memory room.
	* Using the LRU mechanism, if the `longterm_memory.json`'s answers are set to a specified amount (currently 500 entries, which can be reduced or increased), the least recently used answer will be deleted.

*  **Structured JSON Output**
	*  GPT outputs are returned as one of: `character_cards`, `symbol_list`, `timeline`, `quote_analysis`, `summary`, `theme`, or `context_paragraph`.
	*  The UI format will paired the different structures.

## How it works?

- **PDF Preprocessing & Chunking**
    - Book text is pre-split into chunks.
    - Each chunk is embedded using `text-embedding-3-small`.
    - Chunk metadata is stored in `metadata.pkl` with vectors saved in `embeddings.npy`.

- **Fast Similarity Search**
    - Uses FAISS (`IndexFlatL2`) to retrieve top-K chunks given a new query embedding.
    - Matched chunk text is passed to GPT-4o with a layout instruction.		

- **Memory Matching & Deduplication**
    - All user queries are embedded.
    - Long-term memory search uses:
        - Cosine similarity
        - Keyword overlap
        - GPT-4o fallback equivalence check (controlled by `llm_is_equivalent()`)
    - Reuses existing answers when a match is detected.

- **GPT Layout Generation**
    - A layout-specific prompt instructs GPT-4o to return valid structured JSON.
    - If parsing fails, falls back to simple paragraph string.

- **LLM Models Used**
    - `gpt-4o` for question normalization, layout generation, and equivalence detection.
    - `text-embedding-3-small` for semantic vector search.

## How to Run
### Backend:
```
export OPENAI_API_KEY="your-api-key"
# or on Windows:
# $env:OPENAI_API_KEY="your-api-key"
uvicorn scripts.api:app --reload
```

### Frontend:
```
cd frontend
npm install
npm run dev
```
Then open [http://localhost:5173](http://localhost:5173).


