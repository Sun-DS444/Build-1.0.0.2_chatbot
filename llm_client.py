# llm_client.py
import requests
import streamlit as st


def call_llm(context: str, question: str) -> str:
    """
    Calls Hugging Face Inference API to generate an answer.
    Requires secrets:
    - HF_API_KEY
    - HF_MODEL
    """

    try:
        url = f"https://api-inference.huggingface.co/models/{st.secrets['HF_MODEL']}"

        headers = {
            "Authorization": f"Bearer {st.secrets['HF_API_KEY']}",
            "Content-Type": "application/json"
        }

        prompt = f"""
You are a helpful AI assistant.
Answer clearly and simply.

Rules:
- Use simple, clear words
- Short paragraphs
- Do NOT mention Jira, tickets, IDs, sections, or documents
- Use the context only as background
- If information is unclear, answer generally

Context:
{context}

Question:
{question}

Answer:
""".strip()

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 300,
                "temperature": 0.3,
                "return_full_text": False
            }
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        result = response.json()

        # HF API response handling
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"].strip()

        return "⚠️ Unable to generate response at the moment."

    except Exception as e:
        return (
            "⚠️ AI service temporarily unavailable.\n\n"
            "Please try again after some time."
        )
