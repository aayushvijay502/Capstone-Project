# Multimodal Construction Intelligence Platform 🏗️
**Category:** Generative AI | Real Estate Decision Support  
**Platform ID:** `6ac4c98d1dcde6d7857c1642`  
**Skill Wallet Capstone Project 1 (Turnkey Implementation)**

---

## 📌 Executive Summary & Scope
The **Multimodal Construction Intelligence Platform** is an enterprise-grade AI decision-support system designed for civil contractors, structural engineering consultants, project management consultants (PMC), and real estate developers.

The platform processes high-resolution site photography to:
1. **Audit PPE Safety Compliance (Epic 2):** Autonomously detect worker safety violations under **OSHA 1926** and **IS 456 / IS 3521** standards, computing a quantitative Safety Score (0-100) and generating corrective directives.
2. **Classify Structural Concrete Cracks (Epic 2):** Detect and categorize surface defects into *Hairline*, *Settlement*, *Structural Shear*, *Thermal Expansion*, and *Spalling* with sub-millimeter width estimation and **IS 13935 / ACI 224.1R** repair protocols (epoxy injection, CFRP wrapping).
3. **Plan Budgets & Real Estate Valuation (Epic 3):** Forecast capital expenditure (CapEx), current WIP market asset valuation in INR (Lakhs / Crores), and calculate IS 456 material requirements (Steel MT & Cement Bags) with conceptual 3D architectural synthesis via Pollinations AI.
4. **Site Assistant & Weather Advisory (Epic 5):** Dispatch meteorological hazard protocols (tower crane wind cutoffs, IS 456 hot/cold weather concreting, electrical hazard isolation) and interact with an AI Senior Civil Engineering assistant.

---

## 🚀 Live Demo & Zero-Database Architecture
- **Self-Contained:** Zero external database dependencies (no Postgres, MongoDB, or Redis required). State is managed seamlessly in memory and session storage.
- **1-Click Deployment:** Ready for instant deployment on **Streamlit Community Cloud**, HuggingFace Spaces, or local container.
- **Graceful Demonstration Mode:** Includes built-in synthetic benchmark inspection datasets and full-fidelity offline analysis for reviewers evaluating without a live Gemini API key.

---

## 🛠️ Kanban Epics Coverage Matrix

| Epic | Module Name | Deliverables & Code Artifacts |
| :--- | :--- | :--- |
| **Epic 1** | Requirements & Environment | `.streamlit/config.toml`, `requirements.txt`, modular directory hierarchy |
| **Epic 2** | PPE Vision & Crack Diagnostics | `modules/safety_audit.py`, `modules/crack_diagnostics.py`, OSHA & IS 456 JSON contracts |
| **Epic 3** | Planning & Real Estate Valuation | `modules/valuation_planning.py`, INR currency models, Pollinations AI 3D rendering |
| **Epic 4** | Multimodal AI & JSON Contracts | `modules/gemini_client.py`, structured JSON parsing, strict schema validation |
| **Epic 5** | Site Chatbot & Weather Advisory | `modules/site_assistant.py`, meteorological dispatch engine, multi-turn civil assistant |
| **Epic 6** | Interface, Testing & Cloud Deployment | `app.py`, `modules/styles.py`, Streamlit Community Cloud readiness |

---

## 📋 Regulatory & Engineering Standards Implemented

- **OSHA 1926.28 & 1926.100:** Personal Protective Equipment and Head Protection in construction zones.
- **OSHA 1926.501 & 1926.502:** Fall protection, perimeter edge guardrails (42-inch top rail, 21-inch mid-rail, 4-inch toe-board).
- **OSHA 1926.1400 / IS 13367:** Tower crane and mobile crane high-wind operational cutoffs (>38 km/h) and free weathervaning.
- **IS 456:2000 (Indian Standard):** Code of Practice for Plain and Reinforced Concrete (Curing duration Cl. 13.5, hot/cold weather concreting Cl. 14, crack width limits Cl. 35.3.2).
- **IS 13935:2020:** Guidelines for Repair and Seismic Strengthening of Buildings.
- **IS 2925 / IS 3521 / IS 15298:** Specifications for industrial safety helmets, full-body harnesses, and protective footwear.
- **ACI 224.1R-07:** Causes, Evaluation, and Repair of Cracks in Concrete Structures (American Concrete Institute).

---

## 💻 Local Installation & Setup Guide

### 1. Prerequisites
- Python 3.9+ (Python 3.10, 3.11, 3.12, 3.13 supported)
- Git (optional)

### 2. Clone or Navigate to Directory
```bash
cd "c:/Users/HP/OneDrive/Dokumen/Desktop/Project/Multimodal Construction Intelligence Platform"
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch Application
```bash
python -m streamlit run app.py
```
Or directly:
```bash
streamlit run app.py
```

Access the web dashboard in your browser at `http://localhost:8501`.

---

## ☁️ Streamlit Community Cloud 1-Click Deployment

1. Push this repository to GitHub.
2. Log in to [share.streamlit.io](https://share.streamlit.io/).
3. Click **"New App"** and select:
   - **Repository:** `Your-Username/Multimodal-Construction-Intelligence-Platform`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. *(Optional)* Add your Google Gemini API Key in **Advanced Settings -> Secrets**:
   ```toml
   GEMINI_API_KEY = "AIzaSy..."
   ```
5. Click **Deploy!** The app will be live within 60 seconds with SSL and zero database requirements.

---

## 📦 JSON Data Contracts

### 1. Site Safety & PPE Audit Output Schema
```json
{
  "safety_score": 62,
  "overall_status": "Conditional Pass - Immediate Corrective Action Required",
  "standards_compliance": {
    "OSHA_1926_28": "Partial Non-Compliance",
    "IS_456_2000_Safety": "Deficiency Identified"
  },
  "workers_detected": 2,
  "ppe_detection": [
    {
      "item": "Industrial Hardhats (IS 2925)",
      "detected_count": 1,
      "missing_count": 1,
      "status": "Violation"
    }
  ],
  "identified_hazards": [
    {
      "hazard": "Worker B Operating at Height Without Fall Arrest Harness",
      "severity": "Critical",
      "osha_reference": "OSHA 1926.501(b)(1)",
      "is_standard": "IS 3521",
      "immediate_remedy": "Halt work immediately. Rig double-locking full-body safety harness tied to certified static lifeline."
    }
  ]
}
```

### 2. Crack Diagnostics Output Schema
```json
{
  "defect_classification": "Structural Shear Fracture",
  "defect_confidence": 0.94,
  "structural_element": "Reinforced Concrete Beam-Column Joint",
  "estimated_width_mm": 2.8,
  "severity_rating": "Critical",
  "structural_risk_index": 88,
  "root_causes": [
    "Diagonal principal tensile stress exceeding concrete tensile strength"
  ],
  "engineering_repair_specification": {
    "primary_protocol": "High-Pressure Structural Epoxy Resin Injection followed by CFRP Wrap",
    "epoxy_grade": "Low-viscosity high-modulus epoxy (ASTM C881 Type I & IV)",
    "injection_pressure": "0.2 to 0.4 N/mm² (30-60 psi)",
    "urgency": "Immediate (Within 24 to 48 Hours)"
  }
}
```

---

## 🔒 Security & Privacy
- API Keys entered through the UI are held exclusively in Streamlit session memory and are never written to disk or transmitted to external servers other than official Google AI endpoints.
- When Demonstration Mode is active, no network requests are sent outside the local environment.

---
*Developed for Skill Wallet Capstone Project 1 • Generative AI & Real Estate Decision Support*
