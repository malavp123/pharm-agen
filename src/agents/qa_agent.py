
import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class QAAgent:
    def __init__(self, model_name="gpt-4o-mini", openai_api_key=OPENAI_API_KEY):
        self.model_name = model_name
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set.")

        openai.api_key = self.api_key

    def build_prompt(self, query, context_chunks):
        context_str = "\n---\n".join(context_chunks)
        return (
            f"You must only answer based on the given context.\n"
            f"You are a helpful assistant for biomedical research questions.\n"
            f"Explain in simpler terms rather than more complex explainations.\n"
            f"Do not make up information. If the answer is unclear or incomplete, say 'The information is not available in the provided context.'\n"
            f"Given the following document excerpts, answer the user's question.\n\n"
            f"Limit your answer to under 150 words.\n\n"
            f"Context:\n{context_str}\n\n"
            f"Question: {query}\n\n"
            f"Answer:"
        )

    def generate(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response["choices"][0]["message"]["content"].strip()

    def run(self, state):
        query = state["query"]
        context = state.get("retrieved_chunks", [])
        if not context:
            return {**state, "answer": "No relevant context retrieved."}

        prompt = self.build_prompt(query, context)
        answer = self.generate(prompt)
        return {**state, "answer": answer}
