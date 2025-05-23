import pickle
import re

import faiss
import numpy as np


def load_faiss_and_metadata(
    index_path="./vectorization/log_index.faiss",
    meta_path="./vectorization/log_metadata.pkl",
):
    index = faiss.read_index(index_path)
    with open(meta_path, "rb") as f:
        metadata = pickle.load(f)
    return index, metadata


# def search_index(query, model, index, metadata_store, k=5):
#     query_vec = model.encode(query, convert_to_numpy=True).astype("float32")
#     D, I = index.search(np.array([query_vec]), k)
#     results = []

#     for idx in I[0]:
#         result = metadata_store[idx]
#         results.append(result)


#     return results
def search_index(query, model, index, metadata_store, k=5):
    query_vec = model.encode(query, convert_to_numpy=True).astype("float32")
    D, I = index.search(np.array([query_vec]), k * 3)  # get more candidates

    # Check if the query contains a date (YYYY-MM-DD)
    date_match = re.search(r"\d{4}-\d{2}-\d{2}", query)
    target_date = date_match.group() if date_match else None

    filtered = []
    fallback = []

    for idx in I[0]:
        result = metadata_store[idx]
        if target_date and result["metadata"]["date"] == target_date:
            filtered.append(result)
        elif not target_date:
            filtered.append(result)
        else:
            fallback.append(result)

        # Stop early if we have enough
        if len(filtered) >= k:
            break

    # Fill in the rest if not enough exact date matches
    remaining = k - len(filtered)
    filtered.extend(fallback[:remaining])

    return filtered
