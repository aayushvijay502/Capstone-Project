"""
Tab 4: Daily Site Assistant & Weather-Aware Advisory Module (Epic 5).
Features dynamic meteorological hazard engineering protocols (crane operations, IS 456 concrete curing,
electrical safety) and an interactive multi-turn civil engineering assistant chatbot.
"""

import streamlit as st
from typing import Optional, List, Dict
from modules.gemini_client import call_text_gemini


WEATHER_PROTOCOLS = {
    "🌪️ High Wind (>38 km/h Gale / Strong Gusts)": {
        "status_level": "extreme",
        "badge": "CRITICAL RISK - SUSPEND CRANE LIFTS",
        "crane_protocol": (
            "**IMMEDIATE CUTOFF (OSHA 1926.1400 / IS 13367):** Suspend all tower crane and mobile crane hoisting. "
            "Lower hooks to boom level and secure loose slings. For sustained winds >60 km/h, disengage tower crane "
            "slewing brakes to permit 360° free weathervaning to prevent mast torsion failure."
        ),
        "electrical_protocol": (
            "Inspect overhead high-tension line clearances. Ensure temporary site lighting masts and distributed power cords "
            "are lashed and anchored to prevent conductor whipping."
        ),
        "concrete_protocol": (
            "High wind accelerates surface evaporation, causing severe plastic shrinkage cracking. Apply aliphatic alcohol "
            "evaporation retarders immediately after screeding. Erect windbreaks around newly poured slabs."
        ),
        "scaffolding_protocol": (
            "Verify all external scaffolding wall ties (IS 3696 Part 1). Inspect debris containment netting; if winds exceed 50 km/h, "
            "furled or slit safety netting to minimize aerodynamic sail effect."
        )
    },
    "🌧️ Heavy Monsoon Rain & Waterlogging": {
        "status_level": "extreme",
        "badge": "SEVERE RISK - EXCAVATION & FLOODING",
        "crane_protocol": (
            "Inspect ground bearing capacity under outrigger crane mats. Saturated soil can lead to sudden differential outrigger "
            "settlement and crane overturning."
        ),
        "electrical_protocol": (
            "**HIGH SHOCK HAZARD:** De-energize unsealed distribution boards. Test all 30mA Earth Leakage Circuit Breakers (ELCB / RCCB). "
            "Elevate extension leads on insulated timber pegs off wet mud."
        ),
        "concrete_protocol": (
            "**IS 456 Cl 13.3:** Do NOT pour concrete during heavy downpours without continuous waterproof shelter. "
            "Rain alters the critical water-cement (w/c) ratio, washing away surface cement paste and destroying 28-day compressive strength. "
            "Keep polyethene tarpaulins unrolled on standby."
        ),
        "scaffolding_protocol": (
            "Check deep foundation pits and trench shoring. Soil saturation drastically increases lateral earth pressure; inspect "
            "for bank slippage and run continuous dewatering submersible pumps."
        )
    },
    "☀️ Extreme Ambient Heat (>40°C Summer Heatwave)": {
        "status_level": "warning",
        "badge": "HIGH RISK - HEAT STRESS & RAPID SLUMP LOSS",
        "crane_protocol": (
            "Hydraulic oil overheating alert. Monitor boom hydraulic fluid temperatures and inspect tire inflation pressures on mobile cranes."
        ),
        "electrical_protocol": (
            "Cable thermal de-rating. Ensure transformers and temporary generators have unobstructed shade and ventilation to prevent thermal tripping."
        ),
        "concrete_protocol": (
            "**IS 456 Cl 14.1 & ACI 305R (Hot Weather Concreting):** Fresh concrete temperature must not exceed 32°C. "
            "Dose batching plant with chilled water or flaked ice. Reschedule major structural pours to night shifts (8 PM to 4 AM). "
            "Initiate wet hessian burlap ponding curing immediately upon initial set (extend curing to 10-14 days)."
        ),
        "scaffolding_protocol": (
            "Enforce OSHA heat illness prevention: mandatory 15-minute shaded rest intervals every 90 minutes. Provide electrolyte hydration stations."
        )
    },
    "❄️ Severe Cold Snap (<5°C Freezing Fog)": {
        "status_level": "warning",
        "badge": "MODERATE RISK - RETARDED HYDRATION",
        "crane_protocol": (
            "Perform warm-up idle cycling for crane hydraulics. Steel embrittlement inspection at sub-zero temperatures."
        ),
        "electrical_protocol": (
            "Verify condensation drain holes in outdoor junction boxes. Avoid cable stiffening and sheath cracking during uncoiling."
        ),
        "concrete_protocol": (
            "**IS 456 Cl 14.2 & ACI 306R (Cold Weather Concreting):** Hydration slows drastically below 5°C. "
            "Use warm mixing water, non-chloride accelerating admixtures, and wrap forms with insulated curing blankets. "
            "Do NOT strip formwork prematurely until maturity meters confirm required stripping strength."
        ),
        "scaffolding_protocol": (
            "Inspect scaffold walking boards for morning frost or black ice slip hazards. Spread sand on access ramps."
        )
    },
    "🌤️ Normal / Optimal Concreting Weather": {
        "status_level": "normal",
        "badge": "ALL OPERATIONS CLEARED FOR OPTIMAL PROGRESS",
        "crane_protocol": (
            "Standard lifting operations approved within certified load chart capacities. Conduct daily pre-shift limit switch test."
        ),
        "electrical_protocol": (
            "Routine weekly earth-pit resistance checks (< 2 Ohms per IS 3043)."
        ),
        "concrete_protocol": (
            "Standard IS 456 curing regime: 7 days ponding or wet burlap covering for Ordinary Portland Cement (OPC), 10 days for blended cements."
        ),
        "scaffolding_protocol": (
            "Standard Green-Tag inspection valid. Daily perimeter edge checks."
        )
    }
}


def render_site_assistant_tab(api_key: Optional[str], selected_model: str):
    """Render Tab 4 - Daily Site Assistant & Weather-Aware Advisory."""
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
        <div>
            <h3 style="margin: 0; color: #F8FAFC; font-weight: 700;">⛅ Daily Site Assistant & Weather Advisory</h3>
            <p style="margin: 0; color: #94A3B8; font-size: 0.9rem;">
                Dynamic meteorological safety protocol dispatching and interactive AI civil engineering assistant
            </p>
        </div>
        <span class="hero-meta-badge">Epic 5 • Site Bot</span>
    </div>
    """, unsafe_allow_html=True)

    # Weather Condition Selector Section
    st.markdown("#### 🌦️ Real-Time Site Weather Protocol Dispatcher")
    
    selected_weather = st.selectbox(
        "Current On-Site Meteorological Condition:",
        list(WEATHER_PROTOCOLS.keys()),
        index=0
    )

    proto = WEATHER_PROTOCOLS[selected_weather]
    lvl = proto["status_level"]
    badge_text = proto["badge"]

    # Banner
    banner_class = "weather-extreme" if lvl == "extreme" else ("weather-warning" if lvl == "warning" else "weather-normal")
    st.markdown(f"""
    <div class="weather-banner {banner_class}">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h5 style="margin: 0; font-size: 1.05rem;">{selected_weather}</h5>
            <span class="pill {'pill-danger' if lvl=='extreme' else ('pill-warning' if lvl=='warning' else 'pill-compliant')}">{badge_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Key Engineering Protocol Cards
    w1, w2 = st.columns(2)
    with w1:
        st.markdown(f"""
        <div class="content-box content-box-amber">
            <h5 style="color: #FBBF24; margin-top: 0;">🏗️ Tower & Mobile Crane Protocol</h5>
            <p style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.5; margin: 0;">
                {proto['crane_protocol']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="content-box content-box-blue">
            <h5 style="color: #38BDF8; margin-top: 0;">⚡ Electrical Hazard Mitigation</h5>
            <p style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.5; margin: 0;">
                {proto['electrical_protocol']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with w2:
        st.markdown(f"""
        <div class="content-box content-box-emerald">
            <h5 style="color: #34D399; margin-top: 0;">🧱 IS 456 Concrete Curing & Pouring</h5>
            <p style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.5; margin: 0;">
                {proto['concrete_protocol']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="content-box content-box-red">
            <h5 style="color: #F87171; margin-top: 0;">🪜 Scaffolding & Deep Excavation</h5>
            <p style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.5; margin: 0;">
                {proto['scaffolding_protocol']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Interactive Construction Engineering Assistant Chatbot
    st.markdown("#### 🤖 Chief Construction Engineering Assistant")
    st.caption("Ask questions regarding IS 456 clauses, OSHA safety, crack retrofitting, slump adjustments, or material ratios.")

    # Initialize session state chat
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = [
            {
                "role": "assistant",
                "content": (
                    "👋 **Namaste! I am your Senior Civil & Structural Intelligence Assistant.**\n\n"
                    "I am equipped with Indian Standard Codes (IS 456, IS 13935, IS 1893, NBC 2016) and OSHA 1926 standards. "
                    "How can I assist your site engineering and planning today?"
                )
            }
        ]

    # Quick prompt buttons
    st.markdown("##### ⚡ Quick Engineering Queries:")
    qc1, qc2, qc3, qc4 = st.columns(4)
    quick_query = None
    with qc1:
        if st.button("⏱️ IS 456 Curing Periods", use_container_width=True):
            quick_query = "What is the mandatory curing period under IS 456 for OPC and mineral admixture concrete?"
    with qc2:
        if st.button("🌪️ Crane Wind Limits", use_container_width=True):
            quick_query = "What are the OSHA and IS 13367 cutoff wind speed limits for tower crane operations?"
    with qc3:
        if st.button("🩹 2mm Shear Crack Repair", use_container_width=True):
            quick_query = "How do I repair an active 2.5 mm diagonal shear crack on an RC beam-column joint?"
    with qc4:
        if st.button("📊 Steel & Cement Ratios", use_container_width=True):
            quick_query = "What are the standard thumb rule quantities of reinforcement steel and cement per sq.ft in Indian construction?"

    # Display chat history
    for msg in st.session_state["chat_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle input (either from chat input or quick query button)
    user_input = st.chat_input("Type your engineering question here...")
    prompt_to_send = quick_query or user_input

    if prompt_to_send:
        # Append user message
        st.session_state["chat_messages"].append({"role": "user", "content": prompt_to_send})
        with st.chat_message("user"):
            st.markdown(prompt_to_send)

        # Generate bot response
        with st.chat_message("assistant"):
            with st.spinner("Consulting structural engineering knowledgebase..."):
                reply = call_text_gemini(
                    prompt=prompt_to_send,
                    api_key=api_key,
                    model_name=selected_model,
                    conversation_history=st.session_state["chat_messages"]
                )
                st.markdown(reply)

        st.session_state["chat_messages"].append({"role": "assistant", "content": reply})
        st.rerun()
