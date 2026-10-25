"""
Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1
Category: Generative AI | Real Estate Decision Support | Platform ID: 6ac4c98d1dcde6d7857c1642

Master turnkey Streamlit application for autonomous PPE safety auditing,
concrete crack diagnostics, project cost & INR valuation, and weather-aware site advisory.
"""

import streamlit as st
import os

# Set page configuration with wide layout and custom title
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom styling and modules
from modules.styles import get_custom_css
from modules.gemini_client import test_gemini_connection, get_available_models
from modules.safety_audit import render_safety_audit_tab
from modules.crack_diagnostics import render_crack_diagnostics_tab
from modules.valuation_planning import render_valuation_planning_tab
from modules.site_assistant import render_site_assistant_tab

# Inject custom modern CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)


def init_session_state():
    """Initialize necessary session state variables."""
    if "api_key" not in st.session_state:
        st.session_state["api_key"] = os.environ.get("GEMINI_API_KEY", "")
    if "force_demo_mode" not in st.session_state:
        st.session_state["force_demo_mode"] = False


init_session_state()

# =========================================================================
# SIDEBAR: API Key, Architecture Overview, and Quick Start
# =========================================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-box">
        <div style="font-size: 2.2rem; margin-bottom: 4px;">🏗️</div>
        <h3 style="color: #F8FAFC; margin: 0; font-size: 1.15rem; font-weight: 700;">Construction AI</h3>
        <p style="color: #94A3B8; font-size: 0.75rem; margin: 0;">Decision Support Platform</p>
        <div style="margin-top: 8px;">
            <span class="pill pill-info" style="font-size: 0.7rem;">ID: 6ac4c98d1dcde6d7857c1642</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔑 Multimodal LLM Config")
    
    api_key_input = st.text_input(
        "Google Gemini API Key:",
        value=st.session_state.get("api_key", ""),
        type="password",
        help="Input your Google AI Studio Gemini API Key. If left blank, system runs in High-Precision Demonstration Mode."
    )
    st.session_state["api_key"] = api_key_input

    model_options = get_available_models()
    selected_model = st.selectbox(
        "Vision Model Engine:",
        model_options,
        index=0,
        help="Gemini 1.5 Flash provides optimal speed and sub-second reasoning for multimodal vision inspection."
    )

    col_test, col_demo = st.columns(2)
    with col_test:
        if st.button("🔌 Test Key", use_container_width=True):
            if api_key_input:
                with st.spinner("Connecting..."):
                    valid, msg = test_gemini_connection(api_key_input, selected_model)
                    if valid:
                        st.success("Connected!")
                    else:
                        st.error(msg)
            else:
                st.warning("Key is empty.")

    with col_demo:
        demo_toggle = st.toggle("Demo Mode", value=not bool(api_key_input), help="Run without an active Gemini API key using benchmark datasets.")
        st.session_state["force_demo_mode"] = demo_toggle

    if not api_key_input or st.session_state["force_demo_mode"]:
        st.markdown("""
        <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 8px; padding: 8px; margin-top: 6px; font-size: 0.78rem; color: #FDE68A;">
            ⚡ <strong>Demonstration Mode Active:</strong> Fully functional offline benchmark suite enabled with zero API dependencies.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Architecture Overview
    st.markdown("### 🏛️ Architecture & Standards")
    st.markdown("""
    - **Epic 1:** Requirements & Environment
    - **Epic 2:** PPE Vision & Crack Diagnostics
    - **Epic 3:** Planning & Real Estate Valuation
    - **Epic 4:** Multimodal AI & JSON Contracts
    - **Epic 5:** Site Chatbot & Weather Advisory
    - **Epic 6:** Community Cloud Turnkey Deployment
    """)

    st.markdown("##### 📜 Regulatory Standards:")
    st.markdown("""
    - **OSHA 1926:** Construction Safety
    - **IS 456:2000:** Plain & Reinforced Concrete
    - **IS 13935:2020:** Seismic Strengthening
    - **ACI 224.1R:** Concrete Defect Evaluation
    - **NBC 2016:** National Building Code
    """)

    st.markdown("---")
    st.caption("Multimodal Construction Intelligence Platform • Capstone Project 1 • Production Ready")


# =========================================================================
# MAIN CONTENT HERO HEADER
# =========================================================================
st.markdown("""
<div class="hero-header">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
        <div>
            <div class="hero-meta-badge">Skill Wallet Capstone Project 1 • Generative AI & Real Estate</div>
            <h1 class="hero-title">Multimodal Construction Intelligence Platform</h1>
            <p class="hero-subtitle">
                Autonomous decision-support ecosystem analyzing site imagery for OSHA/IS 456 PPE safety audits,
                crack defect classification, dynamic CapEx & INR market valuation, and weather-aware hazard protocols.
            </p>
        </div>
        <div style="text-align: right;">
            <span class="pill pill-compliant" style="font-size: 0.82rem; padding: 5px 14px;">Platform Online</span>
            <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">Zero DB Dependency • 1-Click Deploy</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================================
# TABS NAVIGATION
# =========================================================================
tab_safety, tab_cracks, tab_valuation, tab_assistant = st.tabs([
    "🦺 1. PPE Safety Audit (Epic 2)",
    "🔬 2. Crack Diagnostics (Epic 2)",
    "📊 3. Planning & Valuation (Epic 3)",
    "⛅ 4. Site Assistant & Weather (Epic 5)"
])

# Pass effective API key (empty if demo mode is forced)
effective_api_key = "" if st.session_state["force_demo_mode"] else st.session_state["api_key"]

with tab_safety:
    render_safety_audit_tab(api_key=effective_api_key, selected_model=selected_model)

with tab_cracks:
    render_crack_diagnostics_tab(api_key=effective_api_key, selected_model=selected_model)

with tab_valuation:
    render_valuation_planning_tab()

with tab_assistant:
    render_site_assistant_tab(api_key=effective_api_key, selected_model=selected_model)
