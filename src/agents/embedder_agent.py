
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbedderAgent:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def run(self, state):
        query = state["query"]
        embedding = self.model.encode(query, convert_to_numpy=True)
        return {**state, "query_embedding": embedding}
