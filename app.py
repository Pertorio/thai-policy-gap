import streamlit as st
from src.pdf_parser import extract_text_from_pdf
from src.analyzer import (
    get_client,
    load_standard,
    map_standard,
    analyze_gap,
    summarize_document
)

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
con_button_lable = "Analyze"
con_succ_massage = "Information Receive. Start Analyzing"
con_no_policy_message = "Please select your prefer standard for gap analyzing process"
con_no_fileupload_message = "Please Upload your Data Governance Policy"

# When Analyze Button is triggered
if st.button(label=con_button_lable):
    if len(user_standard_choice) == 0:
        st.warning(con_no_policy_message)
        st.stop()

    if uploaded_file is None:
        st.warning(con_no_fileupload_message)
        st.stop()

    st.success(con_succ_massage)
    # User Input -> Turn PDF object into bytes-stream
    byte_uploaded_file = uploaded_file.getvalue()
    user_policy_string = extract_text_from_pdf(byte_uploaded_file)
    
    # Load Selected Standards -> Dict
    standard = load_standard(
        map_standard(user_standard_choice[0])
    )

    #Get Antrophic Client
    client = get_client()
    
    #Analyze Gap
    message = analyze_gap(
        client=client,
        standards=standard,
        policy_text=user_policy_string
    )
    # Cache the result data
    st.session_state.analysis_result = message
    st.write(message)

# Display Old Output if state is cached
if st.session_state.analysis_result is not None:
    st.json(st.session_state.analysis_result)



# โจทย์ลับ: เพิ่ม print ตรงนี้
print("--- script รันรอบใหม่ ---")