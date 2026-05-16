import pymupdf
import pymupdf4llm
import streamlit as st

@st.cache_data
def extract_text_from_pdf(file_bytes : bytes) -> str:
    doc = pymupdf.open(stream=file_bytes, filetype="pdf")
    all_text = []
    for page in doc: # iterate the document pages
        text = page.get_text()
        all_text.append(text)
    # all_text = [page.get_text for page in doc] #List Comprehension method
    doc.close()
    return "\n\n".join(all_text)

def extract_text_from_pdf_as_markdown(file_bytes: bytes):
    md_text = pymupdf4llm.to_markdown("input.pdf")

    # Write the text to some file in UTF8-encoding
    # pathlib.Path("output.md").write_bytes(md_text.encode())