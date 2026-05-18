from src.pdf_parser import extract_text_from_pdf
from src.rag_pipline import (
    chunk_text, 
    build_index, 
    get_voyage_client
)
from src.analyzer import (
    get_client, 
    load_standard, 
    map_standard, 
    analyze_gap_with_rag
)
import json


with open("/home/pertorio/Downloads/DGA6.pdf", "rb") as f:
    pdf_bytes = f.read()

print("📄 Reading PDF...")
text = extract_text_from_pdf(pdf_bytes)

# 2. สร้าง RAG index
print("🔢 Building RAG index...")
voyage_client = get_voyage_client()
chunks = chunk_text(text)
collection = build_index(voyage_client, chunks)

# 3. โหลด standard
print("📋 Loading standard...")
standard = load_standard(map_standard("มรด. 6"))

# 4. Analyze
print("🤖 Analyzing with RAG...")
import time
t0 = time.time()
anthropic_client = get_client()
result = analyze_gap_with_rag(
    antropic_client=anthropic_client,
    voyageai_client=voyage_client,
    collection=collection,
    standards=standard,
)
print(f"   Done in {time.time()-t0:.1f}s")

# 5. แสดงผล
print(f"\n📊 Overall score: {result['overall_score']}")
print(f"📋 Total gaps: {len(result['gaps'])}")

# นับตามสถานะ
from collections import Counter
levels = Counter(g["compliance_level"] for g in result["gaps"])
print(f"   Full: {levels['full']}, Partial: {levels['partial']}, Missing: {levels['missing']}")

# ดูผลแบบ raw
print("\n📝 Summary:", result["summary"])