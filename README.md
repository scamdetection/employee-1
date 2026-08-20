# Employee Management RAG - Render Fixed Version

## Render service type
Web Service

## Build Command
pip install -r requirements.txt && python ingest.py

## Start Command
python -m streamlit run app.py --server.address 0.0.0.0 --server.port $PORT

## Environment Variables
None.

## API
No OpenAI API, no API key, no .env, no Ollama, and no paid LLM API.

## Architecture
KT -> chunking -> Sentence Transformers -> FAISS -> similarity search -> retrieved answer -> Streamlit

The Streamlit configuration disables CORS/XSRF conflicts that can cause a blank page behind a reverse proxy.
