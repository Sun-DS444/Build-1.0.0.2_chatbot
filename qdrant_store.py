from qdrant_client import QdrantClient
import streamlit as st

def get_client():
    return QdrantClient(
        url=st.secrets["QDRANT_URL"],
        api_key=st.secrets["QDRANT_API_KEY"]
    )
