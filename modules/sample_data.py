"""
Sample datasets and synthetic benchmark images for Multimodal Construction Intelligence Platform.
Enables immediate 1-click testing with zero external image requirements.
"""

from PIL import Image, ImageDraw, ImageFont
import io

def generate_sample_ppe_image() -> Image.Image:
    """Generate a realistic synthetic construction site scene with workers for testing."""
    img = Image.new("RGB", (700, 480), color=(30, 41, 59))
    draw = ImageDraw.Draw(img)
    
    # Draw sky / upper site background
    draw.rectangle([0, 0, 700, 160], fill=(71, 85, 105))
    
    # Draw concrete slab / floor
    draw.rectangle([0, 320, 700, 480], fill=(100, 116, 139))
    
    # Draw steel reinforcement rebar columns
    for x in [120, 340, 560]:
        draw.rectangle([x, 100, x + 25, 340], fill=(148, 163, 184))
        # cross ties
        for y in range(110, 330, 20):
            draw.line([x - 5, y, x + 30, y], fill=(203, 213, 225), width=3)
            
    # Draw scaffolding pipes
    draw.line([60, 60, 60, 380], fill=(245, 158, 11), width=4)
    draw.line([220, 60, 220, 380], fill=(245, 158, 11), width=4)
    draw.line([60, 160, 220, 160], fill=(245, 158, 11), width=3)
    draw.line([60, 260, 220, 260], fill=(245, 158, 11), width=3)
    draw.line([60, 160, 220, 260], fill=(234, 179, 8), width=2)
    
    # Worker 1: Fully Compliant Worker (Left)
    # Hardhat (Yellow)
    draw.ellipse([140, 220, 165, 238], fill=(250, 204, 21))
    # Head
    draw.ellipse([144, 230, 161, 248], fill=(225, 175, 140))
    # High-vis Vest (Neon Orange/Yellow with reflective stripes)
    draw.rectangle([138, 248, 167, 290], fill=(249, 115, 22))
    draw.line([143, 255, 143, 290], fill=(241, 245, 249), width=3)
    draw.line([162, 255, 162, 290], fill=(241, 245, 249), width=3)
    # Trousers
    draw.rectangle([140, 290, 165, 340], fill=(30, 58, 138))
    # Steel-toe boots (Dark Brown/Black)
    draw.rectangle([136, 340, 150, 348], fill=(15, 23, 42))
    draw.rectangle([155, 340, 169, 348], fill=(15, 23, 42))
    
    # Worker 2: High-Risk Worker (Right) - Missing Helmet & Missing Harness near edge!
    # Head without helmet (Brown hair)
    draw.ellipse([465, 225, 485, 245], fill=(120, 53, 15))
    # Regular casual clothes (Red shirt, no high-vis vest)
    draw.rectangle([460, 245, 490, 290], fill=(185, 28, 28))
    # Jeans
    draw.rectangle([462, 290, 488, 340], fill=(71, 85, 105))
    # Sneakers (non-steel toe)
    draw.rectangle([458, 340, 472, 348], fill=(255, 255, 255))
    draw.rectangle([478, 340, 492, 348], fill=(255, 255, 255))
    
    # Unprotected Floor Edge Danger Zone
    draw.line([440, 345, 680, 345], fill=(239, 68, 68), width=3)
    draw.text((30, 20), "SIMULATED SITE AUDIT CAPTURE: ZONE 4B - HIGH-RISE CORE", fill=(245, 158, 11))
    draw.text((30, 40), "Standards Reference: OSHA 1926.28 / IS 456:2000 Cl 41", fill=(148, 163, 184))
    draw.text((120, 360), "[Worker A: Compliant]", fill=(34, 197, 94))
    draw.text((430, 360), "[Worker B: VIOLATIONS]", fill=(239, 68, 68))
    
    return img


def generate_sample_crack_image() -> Image.Image:
    """Generate a realistic synthetic concrete crack image for diagnostics testing."""
    img = Image.new("RGB", (700, 480), color=(148, 163, 184))
    draw = ImageDraw.Draw(img)
    
    # Concrete texture simulation (grid lines and shading)
    for y in range(0, 480, 40):
        draw.line([0, y, 700, y], fill=(100, 116, 139), width=1)
    for x in range(0, 700, 40):
        draw.line([x, 0, x, 480], fill=(100, 116, 139), width=1)
        
    # Formwork joint
    draw.line([350, 0, 350, 480], fill=(71, 85, 105), width=3)
    
    # Draw significant diagonal shear crack (45 degree shear pattern across beam-column joint)
    crack_points = [
        (150, 80), (180, 110), (220, 140), (250, 180), (290, 210),
        (330, 245), (380, 290), (430, 320), (480, 370), (520, 410), (560, 440)
    ]
    
    # Deep fracture core
    for i in range(len(crack_points) - 1):
        p1 = crack_points[i]
        p2 = crack_points[i+1]
        draw.line([p1, p2], fill=(15, 23, 42), width=5)
        # branching secondary micro-cracks
        draw.line([p1[0], p1[1], p1[0] + 15, p1[1] - 8], fill=(30, 41, 59), width=2)
        draw.line([p2[0], p2[1], p2[0] - 12, p2[1] + 10], fill=(51, 65, 85), width=2)
        
    # Spalling zone
    draw.polygon([(360, 260), (410, 270), (430, 310), (390, 320), (350, 290)], fill=(71, 85, 105))
    draw.text((370, 280), "SPALL", fill=(239, 68, 68))
    
    # Annotation overlay
    draw.text((25, 25), "SAMPLE SCAN: REINFORCED CONCRETE BEAM-COLUMN JUNCTION", fill=(15, 23, 42))
    draw.text((25, 45), "Estimated Surface Width: ~2.8 mm | Angle: ~45 deg (Principal Tension)", fill=(185, 28, 28))
    draw.text((25, 65), "Reference: IS 456 Cl 35.3.2 / ACI 224R Structural Shear", fill=(30, 58, 138))
    
    return img


SAMPLE_PPE_AUDIT_DATA = {
    "safety_score": 62,
    "overall_status": "Conditional Pass - Immediate Corrective Action Required",
    "standards_compliance": {
        "OSHA_1926_28": "Partial Non-Compliance",
        "IS_456_2000_Safety": "Deficiency Identified (Cl. 41 Edge Protection)"
    },
    "workers_detected": 2,
    "ppe_detection": [
        {"item": "Industrial Hardhats (IS 2925)", "detected_count": 1, "missing_count": 1, "status": "Violation"},
        {"item": "High-Visibility Safety Vests (EN ISO 20471)", "detected_count": 1, "missing_count": 1, "status": "Violation"},
        {"item": "Steel-Toe Safety Footwear (IS 15298)", "detected_count": 1, "missing_count": 1, "status": "Partial Concern"},
        {"item": "Fall Arrest Harness & Lanyard (IS 3521)", "detected_count": 0, "missing_count": 1, "status": "Critical Breach"},
        {"item": "Eye / Face Protection", "detected_count": 0, "missing_count": 2, "status": "Advisory"}
    ],
    "identified_hazards": [
        {
            "hazard": "Worker B Operating at Height Without Fall Arrest Harness",
            "severity": "Critical",
            "osha_reference": "OSHA 1926.501(b)(1) - Unprotected Sides & Edges > 6ft",
            "is_standard": "IS 3521 / National Building Code (NBC) Part 7",
            "immediate_remedy": "Halt work immediately. Evacuate worker from slab edge and rig double-locking full-body safety harness tied to certified static life line."
        },
        {
            "hazard": "Absence of Certified Hardhat & High-Vis Vest in Active Overhead Zone",
            "severity": "High",
            "osha_reference": "OSHA 1926.100 - Head Protection",
            "is_standard": "IS 2925:1984 Specification for Industrial Safety Helmets",
            "immediate_remedy": "Issue Type 1 Class E industrial helmet and retro-reflective vest before re-entry."
        },
        {
            "hazard": "Missing Perimeter Edge Guardrail / Toe-Board System",
            "severity": "High",
            "osha_reference": "OSHA 1926.502(b) - Guardrail Systems (42-inch top rail)",
            "is_standard": "IS 3696 Part 1 (Safety code for scaffolds and ladders)",
            "immediate_remedy": "Install two-tier perimeter steel guardrail (top rail at 1050 mm, mid-rail at 530 mm) and 150 mm toe-board."
        },
        {
            "hazard": "Unsecured Scaffolding Diagonal Bracing Joint",
            "severity": "Medium",
            "osha_reference": "OSHA 1926.451(c) - Scaffold Support & Plumbness",
            "is_standard": "IS 4014 Part 2",
            "immediate_remedy": "Torque all right-angle and swivel couplers to 54 Nm (40 lbf-ft) and inspect base plates."
        }
    ],
    "recommendations": [
        "Issue Stop-Work Notice on Zone 4B until edge guardrails are verified.",
        "Conduct mandatory 15-minute Morning Toolbox Talk on 100% Tie-Off protocols.",
        "Digitally log incident in site EHS Compliance register."
    ]
}


SAMPLE_CRACK_AUDIT_DATA = {
    "defect_classification": "Structural Shear Fracture",
    "defect_confidence": 0.94,
    "structural_element": "Reinforced Concrete Beam-Column Joint (Zone 2 Critical Shear)",
    "estimated_width_mm": 2.8,
    "width_tolerance_range": "2.5 mm - 3.1 mm",
    "crack_orientation": "Diagonal 45-degree angle pointing towards compressive column face",
    "severity_rating": "Critical",
    "structural_risk_index": 88,
    "root_causes": [
        "Diagonal principal tensile stress exceeding concrete tensile strength (0.7 * sqrt(fck))",
        "Insufficient shear reinforcement (transverse stirrup spacing exceeding d/2 as per IS 456 Cl 26.5.1.5)",
        "Differential settlement or dynamic load surge during recent floor casting"
    ],
    "secondary_defects": [
        "Surface concrete spalling (loss of cover zone ~40 mm)",
        "Early rebar oxidation exposure risk"
    ],
    "engineering_repair_specification": {
        "primary_protocol": "High-Pressure Structural Epoxy Resin Injection followed by CFRP Wrap",
        "epoxy_grade": "Low-viscosity high-modulus epoxy conforming to ASTM C881 Type I & IV Grade 1",
        "surface_preparation": "V-groove along crack line, clean with oil-free compressed air, seal with thixotropic epoxy putty, install brass/plastic injection ports at 150 mm c/c",
        "injection_pressure": "0.2 to 0.4 N/mm² (30-60 psi) until refusal and resin emerges from adjacent port",
        "structural_strengthening": "Apply 2-ply bidirectional Carbon Fiber Reinforced Polymer (CFRP) fabric wrap around beam joint to restore shear capacity",
        "urgency": "Immediate (Within 24 to 48 Hours) - Temporary propping of beam required immediately"
    },
    "relevant_codes": [
        "IS 456:2000 (Plain and Reinforced Concrete - Cl 35.3.2 Limit State of Serviceability)",
        "IS 13935:2020 (Repair and Seismic Strengthening of Buildings - Guidelines)",
        "ACI 224.1R-07 (Causes, Evaluation, and Repair of Cracks in Concrete Structures)"
    ]
}
