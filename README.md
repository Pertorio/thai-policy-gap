# 📋 Thai Policy Gap Analyzer

> AI-powered gap analysis tool for Thai data governance policies — built with Claude + RAG

Compare Thai government data governance policies against official standards (PDPA, มรด. 3-1, มรด. 5, มรด. 6, etc.) using Claude AI with Retrieval-Augmented Generation.

## 🎯 What it does

Upload a Thai data governance policy document (PDF), select a reference standard, and get:

- **Executive dashboard** with compliance score
- **Per-requirement gap analysis** with 3-level compliance assessment (full / partial / missing)
- **Evidence citations** from the source document
- **Actionable recommendations** for each gap

## 🏗️ Architecture
PDF → Text extraction → Chunking → Embedding (Voyage AI)
↓
ChromaDB (vector store)
↓
Checklist (YAML) → Retrieval → Claude (gap analysis) → JSON results
↓
Streamlit dashboard

### Tech stack
- **LLM**: Claude (Haiku 4.5 + Sonnet 4.5 with model routing)
- **Embeddings**: Voyage AI (voyage-3.5, 1024-dim, multilingual)
- **Vector DB**: ChromaDB (in-memory)
- **UI**: Streamlit
- **PDF**: PyMuPDF

## 🧠 Engineering highlights

- **2-dimensional compliance schema** — `found_in_document × compliance_level` (full/partial/missing) reflecting how compliance auditors actually think
- **Output validation layer** — Detects LLM hallucinations via invalid combinations (In development)
- **Model routing** — Auto-selects Haiku vs Sonnet based on document complexity (In development)
- **Batch processing with retry** — Production-grade embedding pipeline with rate-limit handling
- **Streamlit session state** — Persists results across reruns

## 🚀 Getting started

### Prerequisites
- Python 3.10+
- Anthropic API key
- Voyage AI API key

### Setup
```bash
git clone https://github.com/your-username/thai-policy-gap.git
cd thai-policy-gap
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Configuration
Create `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
VOYAGE_API_KEY = "pa-..."
```

### Run
```bash
streamlit run app.py
```

## 📁 Project structure
thai-policy-gap/
├── app.py                       # Streamlit entry point
├── src/
│   ├── pdf_parser.py           # PDF text extraction
│   ├── rag_pipeline.py         # Chunking, embedding, retrieval
│   ├── analyzer.py             # Claude integration + gap analysis
│   └── render_dashboard.py     # UI components
├── standards/                  # YAML checklists per standard
│   ├── DGS3-1.yaml
│   ├── DGS3-2.yaml
│   ├── DGS4-1.yaml
│   ├── DGS4-2.yaml
│   ├── DGS_5.yaml
│   ├── DGS_6.yaml
│   ├── DGS_8.yaml
│   └── PDPA.yaml
└── requirements.txt

## 🎓 Context

Built as a 14-day learning project to apply concepts from the Data Governance Professiona to a real-world data governance use case in the Thai public sector.

## 📜 License
MIT