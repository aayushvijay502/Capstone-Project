"""
Tab 2: Crack Diagnostics & Structural Integrity Module (Epic 2).
Multimodal AI for concrete defect classification, crack width estimation, root-cause diagnosis,
and structural engineering repair specifications.
"""

import streamlit as st
from PIL import Image
import json
import plotly.graph_objects as go
from typing import Optional

from modules.gemini_client import call_multimodal_gemini
from modules.sample_data import generate_sample_crack_image, SAMPLE_CRACK_AUDIT_DATA


CRACK_SYSTEM_INSTRUCTION = """
You are a Senior Forensic Structural Engineer certified in ACI 224.1R (Concrete Crack Assessment) and IS 456 / IS 13935 standards.
Analyze the provided concrete or masonry surface photograph.
You MUST output ONLY a valid, parseable JSON object matching this exact schema:
{
  "defect_classification": "<Hairline | Settlement | Structural Shear | Thermal Expansion | Spalling>",
  "defect_confidence": <float between 0.0 and 1.0>,
  "structural_element": "<e.g. Reinforced Concrete Beam-Column Joint | Floor Slab | Masonry Infill Wall | Retaining Wall>",
  "estimated_width_mm": <float estimated crack width in millimeters>,
  "width_tolerance_range": "<e.g. 2.5 mm - 3.1 mm>",
  "crack_orientation": "<e.g. Diagonal 45-degree angle | Vertical flexural | Map/crazing pattern>",
  "severity_rating": "<Low | Medium | High | Critical>",
  "structural_risk_index": <integer from 0 to 100>,
  "root_causes": [
    "<Technical root cause 1>",
    "<Technical root cause 2>"
  ],
  "secondary_defects": [
    "<e.g. Delamination | Spalling | Efflorescence | Rebar corrosion rust stains>"
  ],
  "engineering_repair_specification": {
    "primary_protocol": "<e.g. High-Pressure Structural Epoxy Resin Injection | Polyurethane Grout | CFRP Wrap | V-Groove Elastomeric Sealant>",
    "epoxy_grade": "<e.g. Low-viscosity high-modulus epoxy conforming to ASTM C881 Type I & IV Grade 1>",
    "surface_preparation": "<Detailed surface prep instructions>",
    "injection_pressure": "<Pressure specification e.g. 0.2 to 0.4 N/mm² (30-60 psi)>",
    "structural_strengthening": "<Additional strengthening recommendations>",
    "urgency": "<Immediate (24-48 Hours) | High Priority (7 Days) | Medium (30 Days) | Routine Monitoring>"
  },
  "relevant_codes": [
    "<e.g. IS 456:2000 Cl 35.3.2>",
    "<ACI 224.1R-07>",
    "<IS 13935:2020>"
  ]
}
Do NOT include markdown formatting or commentary outside the JSON object.
"""

CRACK_USER_PROMPT = """
Inspect this structural surface image with high precision.
1. Classify the concrete defect type: Hairline (<0.3mm non-structural), Settlement, Structural Shear (diagonal 45° angle near supports), Thermal Expansion (cyclic joint movement), or Spalling (exposed aggregate/rebar).
2. Quantify crack width in millimeters with tolerance bounds.
3. Determine root causes (load-induced shear vs drying shrinkage vs rebar carbonation).
4. Provide standard structural rehabilitation methods (Epoxy injection ports, low-viscosity resin, CFRP composite jacketing, or polyurethane hydrophilic grouting) compliant with ACI 224.1R and IS 13935:2020.
5. Return strictly the requested JSON schema.
"""


def render_risk_gauge(risk_score: int):
    """Render semi-circular gauge for Structural Risk Index."""
    if risk_score >= 70:
        bar_color = "#EF4444"  # Red
    elif risk_score >= 40:
        bar_color = "#F59E0B"  # Amber
    else:
        bar_color = "#10B981"  # Emerald

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={'suffix': "/100", 'font': {'size': 38, 'color': '#F8FAFC', 'family': 'Space Grotesk'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#64748B'},
            'bar': {'color': bar_color, 'thickness': 0.3},
            'bgcolor': 'rgba(30, 41, 59, 0.5)',
            'borderwidth': 1,
            'bordercolor': 'rgba(255, 255, 255, 0.1)',
            'steps': [
                {'range': [0, 39], 'color': 'rgba(16, 185, 129, 0.15)'},
                {'range': [40, 69], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [70, 100], 'color': 'rgba(239, 68, 68, 0.15)'}
            ]
        }
    ))
    fig.update_layout(
        height=210,
        margin=dict(l=20, r=20, t=25, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig


def render_crack_diagnostics_tab(api_key: Optional[str], selected_model: str):
    """Render Tab 2 - Crack Diagnostics & Structural Integrity."""
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
        <div>
            <h3 style="margin: 0; color: #F8FAFC; font-weight: 700;">🔬 Crack Diagnostics & Structural Integrity</h3>
            <p style="margin: 0; color: #94A3B8; font-size: 0.9rem;">
                Sub-millimeter concrete defect classification, crack width estimation, and IS 13935 / ACI 224R repair engineering
            </p>
        </div>
        <span class="hero-meta-badge">Epic 2 • Defect Triage</span>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_preview = st.columns([1, 1], gap="medium")

    with col_input:
        st.markdown('<div class="content-box content-box-blue">', unsafe_allow_html=True)
        st.markdown("##### 🧱 Select Concrete Surface Image")
        
        input_source = st.radio(
            "Concrete Surface Source:",
            ["Use Curated Benchmark Sample (Beam-Column Shear Joint)", "Upload Custom Surface Photo (JPG/PNG)"],
            label_visibility="collapsed"
        )
        
        target_image = None
        if "Benchmark" in input_source:
            st.info("💡 Loading synthetic test scan of 45° diagonal shear fracture at RC beam-column junction.")
            target_image = generate_sample_crack_image()
            use_sample_fallback = True
        else:
            uploaded_file = st.file_uploader(
                "Upload Concrete / Masonry Image",
                type=["jpg", "jpeg", "png"],
                help="Accepts close-up or elevation photos of beams, columns, floor slabs, or retaining walls."
            )
            if uploaded_file is not None:
                try:
                    target_image = Image.open(uploaded_file).convert("RGB")
                    use_sample_fallback = False
                except Exception as e:
                    st.error(f"Error opening image: {e}")
            else:
                st.caption("Awaiting concrete surface image upload or select the benchmark sample above.")
                use_sample_fallback = True

        st.markdown("<br>", unsafe_allow_html=True)
        diag_btn = st.button("🔍 Run Structural Diagnostics Scan", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_preview:
        if target_image:
            st.image(target_image, caption="Concrete Surface Under Diagnostic Evaluation", use_container_width=True)
        else:
            st.info("Upload or select a concrete surface image on the left.")

    session_key = "crack_diag_result"
    
    if diag_btn and target_image:
        with st.spinner("Analyzing concrete morphology and stress trajectories..."):
            fallback_dataset = SAMPLE_CRACK_AUDIT_DATA if use_sample_fallback else None
            
            result_json, is_demo, msg = call_multimodal_gemini(
                image=target_image,
                prompt=CRACK_USER_PROMPT,
                api_key=api_key,
                model_name=selected_model,
                system_instruction=CRACK_SYSTEM_INSTRUCTION,
                demo_fallback_data=fallback_dataset
            )
            
            st.session_state[session_key] = {
                "data": result_json,
                "is_demo": is_demo,
                "message": msg
            }

    if session_key in st.session_state:
        res = st.session_state[session_key]
        diag_data = res["data"]
        is_demo = res["is_demo"]
        status_msg = res["message"]

        st.markdown("---")
        
        if is_demo:
            st.warning(f"ℹ️ {status_msg}")
        else:
            st.success(f"✅ {status_msg}")

        # Metrics row
        defect_type = diag_data.get("defect_classification", "Unclassified")
        width_mm = diag_data.get("estimated_width_mm", "N/A")
        severity = diag_data.get("severity_rating", "Unknown")
        risk_index = diag_data.get("structural_risk_index", 50)
        confidence = diag_data.get("defect_confidence", 0.90)

        c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])

        with c1:
            st.plotly_chart(render_risk_gauge(risk_index), use_container_width=True)

        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Defect Classification</div>
                <div class="metric-value" style="font-size: 1.15rem; margin-top: 10px; color: #38BDF8;">
                    {defect_type}
                </div>
                <div style="margin-top: 8px;">
                    <span class="pill pill-info">Confidence: {int(confidence*100) if isinstance(confidence, float) else confidence}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Estimated Crack Width</div>
                <div class="metric-value" style="color: {'#EF4444' if width_mm > 1.0 else '#F59E0B'};">{width_mm} mm</div>
                <div style="margin-top: 8px;">
                    <span class="pill {'pill-danger' if width_mm > 1.0 else 'pill-warning'}">{diag_data.get('width_tolerance_range', 'Est.')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            sev_class = "pill-danger" if severity.lower() in ["critical", "high"] else "pill-warning"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Severity & Urgency</div>
                <div class="metric-value" style="font-size: 1.2rem; margin-top: 8px; color: {'#EF4444' if severity.lower() in ['critical', 'high'] else '#F59E0B'};">
                    {severity}
                </div>
                <div style="margin-top: 8px;">
                    <span class="pill {sev_class}">{diag_data.get('engineering_repair_specification', {}).get('urgency', 'Urgent Action')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Forensic Analysis & Recommended Engineering Repair Protocol
        col_causes, col_repairs = st.columns([1, 1.2], gap="large")

        with col_causes:
            st.markdown("#### 🔬 Forensic Etiology & Root Causes")
            st.markdown(f"**Structural Element Identified:** `{diag_data.get('structural_element', 'Concrete member')}`")
            st.markdown(f"**Fracture Orientation:** `{diag_data.get('crack_orientation', 'N/A')}`")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("##### 📌 Probable Causal Factors:")
            causes = diag_data.get("root_causes", [])
            for c in causes:
                st.markdown(f"- ⚠️ {c}")

            secondaries = diag_data.get("secondary_defects", [])
            if secondaries:
                st.markdown("##### ⚡ Secondary Structural Degradation:")
                for s in secondaries:
                    st.markdown(f"- 🔸 {s}")

            codes = diag_data.get("relevant_codes", [])
            if codes:
                st.markdown("##### 📚 Reference Structural Standards:")
                for cd in codes:
                    st.markdown(f"- 📄 `{cd}`")

        with col_repairs:
            st.markdown("#### 🛠️ Recommended Engineering Repair Protocol")
            repair = diag_data.get("engineering_repair_specification", {})
            
            st.markdown(f"""
            <div class="content-box content-box-emerald">
                <h5 style="color: #34D399; margin-top: 0;">Protocol: {repair.get('primary_protocol', 'Structural Injection')}</h5>
                <p style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 8px;">
                    <strong>Material Specification:</strong> {repair.get('epoxy_grade', 'ASTM C881 High Modulus Resin')}
                </p>
                <div style="background: rgba(15, 23, 42, 0.7); padding: 10px; border-radius: 8px; margin-bottom: 8px; font-size: 0.85rem;">
                    <strong style="color: #FBBF24;">1. Surface Preparation & Porting:</strong><br>
                    {repair.get('surface_preparation', 'Clean substrate and install ports.')}
                </div>
                <div style="background: rgba(15, 23, 42, 0.7); padding: 10px; border-radius: 8px; margin-bottom: 8px; font-size: 0.85rem;">
                    <strong style="color: #38BDF8;">2. Pressure Injection Regime:</strong><br>
                    {repair.get('injection_pressure', 'Inject at 0.2-0.4 MPa until refusal.')}
                </div>
                <div style="background: rgba(15, 23, 42, 0.7); padding: 10px; border-radius: 8px; font-size: 0.85rem;">
                    <strong style="color: #A78BFA;">3. Structural Strengthening & Containment:</strong><br>
                    {repair.get('structural_strengthening', 'CFRP composite jacketing.')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        json_str = json.dumps(diag_data, indent=2)
        st.download_button(
            label="📥 Download Forensic Diagnostic Report (JSON)",
            data=json_str,
            file_name=f"concrete_defect_audit_{defect_type.lower().replace(' ', '_')}.json",
            mime="application/json",
            use_container_width=True
        )
