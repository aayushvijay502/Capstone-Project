"""
Tab 3: Planning & Real Estate Valuation Module (Epic 3).
Computes project budgets, CapEx incurred, current asset market valuations in INR (Lakhs/Crores),
material requirement quantities (Steel MT / Cement Bags), milestone progress, and conceptual 3D architectural rendering.
"""

import streamlit as st
import urllib.parse
import plotly.graph_objects as go
from typing import Dict, Any, Tuple


# Standard benchmark rates (INR per sq.ft) by typology and city tier
CONSTRUCTION_RATES = {
    "Residential High-Rise (G+24)": {
        "Tier 1 (Mumbai, Bengaluru, Delhi-NCR)": 2450,
        "Tier 2 (Pune, Ahmedabad, Hyderabad)": 2050,
        "Tier 3 (Indore, Coimbatore, Jaipur)": 1750,
        "steel_factor_kg_sqft": 4.2,
        "cement_factor_bags_sqft": 0.42,
        "concrete_factor_cum_sqft": 0.045
    },
    "Commercial IT Park & Office Tower": {
        "Tier 1 (Mumbai, Bengaluru, Delhi-NCR)": 3100,
        "Tier 2 (Pune, Ahmedabad, Hyderabad)": 2600,
        "Tier 3 (Indore, Coimbatore, Jaipur)": 2150,
        "steel_factor_kg_sqft": 4.8,
        "cement_factor_bags_sqft": 0.45,
        "concrete_factor_cum_sqft": 0.052
    },
    "Luxury Gated Villa Enclave": {
        "Tier 1 (Mumbai, Bengaluru, Delhi-NCR)": 3400,
        "Tier 2 (Pune, Ahmedabad, Hyderabad)": 2800,
        "Tier 3 (Indore, Coimbatore, Jaipur)": 2300,
        "steel_factor_kg_sqft": 3.8,
        "cement_factor_bags_sqft": 0.40,
        "concrete_factor_cum_sqft": 0.040
    },
    "Industrial Warehouse & PEB Logistics": {
        "Tier 1 (Mumbai, Bengaluru, Delhi-NCR)": 1850,
        "Tier 2 (Pune, Ahmedabad, Hyderabad)": 1550,
        "Tier 3 (Indore, Coimbatore, Jaipur)": 1350,
        "steel_factor_kg_sqft": 5.2,
        "cement_factor_bags_sqft": 0.30,
        "concrete_factor_cum_sqft": 0.035
    },
    "Mixed-Use Retail & Residential Hub": {
        "Tier 1 (Mumbai, Bengaluru, Delhi-NCR)": 2900,
        "Tier 2 (Pune, Ahmedabad, Hyderabad)": 2400,
        "Tier 3 (Indore, Coimbatore, Jaipur)": 1950,
        "steel_factor_kg_sqft": 4.5,
        "cement_factor_bags_sqft": 0.44,
        "concrete_factor_cum_sqft": 0.048
    }
}

MARKET_VALUATION_RATES = {
    "Tier 1 (Mumbai, Bengaluru, Delhi-NCR)": 14500,
    "Tier 2 (Pune, Ahmedabad, Hyderabad)": 8200,
    "Tier 3 (Indore, Coimbatore, Jaipur)": 4800
}


def format_inr(amount: float) -> str:
    """Format numerical currency into Indian numbering system (Crores or Lakhs)."""
    if amount >= 10000000:  # 1 Crore = 10,000,000
        val = amount / 10000000.0
        return f"₹ {val:,.2f} Cr"
    elif amount >= 100000:  # 1 Lakh = 100,000
        val = amount / 100000.0
        return f"₹ {val:,.2f} Lakhs"
    else:
        return f"₹ {amount:,.0f}"


def calculate_project_metrics(
    structure_type: str,
    city_tier: str,
    sqft: float,
    completion_pct: float,
    spec_tier: str
) -> Dict[str, Any]:
    """Calculate comprehensive cost, CapEx, valuation, and material requirements."""
    base_data = CONSTRUCTION_RATES[structure_type]
    base_rate = base_data[city_tier]
    
    # Adjust for specification tier
    spec_multiplier = 1.0
    if spec_tier == "Premium Spec (+18%)":
        spec_multiplier = 1.18
    elif spec_tier == "Ultra-Luxury / Platinum LEED (+35%)":
        spec_multiplier = 1.35
        
    effective_rate = base_rate * spec_multiplier
    total_budget = sqft * effective_rate
    capex_incurred = total_budget * (completion_pct / 100.0)
    
    # Material quantities
    steel_mt = (sqft * base_data["steel_factor_kg_sqft"]) / 1000.0
    steel_installed_mt = steel_mt * (completion_pct / 100.0)
    
    cement_bags = sqft * base_data["cement_factor_bags_sqft"]
    cement_consumed_bags = cement_bags * (completion_pct / 100.0)
    
    concrete_cum = sqft * base_data["concrete_factor_cum_sqft"]
    concrete_poured_cum = concrete_cum * (completion_pct / 100.0)
    
    # Real Estate Asset Valuation (Land + Structure + Work-In-Progress WIP Stage Premium)
    base_market_rate = MARKET_VALUATION_RATES[city_tier]
    full_market_valuation = sqft * base_market_rate * (1.1 if "Luxury" in structure_type else 1.0)
    
    # WIP Stage Valuation: Land & Substructure Base (35%) + Completed Superstructure (65% * completion)
    wip_valuation = full_market_valuation * (0.35 + (0.65 * (completion_pct / 100.0)))

    return {
        "effective_rate_sqft": effective_rate,
        "total_budget": total_budget,
        "capex_incurred": capex_incurred,
        "capex_remaining": total_budget - capex_incurred,
        "full_market_valuation": full_market_valuation,
        "current_asset_valuation": wip_valuation,
        "steel_total_mt": steel_mt,
        "steel_installed_mt": steel_installed_mt,
        "cement_total_bags": cement_bags,
        "cement_consumed_bags": cement_consumed_bags,
        "concrete_total_cum": concrete_cum,
        "concrete_poured_cum": concrete_poured_cum
    }


def render_cost_breakdown_pie(total_budget: float):
    """Plotly Donut Chart representing standard construction expenditure buckets."""
    labels = ["RCC & Structural Core", "Finishing & Facade", "MEP & Fire Engineering", "Preliminaries & Site Mgmt", "Contingency & Approvals"]
    values = [
        total_budget * 0.42,
        total_budget * 0.23,
        total_budget * 0.18,
        total_budget * 0.10,
        total_budget * 0.07
    ]
    colors = ["#F59E0B", "#38BDF8", "#10B981", "#818CF8", "#F43F5E"]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color='#0F172A', width=2)),
        textinfo='label+percent',
        insidetextorientation='radial',
        textfont=dict(color='#F8FAFC', family='Space Grotesk', size=11)
    )])

    fig.update_layout(
        showlegend=False,
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig


def render_valuation_planning_tab():
    """Render Tab 3 - Planning & Real Estate Valuation."""
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
        <div>
            <h3 style="margin: 0; color: #F8FAFC; font-weight: 700;">📊 Project Planning & Real Estate Valuation</h3>
            <p style="margin: 0; color: #94A3B8; font-size: 0.9rem;">
                CapEx forecasting, material logistics (IS 456), WIP asset valuation in INR, and 3D architectural rendering
            </p>
        </div>
        <span class="hero-meta-badge">Epic 3 • Cost & Valuation</span>
    </div>
    """, unsafe_allow_html=True)

    col_inputs, col_summary = st.columns([1.1, 1.3], gap="large")

    with col_inputs:
        st.markdown('<div class="content-box content-box-amber">', unsafe_allow_html=True)
        st.markdown("##### 🏗️ Project Parameters")

        structure_type = st.selectbox(
            "Structure Typology:",
            list(CONSTRUCTION_RATES.keys()),
            index=0
        )

        city_tier = st.selectbox(
            "Location Classification:",
            list(MARKET_VALUATION_RATES.keys()),
            index=0
        )

        spec_tier = st.selectbox(
            "Specification Quality Tier:",
            ["Standard Specification", "Premium Spec (+18%)", "Ultra-Luxury / Platinum LEED (+35%)"],
            index=0
        )

        col_sqft, col_rate = st.columns(2)
        with col_sqft:
            built_up_sqft = st.number_input(
                "Built-Up Area (Sq.Ft):",
                min_value=1000,
                max_value=2500000,
                value=75000,
                step=5000
            )

        completion_pct = st.slider(
            "Current Construction Milestone (% Completed):",
            min_value=0,
            max_value=100,
            value=58,
            step=1,
            help="Reflects the verified on-site physical progress according to RERA / PMC milestones."
        )

        st.markdown('</div>', unsafe_allow_html=True)

    # Compute metrics
    m = calculate_project_metrics(structure_type, city_tier, built_up_sqft, completion_pct, spec_tier)

    with col_summary:
        st.markdown("##### 💰 Financial & Asset Valuation Overview")
        
        # 4 Core KPI Metric Cards
        k1, k2 = st.columns(2)
        with k1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Project Budget</div>
                <div class="metric-value" style="color: #FBBF24;">{format_inr(m['total_budget'])}</div>
                <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 4px;">
                    ₹{int(m['effective_rate_sqft']):,}/sq.ft Base Cost
                </div>
            </div>
            """, unsafe_allow_html=True)

        with k2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">CapEx Incurred to Date</div>
                <div class="metric-value" style="color: #38BDF8;">{format_inr(m['capex_incurred'])}</div>
                <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 4px;">
                    {completion_pct}% Capital Disbursed
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

        k3, k4 = st.columns(2)
        with k3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Current Asset Valuation (WIP)</div>
                <div class="metric-value" style="color: #34D399;">{format_inr(m['current_asset_valuation'])}</div>
                <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 4px;">
                    Stage-adjusted market worth
                </div>
            </div>
            """, unsafe_allow_html=True)

        with k4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Completed Market Asset Value</div>
                <div class="metric-value" style="color: #A78BFA;">{format_inr(m['full_market_valuation'])}</div>
                <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 4px;">
                    Exit Market Cap Estimate
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Milestone Progress Tracker & Material Quantities
    col_materials, col_chart = st.columns([1.2, 1], gap="large")

    with col_materials:
        st.markdown("#### 📦 IS 456 Structural Material Requirements")
        
        # Steel
        st.markdown(f"""
        <div class="checklist-row">
            <div>
                <strong style="color: #F8FAFC;">🔩 Fe 550D TMT Reinforcement Steel</strong>
                <div style="font-size: 0.8rem; color: #94A3B8;">
                    Total Required: <strong>{m['steel_total_mt']:,.1f} MT</strong> | Installed to Date: <span style="color:#38BDF8;">{m['steel_installed_mt']:,.1f} MT</span>
                </div>
            </div>
            <span class="pill pill-info">{int(completion_pct)}% Cast</span>
        </div>
        """, unsafe_allow_html=True)

        # Cement
        st.markdown(f"""
        <div class="checklist-row">
            <div>
                <strong style="color: #F8FAFC;">🧱 OPC 53 Grade Cement (50kg Bags)</strong>
                <div style="font-size: 0.8rem; color: #94A3B8;">
                    Total Required: <strong>{int(m['cement_total_bags']):,} Bags</strong> | Consumed: <span style="color:#10B981;">{int(m['cement_consumed_bags']):,} Bags</span>
                </div>
            </div>
            <span class="pill pill-compliant">{int(completion_pct)}% Consumed</span>
        </div>
        """, unsafe_allow_html=True)

        # Concrete
        st.markdown(f"""
        <div class="checklist-row">
            <div>
                <strong style="color: #F8FAFC;">🏗️ Ready-Mix Concrete M35/M40 (m³)</strong>
                <div style="font-size: 0.8rem; color: #94A3B8;">
                    Total Volume: <strong>{int(m['concrete_total_cum']):,} m³</strong> | Poured: <span style="color:#F59E0B;">{int(m['concrete_poured_cum']):,} m³</span>
                </div>
            </div>
            <span class="pill pill-warning">{int(completion_pct)}% Poured</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### 📍 Milestone Progress Stages")
        st.progress(completion_pct / 100.0)
        
        # Stage indicator pill
        current_stage = "Substructure & Foundation"
        if completion_pct > 85:
            current_stage = "Finishing, Snagging & Occupancy Handover"
        elif completion_pct > 65:
            current_stage = "MEP Services, Masonry & Internal Plastering"
        elif completion_pct > 35:
            current_stage = "RCC Superstructure Casting (Floors G+12 to G+24)"
        elif completion_pct > 15:
            current_stage = "Plinth Beam, Retaining Walls & Podium Slabs"
            
        st.markdown(f"**Current Milestone:** <span class='pill pill-info'>{current_stage}</span>", unsafe_allow_html=True)

    with col_chart:
        st.markdown("#### 🥧 Expenditure Distribution")
        st.plotly_chart(render_cost_breakdown_pie(m['total_budget']), use_container_width=True)

    st.markdown("---")

    # Conceptual 3D Architectural Rendering via Pollinations AI
    st.markdown("#### 🎨 Conceptual 3D Architectural Vision Generator (Pollinations AI)")
    st.caption("AI-synthesized parametric exterior elevations and 3D architectural renders matching your typology & city skyline.")

    r_col1, r_col2 = st.columns([1, 1], gap="medium")
    with r_col1:
        arch_style = st.selectbox(
            "Architectural Design Style:",
            [
                "Biophilic Glass Facade with Vertical Gardens",
                "Ultra-Modern Sleek Curtain Wall Tower with Cantilever Balconies",
                "Sustainable Brutalist Reinforced Concrete & Timber Accents",
                "Futuristic Parametric Aerodynamic Geometry",
                "High-End Tropical Modern Luxury Villa Compound"
            ]
        )

        lighting_mood = st.selectbox(
            "Lighting & Atmosphere:",
            [
                "Dramatic Golden Hour Sunset with warm interior illumination",
                "Crisp Architectural Daylight with clear blue sky",
                "Cyberpunk Dusk with neon accent lighting and reflections",
                "Misty Morning Atmospheric fog"
            ]
        )

        render_btn = st.button("✨ Synthesize 3D Architectural Render", use_container_width=True)

    # Generate Image URL
    prompt_raw = (
        f"Professional architectural 3D visualization of {structure_type}, "
        f"{arch_style}, {lighting_mood}, hyper-realistic 8k octane render, "
        f"photorealistic civil engineering masterpiece, architectural digest feature"
    )
    encoded_prompt = urllib.parse.quote(prompt_raw)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=640&nologo=true&seed=42"

    with r_col2:
        if render_btn or "pollinations_active" not in st.session_state:
            st.session_state["pollinations_active"] = True
            st.session_state["current_render_url"] = image_url

        if "current_render_url" in st.session_state:
            st.image(
                st.session_state["current_render_url"],
                caption=f"Conceptual 3D Visualization: {structure_type} ({arch_style})",
                use_container_width=True
            )
            st.caption(f"🔗 **Pollinations Engine Prompt:** `{prompt_raw[:120]}...`")
