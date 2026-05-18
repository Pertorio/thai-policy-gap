import streamlit as st

def render_results(result: dict):

    # GAP ID Status
    done = 0
    needs_update = 0 
    not_done = 0
    # Gap Severity
    high_risk = 0
    medium_risk = 0
    
    for gap in result["gaps"]:
        found = gap["found_in_document"]
        level = gap["compliance_level"]
        
        if found and level == "full":
            done += 1
        elif found and level == "partial":
            needs_update += 1
        elif not found:
            not_done += 1
        
        # นับ risk เฉพาะข้อที่ยังไม่ full
        if level != "full":
            if gap["severity"] == "high":
                high_risk += 1
            elif gap["severity"] == "medium":
                medium_risk += 1
    
    st.subheader("📊 ผลการวิเคราะห์")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 คะแนนรวม", f"{result['overall_score']}/100")
    col2.metric("✅ ทำได้ดี", done)
    col3.metric("⚠️ ต้องปรับปรุง", needs_update, delta_color="inverse")
    col4.metric("❌ ยังไม่ได้ทำ", not_done, delta_color="inverse")
    
    if high_risk + medium_risk > 0:
        st.warning(
            f"🔴 ความเสี่ยงสูง: {high_risk} ข้อ · "
            f"🟡 ความเสี่ยงกลาง: {medium_risk} ข้อ"
        )
    st.info(result["summary"])
    
    # Gap list 
    st.subheader("รายการตรวจสอบ")
    severity_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    
    # Group gaps by status (3 กลุ่ม)
    def status_of(gap):
        found = gap["found_in_document"]
        level = gap["compliance_level"]
        if found and level == "full":
            return "done"
        elif found and level == "partial":
            return "partial"
        else:
            return "missing"
    
    status_label = {
        "missing": ("❌ ยังไม่ได้ทำ — ต้องร่างเพิ่ม", "missing"),
        "partial": ("⚠️ ทำแล้วแต่ไม่ครบ — ต้องปรับปรุง", "partial"),
        "done":    ("✅ ทำได้ดี", "done"),
    }
    
    # แสดงเรียงตาม priority: missing → partial → done
    for status_key in ["missing", "partial", "done"]:
        label, _ = status_label[status_key]
        
        filtered = [g for g in result["gaps"] if status_of(g) == status_key]
        if not filtered:
            continue
        
        st.markdown(f"### {label} ({len(filtered)} ข้อ)")
        
        for gap in filtered:
            sev = severity_color[gap["severity"]]
            title = f"{sev} {gap['checklist_id']}: {gap['requirement']}"
            
            with st.expander(title):
                # Evidence
                if gap.get("evidence"):
                    st.success(f"**📄 พบในเอกสาร:** {gap['evidence']}")
                
                # Gap description
                if gap.get("gap_description"):
                    st.error(f"**🔍 ช่องว่าง:** {gap['gap_description']}")
                
                # Recommendation
                if gap.get("recommendation"):
                    st.markdown(f"**💡 คำแนะนำ:** {gap['recommendation']}")