import anthropic
import streamlit as st
import json
import yaml

def get_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

STANDARD_PATHS = {
    "PDPA":"standards/PDPA.yaml",
    "มรด. 3-1":"standards/DGS3-1.yaml",
    "มรด. 3-2":"standards/DGS3-2.yaml",
    "มรด. 4-1":"standards/DGS4-1.yaml",
    "มรด. 4-2":"standards/DGS4-2.yaml",
    "มรด. 5":"standards/DGS5.yaml",
    "มรด. 6":"standards/DGS6.yaml",
    "มรด. 8":"standards/DGS8.yaml"
}


# Load Standard Data from YAML file
def load_standard(standard_code: str):
    with open(file=standard_code, encoding="utf-8") as f:
        foo = yaml.safe_load(f)
        return foo

# Converting Standard Option into Filename    
def map_standard(standard_name: str) -> str:
    """แปลงชื่อมาตรฐานที่ user เลือก → path ของ YAML file"""
    if standard_name not in STANDARD_PATHS:
        raise ValueError(f"ยังไม่รองรับมาตรฐาน: {standard_name}")
    return STANDARD_PATHS[standard_name]
    
def analyze_gap(client:anthropic.Anthropic, standards:dict, policy_text: str) -> dict:
    output_format_example = """
    {
            "gaps": [
                {
                    "checklist_id": "PDPA-01",
                    "requirement": "...",
                    "found_in_document": true/false,
                    "evidence": "ข้อความอ้างอิง หรือ null",
                    "severity": "high/medium/low",
                    "recommendation": "..."
                },
                ...
                    ],
            "overall_score": 75,
            "summary": "สรุปแบบกระชับ 1 ย่อหน้า"
        }
    """

    prompt_message = f"""
    <instruction>
    ตอบเป็นรูปแบบของ JSON
    คุณเป็นผู้เชี่ยวชาญด้านธรรมาภิบาลข้อมูล
    สิ่งที่ต้องทำคือตรวจสอบนโยบายว่ามีช่องว่าง (GAP) ในส่วนไหนบ้างเมื่อเทียบกับมาตรฐานที่กำหนด
    </instruction>
    นโยบาย: <document>{policy_text}</document>
    มาตรฐานเปรียบเทียบ: <checklist>{standards}</checklist>
    รูปแบบผลลัพธ์ที่ต้องการ (Output Format): <example>{output_format_example}</example>
    """
    
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens= 8192,
        messages=[
            {
                "role":"user",
                "content": prompt_message
            }
        ]
    )
    #print(message)
    return message

def summarize_document(client : anthropic.Anthropic,text: str) -> str:
    prompt_message=f"""
    ตอบเป็นภาษาไทย
    คุณคือผู้เชี่ยวชาญด้านธรรมาภิบาลข้อมูล
    สรุปเนื้อหาในเอกสารต่อไปนี้ให้เป็น bullet points 3-5 ข้อ เน้นใจความสำคัญที่กระชับและเข้าใจง่าย
    <document>
    {text}
    </document>"""
    
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt_message 
            }
        ]
    )
    return message.content[0].text