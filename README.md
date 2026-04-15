# 〽️ UMD Student Assistant

An AI-powered chatbot that answers questions about the University of Michigan-Dearborn using a RAG (Retrieval-Augmented Generation) pipeline.

## What it does

Students can ask natural language questions about UM-Dearborn: admissions, academics, campus life, financial aid, campus safety, and more and get accurate answers pulled directly from the university's website.

## How it works

- **Scraper** crawls 100+ pages from umdearborn.edu, extracts clean text using BeautifulSoup, and saves each page as a `.txt` file
- **Ingest pipeline** splits each page into 500-character chunks with 50-character overlap, converts them to vector embeddings, and stores all 1,370 chunks in ChromaDB
- **Query** takes the student's question, converts it to an embedding, and searches ChromaDB for the 3 most semantically similar chunks
- **Claude** receives those chunks as context and generates a natural language answer with no hallucination, only what's in the data

## Tech stack

- **Python** — core language
- **BeautifulSoup** — web scraping
- **ChromaDB** — vector database for semantic search
- **Anthropic Claude API** — LLM for generating answers model used: claude-haiku-4-5-20251001
- **Streamlit** — frontend UI

## Setup

```bash
# Clone the repo
git clone https://github.com/adamh36/umd-assistant.git
cd umd-assistant

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your API key
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# Run the scraper (optional - data already included)
python scraper.py

# Build the vector database
python ingest.py

# Launch the app
streamlit run app.py
```
## Project structure
```
umd-assistant/
  scraper.py      → crawls umdearborn.edu, saves pages to /data
  ingest.py       → chunks text, embeds, stores in ChromaDB
  app.py          → Streamlit UI + RAG query + Claude response
  data/           → scraped text files from 100 UMD pages
  images/         → UI assets
  chroma_db/      → persistent vector database (gitignored)
  .env            → API keys (gitignored)
```

## Future improvements

- Re-indexing pipeline to auto-update when UMD website changes
- Expand to 300+ pages for broader coverage
