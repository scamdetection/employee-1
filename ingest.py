from pathlib import Path
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent
DOC_FILE = BASE_DIR / "docs" / "employee_management_kt.md"
DATA_DIR = BASE_DIR / "data"
INDEX_FILE = DATA_DIR / "employee_kt.index"
CHUNKS_FILE = DATA_DIR / "chunks.txt"
MODEL_NAME = "all-MiniLM-L6-v2"

def split_text(text, chunk_size=900, overlap=120):
    paragraphs = [p.strip() for p in text.replace("\r\n", "\n").split("\n\n") if p.strip()]
    chunks, current = [], ""
    for paragraph in paragraphs:
        if len(current) + len(paragraph) + 2 <= chunk_size:
            current = paragraph if not current else current + "\n\n" + paragraph
        else:
            if current:
                chunks.append(current)
            overlap_text = current[-overlap:] if current else ""
            current = overlap_text + "\n\n" + paragraph if overlap_text else paragraph
    if current:
        chunks.append(current)
    return chunks

def main():
    if not DOC_FILE.exists():
        raise FileNotFoundError(f"KT file not found: {DOC_FILE}")

    text = DOC_FILE.read_text(encoding="utf-8")
    chunks = split_text(text)

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Creating embeddings...")
    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    ).astype("float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_FILE))
    CHUNKS_FILE.write_text(
        "\n\n---CHUNK_SEPARATOR---\n\n".join(chunks),
        encoding="utf-8"
    )

    print(f"RAG index created successfully. Chunks: {len(chunks)}")

if __name__ == "__main__":
    main()
