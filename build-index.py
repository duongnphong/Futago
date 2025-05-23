import pickle
import re
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


def chunk_markdown_with_metadata(folder_path="logs/"):
    data = []
    files = sorted(Path(folder_path).glob("*.md")) + sorted(
        Path(folder_path).glob("*.txt")
    )

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Extract date from filename (e.g., 2025-05-20.md → 2025-05-20)
        date_match = re.search(r"\d{4}-\d{2}-\d{2}", file_path.name)
        file_date = date_match.group() if date_match else "unknown"

        # Chunk by level-2 headers (## Section Title)
        sections = re.split(r"(## .+)", text)
        chunks = []
        current_section = "General"

        for i in range(len(sections)):
            if sections[i].startswith("# "):
                continue
            elif sections[i].startswith("## "):
                current_section = sections[i][3:].strip()  # Remove '## '
            elif sections[i].strip():
                chunk = {
                    "content": sections[i].strip(),
                    "metadata": {
                        "source": file_path.name,
                        "date": file_date,
                        "section": current_section,
                    },
                }
                chunks.append(chunk)

        data.extend(chunks)

    return data


def embed_chunks_local(chunks, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embedded_data = []

    for chunk in tqdm(chunks):
        combined_text = f"Log entry dated {chunk['metadata']['date']}: [{chunk['metadata']['section']}] {chunk['content']}"
        print(combined_text[:200])
        embedding = model.encode(combined_text, convert_to_numpy=True).tolist()
        # embedding = model.encode(chunk["content"], convert_to_numpy=True).tolist()
        embedded_data.append(
            {
                "embedding": embedding,
                "metadata": chunk["metadata"],
                "content": chunk["content"],
            }
        )

    return embedded_data


def build_faiss_index(embedded_chunks):
    dim = len(embedded_chunks[0]["embedding"])  # should be 384
    index = faiss.IndexFlatL2(dim)

    vectors = np.array([c["embedding"] for c in embedded_chunks]).astype("float32")
    index.add(vectors)

    # Save metadata in same order as FAISS vectors
    metadata = [
        {"metadata": c["metadata"], "content": c["content"]} for c in embedded_chunks
    ]

    return index, metadata


chunks = chunk_markdown_with_metadata("logs/")
embedded_chunks = embed_chunks_local(chunks)
# print(embedded_chunks)
index, metadata = build_faiss_index(embedded_chunks)
faiss.write_index(index, "./vectorization/log_index.faiss")
with open("./vectorization/log_metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)
