import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai
import faiss
import numpy as np
import pickle
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# parsing the pdf by pages
def extract_pdf_text_with_pages(pdf_path):
    texts_with_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                texts_with_pages.append({
                    "page": i + 1,
                    "text": text
                })
    return texts_with_pages

# cut the page into smaller chunks
def split_text_into_chunks(texts_with_pages):
    splitter = RecursiveCharacterTextSplitter(chunk_size = 800, chunk_overlap=200)
    all_chunks = []
    for entry in texts_with_pages:
        chunks = splitter.split_text(entry["text"])
        for chunk in chunks:
            all_chunks.append({
                "page": entry["page"],
                "content": chunk
            })
    return all_chunks

# embedding vector -- LLM model: openAI
def embed_chunks(chunks):
    results = []
    for i, chunk in enumerate(chunks):
        print(f"Embedding chunk {i+1}/{len(chunks)}...")
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=chunk["content"]
        )
        embedding = response.data[0].embedding
        results.append({
            "embedding": embedding,
            "page": chunk["page"],
            "content": chunk["content"]
        })
    return results

# build vector database
def build_faiss_index(embedded_chunks, output_dir="data"):
    vectors = [entry["embedding"] for entry in embedded_chunks]
    dim = len(vectors[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(vectors).astype("float32"))
    faiss.write_index(index, os.path.join(output_dir, "index.faiss"))
    with open(os.path.join(output_dir, "metadata.pkl"), "wb") as f:
        pickle.dump(embedded_chunks, f)
    print(f"Index built with {len(vectors)} chunks.")
    


if __name__ == "__main__":
    input_pdf = "data/the-great-gatsby.pdf"
    texts = extract_pdf_text_with_pages(input_pdf)
    chunks = split_text_into_chunks(texts)
    embedded_chunks = embed_chunks(chunks)
    build_faiss_index(embedded_chunks)