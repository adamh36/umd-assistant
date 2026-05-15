# 〽️ UMD Student Assistant
An AI-powered chatbot that answers questions about the University of Michigan-Dearborn using a RAG (Retrieval-Augmented Generation) pipeline built with LangChain.
https://umd-assistant.streamlit.app/

## What it does
Students can ask natural language questions about UM-Dearborn: admissions, academics, campus life, financial aid, campus safety, and more and get accurate answers pulled directly from the university's website.

## How it works
- **Scraper** crawls 300+ pages from umdearborn.edu using Playwright to bypass bot detection, extracts clean text, and saves each page as a `.txt` file
- **Ingest pipeline** splits each page into 500-character chunks with 50-character overlap, converts them to vector embeddings using FastEmbed, and stores all chunks in ChromaDB via LangChain
- **Query** takes the student's question, converts it to an embedding, and searches ChromaDB for the 3 most semantically similar chunks
- **Claude** receives those chunks as context via a LangChain LCEL chain and generates a natural language answer grounded strictly in scraped university data
- **Memory** maintains conversation context across follow-up questions using LangChain's ChatMessageHistory

## Tech stack
- **Python** — core language
- **Playwright** — browser automation for scraping past Cloudflare bot detection
- **BeautifulSoup** — HTML parsing and text extraction
- **LangChain** — RAG pipeline orchestration (LCEL chains, prompt templates, retrievers, memory)
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
playwright install chromium
echo "ANTHROPIC_API_KEY=your-key-here" > .env
python scraper.py
python ingest.py
streamlit run app.py
```

## Project structure
```
umd-assistant/
  scraper.py      → crawls 300+ pages from umdearborn.edu using Playwright
  ingest.py       → chunks text, embeds with FastEmbed, stores in ChromaDB via LangChain
  rag.py          → LangChain LCEL chain with prompt template, memory, and generate_response()
  app.py          → Streamlit UI, calls generate_response() from rag.py
  data/           → scraped text files from 300+ UMD pages
  images/         → UI assets
  chroma_db/      → persistent vector database (gitignored)
  .env            → API keys (gitignored)
```

## Future improvements
- Re-indexing pipeline to auto-update when UMD website changes
- Pinecone migration for cloud-hosted vector storage
- LangGraph agent with multi-tool routing
