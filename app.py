import streamlit as st
from src.pdf_parser import extract_text_from_pdf
from src.analyzer import (
    get_client,
    load_standard,
    map_standard,
    analyze_gap_with_rag_cache
)
from src.render_dashboard import (
    render_results,
    render_overview)
from src.utils import file_hash
from src.rag_pipeline import (
    get_voyage_client,
    chunk_text,
    build_index_cache)
import json

# Page Settings
st.set_page_config(page_title="Thai Data Governance Gap Finder", page_icon="📋")

# Body Elements
st.title("📋 Thai DG Gap Analyzer")
st.subheader("AI-Powered Data Governance Policy Gap Analyzer")

# File Uploader
uploaded_file = st.file_uploader(
    "อัปโหลดเอกสารนโยบาย (PDF)",
    type=["pdf"]
)

# State Initialization
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if uploaded_file:
    st.success(f"✅ ได้รับไฟล์: {uploaded_file.name}")
    st.write(f"ขนาด: {uploaded_file.size / 1024:.1f} KB")

# Standard Selector
standard_label = "มาตรฐานอ้างอิง"
standard_options = ["PDPA", 
                    "มรด. 3-1",
                    "มรด. 3-2",
                    "มรด. 4-1",
                    "มรด. 4-2",
                    "มรด. 5",
                    "มรด. 6",
                    "มรด. 8"]
user_standard_choice = st.multiselect(label=standard_label,
                                      options=standard_options)

# Button To Continue the workflow
continue_button_lable = "Analyze"
continue_succ_massage = "Information Receive. Start Analyzing"
continue_no_policy_message = "Please select your prefer standard for gap analyzing process"
continue_no_fileupload_message = "Please Upload your Data Governance Policy"

# When Analyze Button is triggered
if st.button(label=continue_button_lable):
    if len(user_standard_choice) == 0:
        st.warning(continue_no_policy_message)
        st.stop()

    if uploaded_file is None:
        st.warning(continue_no_fileupload_message)
        st.stop()

    st.success(continue_succ_massage)
    # User Input -> Turn PDF object into bytes-stream
    byte_uploaded_file = uploaded_file.getvalue()
    user_policy_string = extract_text_from_pdf(byte_uploaded_file)
    file_hash_key = file_hash(byte_uploaded_file)

    #Initiate Clients
    ai_client = get_client()
    voyageai_client = get_voyage_client()

    #Handle user's policy data
    chunks = chunk_text(user_policy_string)
    collection = build_index_cache(
        _voyage_client=voyageai_client,
        _chunks=chunks,
        file_hash_key=file_hash_key
    )
    
    # Load Selected Standards
    # standard = load_standard(
    #     map_standard(user_standard_choice[0])
    # )
    # Load Multiple Standards
    standards_list = []
    for standard in user_standard_choice:
        temp = load_standard(map_standard(standard))
        standards_list.append(temp)
        
    
    #Analyze Gap
    with st.spinner("🤖 กำลังให้ AI วิเคราะห์..."):
        results = []
        for standard in standards_list:
            std_name = standard.get("name", "")
            message = analyze_gap_with_rag_cache(
                file_hash_key=file_hash_key,
                standard_name=std_name,
                _anthropic_client=ai_client,
                _voyageai_client=voyageai_client,
                _collection=collection,
                _standards=standard,
                chunks_per_item=2)
            message["standard_name"] = std_name
            message["standard_short_code"] = standard.get("short_code", "")
            results.append(message)

    # Cache the result data
    st.session_state.analysis_result = results

# Display Old Output if state is cached
if st.session_state.analysis_result is not None:
    render_overview(st.session_state.analysis_result)
    for result in st.session_state.analysis_result:
        render_results(result=result)

# JSON download button
if st.session_state.analysis_result:
    json_str = json.dumps(
        st.session_state.analysis_result, 
        ensure_ascii=False,
        indent=2
    )
    st.download_button(
        label="📥 ดาวน์โหลด JSON",
        data=json_str,
        file_name="gap_analysis.json",
        mime="application/json"
    )