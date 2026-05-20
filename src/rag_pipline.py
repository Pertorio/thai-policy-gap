import voyageai
import streamlit as st
import chromadb
import time


def chunk_text(text: str, 
               chunk_size: int = 800, 
               overlap: int = 100
               ) -> list[str]:
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        
        if end >= len(text):
            break
    
    return chunks


@st.cache_resource
def get_voyage_client() -> voyageai.Client:
    return voyageai.Client(api_key=st.secrets["VOYAGEAI_API_KEY"])


def embed_chunks(
        client: voyageai.Client,
        chunks: list[str],
        batch_size: int = 100,
        sleep_between_batches: float = 0.5,
        ) -> list[list[float]]:

    all_embeddings = []
    total = len(chunks)
    total_batches = (total + batch_size - 1) // batch_size
    
    for batch_idx in range(0, total, batch_size):
        batch = chunks[batch_idx:batch_idx + batch_size]
        current_batch_num = batch_idx // batch_size + 1
        
        print(f"  📦 Batch {current_batch_num}/{total_batches} "
              f"({len(batch)} chunks)...")
        
        try:
            result = client.embed(
                texts=batch,
                model="voyage-3.5",
                input_type="document",
            )
            all_embeddings.extend(result.embeddings)
            
        except voyageai.error.RateLimitError:
            print(f"  ⏸️  Rate limit hit — waiting 60 seconds...")
            time.sleep(60)
            
            # Retry หลังรอ
            result = client.embed(
                texts=batch,
                model="voyage-3.5",
                input_type="document",
            )
            all_embeddings.extend(result.embeddings)
        
        # หน่วงระหว่าง batches (ยกเว้น batch สุดท้าย)
        if batch_idx + batch_size < total:
            time.sleep(sleep_between_batches)
    
    return all_embeddings


def embed_query(
        client: voyageai.Client,
        query: str
        ) -> list[float]:
    result = client.embed(
        texts=[query],
        model="voyage-3.5",
        input_type="query"
    )
    return result.embeddings[0]


# For User Policy Document
@st.cache_data
def build_index(
        voyage_client: voyageai.Client,
        chunks: list[str]
        ) -> chromadb.Collection:
    
    embeddings = embed_chunks(voyage_client, chunks)
    chroma_client = chromadb.Client()
    collection_name = "policy_chunks"
    try:
        chroma_client.delete_collection(collection_name)
    except Exception:
        pass
    
    collection = chroma_client.create_collection(name=collection_name)
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))]  
    )
    return collection


def search(
        collection: chromadb.Collection,
        voyage_client: voyageai.Client,
        query: str,
        top_k: int = 5
        ) -> list[str]:
    
    query_embedding = embed_query(voyage_client, query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k)
    return results["documents"][0]