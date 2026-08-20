from pathlib import Path

import faiss
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
INDEX_FILE = DATA_DIR / "employee_kt.index"
CHUNKS_FILE = DATA_DIR / "chunks.txt"

MODEL_NAME = "all-MiniLM-L6-v2"

st.set_page_config(
    page_title="Employee Management RAG",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #666;
        margin-bottom: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(MODEL_NAME)

@st.cache_resource
def load_index():
    return faiss.read_index(str(INDEX_FILE))

@st.cache_data
def load_chunks():
    return CHUNKS_FILE.read_text(
        encoding="utf-8"
    ).split("\n\n---CHUNK_SEPARATOR---\n\n")

def search_knowledge(question, top_k=5):
    model = load_embedding_model()
    index = load_index()
    chunks = load_chunks()

    query_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    scores, ids = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], ids[0]):
        if 0 <= idx < len(chunks):
            results.append(
                {
                    "score": float(score),
                    "text": chunks[idx],
                }
            )

    return results

def build_answer(question, results):
    if not results:
        return "I could not find this information in the KT document."

    # Use the most relevant retrieved KT content directly.
    # This keeps the Render deployment lightweight and requires no LLM API.
    best = results[0]["text"].strip()

    return (
        "Based on the Employee Management System KT:\n\n"
        + best
        + "\n\n"
        "This answer was retrieved from the project knowledge base."
    )

# Page content is rendered before loading ML models.
st.markdown(
    '<div class="main-title">Employee Management System - RAG Assistant</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">Ask questions about the Employee Management System KT.</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("RAG System")
    st.write("Knowledge Base: Employee Management KT")
    st.write("Vector Store: FAISS")
    st.write("Embedding Model: all-MiniLM-L6-v2")
    st.info("No OpenAI API, API key, .env file, Ollama, or paid API is required.")

if not INDEX_FILE.exists() or not CHUNKS_FILE.exists():
    st.error(
        "The RAG index is missing. Render must run "
        "`python ingest.py` during the build."
    )
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "Ask something about the Employee Management System..."
)

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the KT..."):
            try:
                results = search_knowledge(question)

                # Simple relevance threshold to avoid unrelated answers.
                if not results or results[0]["score"] < 0.25:
                    answer = (
                        "I could not find this information in the KT document."
                    )
                    results = []
                else:
                    answer = build_answer(question, results)

            except Exception as exc:
                answer = f"Unable to search the knowledge base: {exc}"
                results = []

        st.markdown(answer)

        if results:
            with st.expander("Retrieved KT Sections"):
                for number, result in enumerate(results, 1):
                    st.markdown(f"### Source {number}")
                    st.write(
                        f"Similarity: {result['score']:.3f}"
                    )
                    st.write(result["text"])

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
