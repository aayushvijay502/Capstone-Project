"""
Tab 1: Site Safety & PPE Audit Module (Epic 2).
Conducts multimodal vision-based audits on construction site imagery under OSHA & IS 456 standards.
"""

import streamlit as st
from PIL import Image
import json
import plotly.graph_objects as go
from typing import Dict, Any, Optional

from modules.gemini_client import call_multimodal_gemini
from modules.sample_data import generate_sample_ppe_image, SAMPLE_PPE_AUDIT_DATA


PPE_SYSTEM_INSTRUCTION = """
You are an OSHA Lead Construction Safety Auditor and an Indian Bureau of Standards (IS 456 / IS 3521 / IS 2925) compliance officer.
Analyze the provided construction site photograph with meticulous technical rigor.
You MUST output ONLY a valid, parseable JSON object matching this exact schema:
{
  "safety_score": <integer from 0 to 100>,
  "overall_status": "<Compliant | Conditional Pass - Action Required | Non-Compliant - Immediate Stop-Work>",
  "standards_compliance": {
    "OSHA_1926_28": "<summary status>",
    "IS_456_2000_Safety": "<summary status>"
  },
  "workers_detected": <integer>,
  "ppe_detection": [
    {
      "item": "<Item name e.g. Industrial Hardhats (IS 2925), High-Vis Vests, Steel-Toe Boots, Fall Harness>",
      "detected_count": <integer>,
      "missing_count": <integer>,
      "status": "<Compliant | Partial | Violation | Critical Breach | Not Applicable>"
    }
  ],
  "identified_hazards": [
    {
      "hazard": "<Specific description of hazard observed>",
      "severity": "<Low | Medium | High | Critical>",
      "osha_reference": "<e.g. OSHA 1926.501>",
      "is_standard": "<e.g. IS 3521 / IS 456 Cl 41>",
      "immediate_remedy": "<Clear, actionable engineering corrective measure>"
    }
  ],
  "recommendations": [
    "<High priority site management recommendation 1>",
    "<Recommendation 2>"
  ]
}
Do NOT include markdown formatting or commentary outside the JSON object.
"""

PPE_USER_PROMPT = """
Perform an exhaustive multimodal Site Safety and PPE Audit on this construction site image.
1. Detect all visible personnel, machinery, and working conditions.
2. Inspect Personal Protective Equipment (PPE) compliance including helmets/hard hats, high-visibility reflective vests, steel-toe safety footwear, fall arrest harnesses/lanyards at elevated ledges, eye protection, and gloves.
3. Identify all physical and procedural hazards (unprotected slab edges, missing guardrails, unbraced scaffolding, tripping hazards, electrical cables near wet concrete).
4. Benchmark against OSHA 1926 Safety & Health Regulations for Construction and Indian Standards (IS 456:2000, IS 2925, IS 3521).
5. Output structured JSON adhering strictly to the required schema.
"""


def render_safety_score_gauge(score: int):
    """Render a sleek, semi-circular radial gauge for safety compliance score."""
    if score >= 80:
        bar_color = "#10B981"  # Emerald
    elif score >= 50:
        bar_color = "#F59E0B"  # Amber
    else:
        bar_color = "#EF4444"  # Crimson

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={'suffix': "/100", 'font': {'size': 38, 'color': '#F8FAFC', 'family': 'Space Grotesk'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#64748B'},
            'bar': {'color': bar_color, 'thickness': 0.3},
            'bgcolor': 'rgba(30, 41, 59, 0.5)',
            'borderwidth': 1,
            'bordercolor': 'rgba(255, 255, 255, 0.1)',
            'steps': [
                {'range': [0, 49], 'color': 'rgba(239, 68, 68, 0.15)'},
                {'range': [50, 79], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [80, 100], 'color': 'rgba(16, 185, 129, 0.15)'}
            ],
            'threshold': {
                'line': {'color': '#F59E0B', 'width': 3},
                'thickness': 0.75,
                'value': 75
            }
        }
    ))
    fig.update_layout(
        height=210,
        margin=dict(l=20, r=20, t=25, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig


def render_safety_audit_tab(api_key: Optional[str], selected_model: str):
    """Render the full Site Safety & PPE Audit UI and workflow."""
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
        <div>
            <h3 style="margin: 0; color: #F8FAFC; font-weight: 700;">🦺 Site Safety & PPE Compliance Audit</h3>
            <p style="margin: 0; color: #94A3B8; font-size: 0.9rem;">
                Autonomous OSHA 1926 & IS 456 visual compliance inspection powered by Gemini Multimodal Vision
            </p>
        </div>
        <span class="hero-meta-badge">Epic 2 • Vision AI</span>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_preview = st.columns([1, 1], gap="medium")

    with col_input:
        st.markdown('<div class="content-box content-box-amber">', unsafe_allow_html=True)
        st.markdown("##### 📸 Select Site Inspection Source")
        
        input_source = st.radio(
            "Image Input Mode:",
            ["Use Curated Benchmark Sample (Zone 4B Active Slab)", "Upload Custom Site Photo (JPG/PNG)"],
            label_visibility="collapsed"
        )
        
        target_image = None
        if "Benchmark" in input_source:
            st.info("💡 Loading pre-configured high-rise concrete slab photo with compliant & non-compliant workers.")
            target_image = generate_sample_ppe_image()
            use_sample_fallback = True
        else:
            uploaded_file = st.file_uploader(
                "Upload Construction Site Photo",
                type=["jpg", "jpeg", "png"],
                help="Accepts high-resolution JPG or PNG images of construction site zones, scaffolding, or workers."
            )
            if uploaded_file is not None:
                try:
                    target_image = Image.open(uploaded_file).convert("RGB")
                    use_sample_fallback = False
                except Exception as e:
                    st.error(f"Error opening image: {e}")
            else:
                st.caption("Awaiting site photo upload or choose the benchmark sample above.")
                use_sample_fallback = True

        st.markdown("<br>", unsafe_allow_html=True)
        audit_btn = st.button("🚀 Run Multimodal Safety Audit", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_preview:
        if target_image:
            st.image(target_image, caption="Inspected Site Imagery (Active ROI)", use_container_width=True)
        else:
            st.info("Upload or select a photo on the left to preview.")

    # Execute Audit when button clicked or if state already has results
    session_key = "safety_audit_result"
    
    if audit_btn and target_image:
        with st.spinner("Analyzing site imagery with Gemini Vision neural pipeline..."):
            fallback_dataset = SAMPLE_PPE_AUDIT_DATA if use_sample_fallback else None
            
            result_json, is_demo, msg = call_multimodal_gemini(
                image=target_image,
                prompt=PPE_USER_PROMPT,
                api_key=api_key,
                model_name=selected_model,
                system_instruction=PPE_SYSTEM_INSTRUCTION,
                demo_fallback_data=fallback_dataset
            )
            
            st.session_state[session_key] = {
                "data": result_json,
                "is_demo": is_demo,
                "message": msg
            }

    # Render results if available
    if session_key in st.session_state:
        res = st.session_state[session_key]
        audit_data = res["data"]
        is_demo = res["is_demo"]
        status_msg = res["message"]

        st.markdown("---")
        
        if is_demo:
            st.warning(f"ℹ️ {status_msg}")
        else:
            st.success(f"✅ {status_msg}")

        # Top Metric Cards
        score = audit_data.get("safety_score", 0)
        overall_status = audit_data.get("overall_status", "Audited")
        workers_count = audit_data.get("workers_detected", "N/A")
        hazards = audit_data.get("identified_hazards", [])
        critical_count = sum(1 for h in hazards if h.get("severity", "").lower() == "critical")

        c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])

        with c1:
            st.plotly_chart(render_safety_score_gauge(score), use_container_width=True)

        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Site Safety Status</div>
                <div class="metric-value" style="font-size: 1.15rem; margin-top: 10px; color: {'#10B981' if score>=80 else ('#F59E0B' if score>=50 else '#EF4444')};">
                    {overall_status}
                </div>
                <div style="margin-top: 8px;">
                    <span class="pill {'pill-compliant' if score>=80 else ('pill-warning' if score>=50 else 'pill-danger')}">
                        Score: {score}/100
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Personnel Observed</div>
                <div class="metric-value">{workers_count}</div>
                <div style="margin-top: 8px;">
                    <span class="pill pill-info">Active Shift</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Critical Hazards</div>
                <div class="metric-value" style="color: {'#EF4444' if critical_count > 0 else '#10B981'};">{critical_count}</div>
                <div style="margin-top: 8px;">
                    <span class="pill {'pill-danger' if critical_count > 0 else 'pill-compliant'}">
                        {'Immediate Action' if critical_count > 0 else 'Zero Breach'}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Tabular / Card Breakdown: PPE Detection & Identified Hazards
        col_ppe, col_hazards = st.columns([1, 1.2], gap="large")

        with col_ppe:
            st.markdown("#### 🛡️ PPE Detection & Compliance Breakdown")
            ppe_list = audit_data.get("ppe_detection", [])
            
            if ppe_list:
                for item in ppe_list:
                    name = item.get("item", "PPE Item")
                    detected = item.get("detected_count", 0)
                    missing = item.get("missing_count", 0)
                    status = item.get("status", "Unknown")
                    
                    status_class = "pill-compliant"
                    if "Violation" in status or "Breach" in status:
                        status_class = "pill-danger"
                    elif "Partial" in status or "Advisory" in status:
                        status_class = "pill-warning"

                    st.markdown(f"""
                    <div class="checklist-row">
                        <div>
                            <strong style="color: #F1F5F9; font-size: 0.9rem;">{name}</strong>
                            <div style="font-size: 0.78rem; color: #94A3B8;">
                                Detected: <span style="color:#10B981;">{detected}</span> | Missing: <span style="color:#EF4444;">{missing}</span>
                            </div>
                        </div>
                        <span class="pill {status_class}">{status}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("No PPE item breakdown provided in model output.")

            # Standards reference
            standards = audit_data.get("standards_compliance", {})
            if standards:
                st.markdown("<div style='margin-top: 1rem;'>", unsafe_allow_html=True)
                st.markdown("##### 📋 Standards Conformance Summary")
                for std, stat in standards.items():
                    st.markdown(f"**{std}:** `{stat}`")
                st.markdown("</div>", unsafe_allow_html=True)

        with col_hazards:
            st.markdown("#### ⚠️ Identified Site Hazards & Engineering Remedies")
            if hazards:
                for i, h in enumerate(hazards, 1):
                    hazard_title = h.get("hazard", f"Hazard #{i}")
                    severity = h.get("severity", "Medium")
                    osha_ref = h.get("osha_reference", "OSHA 1926")
                    is_ref = h.get("is_standard", "IS 456")
                    remedy = h.get("immediate_remedy", "Take standard mitigation measures.")

                    sev_class = "sev-medium"
                    if severity.lower() == "critical":
                        sev_class = "sev-critical"
                    elif severity.lower() == "high":
                        sev_class = "sev-high"
                    elif severity.lower() == "low":
                        sev_class = "sev-low"

                    st.markdown(f"""
                    <div class="content-box" style="padding: 1rem; margin-bottom: 0.8rem; border-left: 3px solid {'#EF4444' if severity.lower()=='critical' else ('#F97316' if severity.lower()=='high' else '#EAB308')};">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <strong style="color: #F8FAFC; font-size: 0.95rem;">{i}. {hazard_title}</strong>
                            <span class="{sev_class}">{severity.upper()}</span>
                        </div>
                        <div style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 6px;">
                            <span>📜 <strong>Ref:</strong> {osha_ref} | {is_ref}</span>
                        </div>
                        <div style="font-size: 0.85rem; color: #E2E8F0; background: rgba(15, 23, 42, 0.6); padding: 8px 10px; border-radius: 6px;">
                            <strong style="color: #FBBF24;">🛠️ Corrective Remedy:</strong> {remedy}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No active hazards identified in this scan.")

        # Recommendations list
        recs = audit_data.get("recommendations", [])
        if recs:
            st.markdown("##### 📌 High-Priority Supervisory Directives")
            for r in recs:
                st.markdown(f"- {r}")

        # Downloadable JSON report
        st.markdown("<br>", unsafe_allow_html=True)
        json_str = json.dumps(audit_data, indent=2)
        st.download_button(
            label="📥 Download Structured Safety Audit Report (JSON)",
            data=json_str,
            file_name=f"site_safety_audit_{audit_data.get('safety_score', 0)}.json",
            mime="application/json",
            use_container_width=True
        )
