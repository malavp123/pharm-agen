
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class RetrieverAgent:
    def __init__(self, chunks, embedder_agent, top_k=5):
        self.chunks = chunks
        self.embedder = embedder_agent
        self.top_k = top_k
        self.index, self.chunk_map = self._build_index()

    def _build_index(self):
        embeddings = self.embedder.model.encode(self.chunks, convert_to_numpy=True)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        return index, {i: chunk for i, chunk in enumerate(self.chunks)}

    def run(self, state):
        query_vec = state["query_embedding"]
        D, I = self.index.search(np.array([query_vec]), self.top_k)
        retrieved = [self.chunk_map[idx] for idx in I[0]]
        return {**state, "retrieved_chunks": retrieved}
