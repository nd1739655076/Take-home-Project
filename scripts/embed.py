# scripts/embed.py
import openai
import numpy as np
import faiss
import pickle
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

with open("data/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

texts = [item["content"] for item in metadata]
embeddings = []
for i in range(0, len(texts), 10):
    batch = texts[i:i+10]
    res = openai.embeddings.create(
        model="text-embedding-3-small",
        input=batch
    )
    embeddings.extend([e.embedding for e in res.data])

np.save("data/embeddings.npy", np.array(embeddings, dtype=np.float32))