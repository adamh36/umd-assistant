# 〽️ UMD Student Assistant
An AI-powered chatbot that answers questions about the University of Michigan-Dearborn using a RAG (Retrieval-Augmented Generation) pipeline built with LangChain.

## What it does
Students can ask natural language questions about UM-Dearborn: admissions, academics, campus life, financial aid, campus safety, and more and get accurate answers pulled directly from the university's website.

## How it works
- **Scraper** crawls 100+ pages from umdearborn.edu, extracts clean text using BeautifulSoup, and saves each page as a `.txt` file
- **Ingest pipeline** splits each page into 500-character chunks with 50-character overlap, converts them to vector embeddings using FastEmbed, and stores all 1,370 chunks in ChromaDB via LangChain
- **Query** takes the student's question, converts it to an embedding, and searches ChromaDB for the 3 most semantically similar chunks
- **Claude** receives those chunks as context via a LangChain LCEL chain and generates a natural language answer with no hallucination, only what's in the data

## Tech stack
- **Python** — core language
- **BeautifulSoup** — web scraping
- **LangChain** — RAG pipeline orchestration (LCEL chains, prompt templates, retrievers)
- **FastEmbed** — lightweight embedding model (all-MiniLM-L6-v2 via ONNX)
- **ChromaDB** — vector database for semantic search
- **Anthropic Claude API** — LLM for generating answers (claude-sonnet-4-20250514)
- **Streamlit** — frontend UI

## Setup
```bash
git clone https://github.com/adamh36/umd-assistant.git
cd umd-assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=your-key-here" > .env
python scraper.py
python ingest.py
streamlit run app.py
```

## Project structure
```
umd-assistant/
  scraper.py      → crawls umdearborn.edu, saves pages to /data
  ingest.py       → chunks text, embeds with FastEmbed, stores in ChromaDB via LangChain
  rag.py          → defines LangChain LCEL chain with prompt template and generate_response()
  app.py          → Streamlit UI, calls generate_response() from rag.py
  data/           → scraped text files from 100+ UMD pages
  images/         → UI assets
  chroma_db/      → persistent vector database (gitignored)
  .env            → API keys (gitignored)
```

## Future improvements
- Re-indexing pipeline to auto-update when UMD website changes
- Expand to 300+ pages for broader coverage
- LangGraph agent with multi-tool routing
- Docker + AWS deployment
