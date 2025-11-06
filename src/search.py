import numpy as np
import pandas as pd
from pathlib import Path
from src.embed import get_embeddings

class ScriptureSearchEngine:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)

        # Load Book of Mormon data
        self.bom_embeddings = np.load(self.data_dir / "bom_embeddings.npz", allow_pickle=True)["embeddings"]
        self.bom_metadata = pd.read_csv(self.data_dir / "bom_metadata.csv")

        # Load King James Bible data
        self.kjb_embeddings = np.load(self.data_dir / "kjb_embeddings.npz", allow_pickle=True)["embeddings"]
        self.kjb_metadata = pd.read_csv(self.data_dir / "kjb_metadata.csv")

        # Normalize embeddings once for faster cosine similarity (dot product of normalized vectors)
        self.bom_embeddings = self.bom_embeddings / np.linalg.norm(self.bom_embeddings, axis=1, keepdims=True)
        self.kjb_embeddings = self.kjb_embeddings / np.linalg.norm(self.kjb_embeddings, axis=1, keepdims=True)

        print(f"Loaded {len(self.bom_metadata)} Book of Mormon verses")
        print(f"Loaded {len(self.kjb_metadata)} King James Bible verses")

    def search(self, query: str, top_k_per_source: int = 30):
        """
        Search for verses similar to the query.
        Always searches both KJB and BOM, returning top_k_per_source from each.

        Args:
            query: Search query text
            top_k_per_source: Number of results to return from each source

        Returns:
            Dictionary with 'kjb' and 'bom' keys containing lists of results
        """
        # Get query embedding and normalize it
        query_embedding = get_embeddings([query])[0]
        query_embedding = query_embedding / np.linalg.norm(query_embedding)

        # Get results from both sources
        bom_results = self._search_corpus(
            query_embedding,
            self.bom_embeddings,
            self.bom_metadata,
            "Book of Mormon",
            top_k_per_source
        )

        kjb_results = self._search_corpus(
            query_embedding,
            self.kjb_embeddings,
            self.kjb_metadata,
            "King James Bible",
            top_k_per_source
        )

        return {
            "kjb": kjb_results,
            "bom": bom_results
        }

    def _search_corpus(self, query_embedding, embeddings, metadata, source_name, top_k):
        """Search within a specific corpus using optimized matrix multiplication."""
        # Calculate similarities using dot product (both vectors are normalized)
        # This is equivalent to cosine similarity but much faster
        similarities = np.dot(embeddings, query_embedding)

        # Get top k indices using argpartition (O(n) vs O(n log n) for full sort)
        # argpartition puts the top-k largest elements at the end, but not sorted
        if top_k < len(similarities):
            top_indices = np.argpartition(similarities, -top_k)[-top_k:]
            # Sort just the top-k indices by similarity (descending)
            top_indices = top_indices[np.argsort(similarities[top_indices])[::-1]]
        else:
            # If top_k >= length, just sort everything
            top_indices = np.argsort(similarities)[::-1]

        # Build results
        results = []
        for idx in top_indices:
            verse_data = metadata.iloc[idx]

            # Build reference string
            if source_name == "Book of Mormon":
                reference = f"{verse_data['book']} {verse_data['chapter']}:{verse_data['verse']}"
            else:
                reference = f"{verse_data['book']} {verse_data['chapter']}:{verse_data['verse']}"

            results.append({
                "reference": reference,
                "text": verse_data["original_text"],
                "embedding_text": verse_data["embedding_text"],
                "similarity": float(similarities[idx]),
                "source": source_name,
                "book": verse_data["book"],
                "chapter": int(verse_data["chapter"]),
                "verse": int(verse_data["verse"]),
                "verse_idx": int(idx)
            })

        return results
