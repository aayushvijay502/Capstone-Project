"""
Custom styling module for Multimodal Construction Intelligence Platform.
Provides rich industrial-grade aesthetics, glassmorphism, responsive metric cards,
and glowing status pills.
"""

def get_custom_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* Global Typography & Font Overrides */
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    code, pre, .mono-font {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 95% !important;
    }

    /* Hero Banner Header */
    .hero-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 50%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 16px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), 0 0 20px rgba(245, 158, 11, 0.08);
        position: relative;
        overflow: hidden;
    }

    .hero-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #F59E0B, #EF4444);
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #F59E0B 0%, #FBBF24 50%, #38BDF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.35rem;
    }

    .hero-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        font-weight: 400;
        margin: 0;
    }

    .hero-meta-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(245, 158, 11, 0.12);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: #FBBF24;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Glassmorphism Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.25s ease-in-out;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
    }

    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(245, 158, 11, 0.4);
        box-shadow: 0 8px 25px -4px rgba(245, 158, 11, 0.15);
    }

    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: -0.02em;
        line-height: 1.1;
        margin-top: 4px;
    }

    .metric-label {
        font-size: 0.8rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 500;
    }

    /* Status Pills */
    .pill {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-align: center;
    }

    .pill-compliant {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10B981;
        color: #34D399;
    }

    .pill-warning {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid #F59E0B;
        color: #FBBF24;
    }

    .pill-danger {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid #EF4444;
        color: #F87171;
    }

    .pill-info {
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid #38BDF8;
        color: #38BDF8;
    }

    /* Severity Badges */
    .sev-critical {
        background: rgba(239, 68, 68, 0.2);
        color: #FCA5A5;
        border: 1px solid #EF4444;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .sev-high {
        background: rgba(249, 115, 22, 0.2);
        color: #FDBA74;
        border: 1px solid #F97316;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .sev-medium {
        background: rgba(234, 179, 8, 0.2);
        color: #FDE047;
        border: 1px solid #EAB308;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .sev-low {
        background: rgba(59, 130, 246, 0.2);
        color: #93C5FD;
        border: 1px solid #3B82F6;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    /* Content Card Container */
    .content-box {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
        backdrop-filter: blur(8px);
    }

    .content-box-amber {
        border-left: 4px solid #F59E0B;
    }
    
    .content-box-blue {
        border-left: 4px solid #38BDF8;
    }

    .content-box-emerald {
        border-left: 4px solid #10B981;
    }

    .content-box-red {
        border-left: 4px solid #EF4444;
    }

    /* Tab Styling Overrides */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 8px 12px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        color: #94A3B8;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.15) 100%) !important;
        color: #FBBF24 !important;
        border-bottom: 2px solid #F59E0B !important;
    }

    /* Sidebar Aesthetic */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    .sidebar-brand-box {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-radius: 12px;
        padding: 1.1rem;
        margin-bottom: 1.2rem;
        text-align: center;
    }

    /* Checklist row */
    .checklist-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 12px;
        margin-bottom: 6px;
        border-radius: 8px;
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.04);
    }

    /* Weather Alert Banner */
    .weather-banner {
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-left: 5px solid;
    }
    
    .weather-extreme {
        background: rgba(239, 68, 68, 0.12);
        border-color: #EF4444;
        color: #FCA5A5;
    }
    
    .weather-warning {
        background: rgba(245, 158, 11, 0.12);
        border-color: #F59E0B;
        color: #FDE68A;
    }

    .weather-normal {
        background: rgba(16, 185, 129, 0.12);
        border-color: #10B981;
        color: #A7F3D0;
    }

    /* Chat message container */
    .chat-bubble-user {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px 12px 0 12px;
        padding: 10px 14px;
        margin: 6px 0;
        max-width: 85%;
        margin-left: auto;
        color: #F8FAFC;
    }

    .chat-bubble-bot {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-radius: 12px 12px 12px 0;
        padding: 12px 16px;
        margin: 6px 0;
        max-width: 90%;
        color: #E2E8F0;
    }
    </style>
    """
