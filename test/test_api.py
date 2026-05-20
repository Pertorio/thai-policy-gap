from src.rag_pipeline import chunk_text

sample = "ABCDEFGHI" * 200  # 2000 ตัวอักษร
chunks = chunk_text(sample, chunk_size=800, overlap=100)

print(f"จำนวน chunks: {len(chunks)}")
print(f"ความยาวแต่ละ chunk: {[len(c) for c in chunks]}")
print(f"Chunk 1 ลงท้ายด้วย: ...{chunks[0][-30:]}")
print(f"Chunk 2 ขึ้นต้นด้วย: {chunks[1][:30]}...")