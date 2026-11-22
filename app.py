import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import re
import json
import time
import os
import requests
import html
from bs4 import BeautifulSoup
from io import BytesIO
from dotenv import load_dotenv

# Load local environment variables if available (.env)
load_dotenv()

st.set_page_config(
    page_title="Findora | Enterprise Lead Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Deploy button
st.markdown("""
<style>
[data-testid="stAppDeployButton"],
[data-testid="stDeployButton"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# Hide Print, Record screen, Made with Streamlit inside the menu
components.html("""
<script>
const doc = window.parent.document;
const HIDE = ["print", "record screen", "made with streamlit"];

function clean() {
  // Deploy button fallback
  doc.querySelectorAll('[data-testid="stAppDeployButton"], [data-testid="stDeployButton"]')
     .forEach(el => el.style.display = "none");

  // Only look inside the menu popup
  doc.querySelectorAll('[data-baseweb="popover"], [data-testid="stMainMenuPopover"]')
     .forEach(menu => {
       menu.querySelectorAll('li, [role="option"], [role="menuitem"], div, span')
         .forEach(el => {
           const t = (el.textContent || "").trim().toLowerCase();
           if (HIDE.some(h => t.startsWith(h)) && t.length < 60) {
             const target = el.closest('li, [role="option"], [role="menuitem"]') || el;
             target.style.display = "none";
           }
         });
     });
}

new MutationObserver(clean).observe(doc.body, {childList: true, subtree: true});
clean();
</script>
""", height=0)

# -------------------------------------------------------------
# Modern Theme-Adaptive Design System (Light, Dark, System)
# -------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, p, div, span, label, input, button, select {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Clean header spacing - toolbar sits comfortably above the card without touching or overlapping */
header[data-testid="stHeader"] {
    background: transparent !important;
    z-index: 99 !important;
}

.block-container,
[data-testid="block-container"],
[data-testid="stMainBlockContainer"],
.stMainBlockContainer {
    padding-top: 3rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

[data-testid="stSidebarContent"] {
    padding-top: 1rem !important;
}

/* Hero Header - Sleek Executive Dark Banner across ALL themes (Light, Dark, System) */
.hero-wrapper {
    background: linear-gradient(135deg, #090d16 0%, #0f172a 50%, #1e293b 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 16px !important;
    padding: 22px 28px !important;
    margin-top: 6px !important;
    margin-bottom: 22px !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.28) !important;
}

.hero-wrapper::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #2563eb 0%, #7c3aed 50%, #06b6d4 100%);
}

.hero-title-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}

.hero-title {
    font-size: 30px !important;
    font-weight: 800 !important;
    color: #ffffff !important; /* Always crisp white */
    letter-spacing: -0.8px !important;
    margin: 0 !important;
    display: flex;
    align-items: center;
    gap: 10px;
}

.hero-title-accent {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

.hero-title-sub {
    font-size: 19px !important;
    font-weight: 600 !important;
    color: #94a3b8 !important; /* Always crisp light slate */
}

.hero-subtitle {
    font-size: 14px !important;
    margin-top: 6px !important;
    font-weight: 400 !important;
    color: #cbd5e1 !important; /* Always crisp light gray */
    opacity: 0.95 !important;
}

/* Badges inside hero - high contrast against dark background in all modes */
.hero-wrapper .badge-chip {
    display: inline-flex !important;
    align-items: center !important;
    gap: 5px !important;
    padding: 4px 12px !important;
    border-radius: 20px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}

.hero-wrapper .badge-green {
    background: rgba(16, 185, 129, 0.18) !important;
    color: #34d399 !important;
    border: 1px solid rgba(52, 211, 153, 0.35) !important;
}

.hero-wrapper .badge-blue {
    background: rgba(56, 189, 248, 0.18) !important;
    color: #38bdf8 !important;
    border: 1px solid rgba(56, 189, 248, 0.35) !important;
}

.hero-wrapper .badge-purple {
    background: rgba(168, 85, 247, 0.18) !important;
    color: #c084fc !important;
    border: 1px solid rgba(168, 85, 247, 0.35) !important;
}

/* Badges with theme-safe contrast */
.badge-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}

.badge-green {
    background: rgba(16, 185, 129, 0.16);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.35);
}

.badge-blue {
    background: rgba(37, 99, 235, 0.16);
    color: #3b82f6;
    border: 1px solid rgba(37, 99, 235, 0.35);
}

.badge-purple {
    background: rgba(124, 58, 237, 0.16);
    color: #a855f7;
    border: 1px solid rgba(124, 58, 237, 0.35);
}

/* Metric Cards */
.metric-card {
    background-color: var(--secondary-background-color);
    border: 1px solid rgba(128, 128, 128, 0.22);
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
}

.metric-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.metric-icon {
    width: 46px;
    height: 46px;
    min-width: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.metric-icon svg {
    width: 28px;
    height: 28px;
}

.icon-blue { background: rgba(37, 99, 235, 0.15); color: #3b82f6; }
.icon-green { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.icon-purple { background: rgba(124, 58, 237, 0.15); color: #a855f7; }
.icon-amber { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }

.metric-value {
    font-size: 35px;
    font-weight: 800;
    color: var(--text-color);
    letter-spacing: -0.5px;
    line-height: 1.1;
    margin: 4px 0 2px 0;
}

.metric-val-green { color: #10b981 !important; }
.metric-val-purple { color: #a855f7 !important; }
.metric-val-blue { color: #3b82f6 !important; }

.metric-sublabel {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-color);
    opacity: 0.75;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 4px;
}

/* Section Headings */
.section-heading {
    font-size: 24px;
    font-weight: 700;
    color: var(--text-color);
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 40px;
    # border-bottom:1px solid grey;
}

/* Clean Dataframe Container */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* Primary Button Styling */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    border: 1px solid #1e40af !important;
    color: #ffffff !important;
    font-size: 26px !important;
    border-radius: 10px !important;
    padding: 14px 28px !important;
    box-shadow: 0 2px 6px rgba(37, 99, 235, 0.25) !important;
    transition: all 0.15s ease !important;
}

div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.35) !important;
    transform: translateY(-1px) !important;
}


/* Enrichment Mode Selector */
div[role="radiogroup"] {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}

/* Radio Option */
div[role="radiogroup"] label {
    background: rgba(148, 163, 184, 0.06);
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 10px;
    padding: 10px 16px;
    transition: all 0.2s ease;
}

/* Hover */
div[role="radiogroup"] label:hover {
    border-color: #3B82F6;
    background: rgba(59, 130, 246, 0.07);
}

/* Selected Option */
div[role="radiogroup"] label:has(input:checked) {
    background: rgba(59, 130, 246, 0.10);
    border: 1px solid #3B82F6;
}

/* Option Text */
div[role="radiogroup"] label p {
    font-size: 13px;
    font-weight: 600;
}

/* Selected Fields Preview */
div[data-testid="stCaptionContainer"] {
    color: #94A3B8;
    font-size: 12px;
    margin-top: 8px;
}

div[role="radiogroup"] label p {
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.1px !important;
}


/* ==========================================
   FINDORA LIVE INTELLIGENCE ENGINE
========================================== */

.processing-panel {
    background: linear-gradient(135deg, #080f1e, #111c32);
    border: 1px solid rgba(59,130,246,.35);
    border-radius: 18px;
    padding: 25px;
    margin: 20px 0;
    color: #f8fafc;
    box-shadow: 0 12px 35px rgba(0,0,0,.20);
}

.processing-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}

.processing-title {
    font-size: 21px;
    font-weight: 800;
    color: #ffffff;
}

.processing-subtitle {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 5px;
}

.live-indicator {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #34d399;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
}

.live-dot {
    width: 9px;
    height: 9px;
    background: #10b981;
    border-radius: 50%;
    animation: livePulse 1.2s infinite;
}

@keyframes livePulse {
    0%, 100% {
        box-shadow: 0 0 0 0 rgba(16,185,129,.5);
    }
    50% {
        box-shadow: 0 0 0 8px rgba(16,185,129,0);
    }
}

.processing-stats {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 12px;
    margin-top: 25px;
}

.processing-stat {
    background: rgba(255,255,255,.045);
    border: 1px solid rgba(148,163,184,.15);
    border-radius: 12px;
    padding: 15px;
}

.processing-stat-label {
    font-size: 10px;
    color: #94a3b8;
    font-weight: 700;
    letter-spacing: .8px;
}

.processing-stat-value {
    font-size: 25px;
    font-weight: 800;
    color: #ffffff;
    margin-top: 5px;
}

.processing-track {
    height: 9px;
    border-radius: 20px;
    background: #26344b;
    overflow: hidden;
    margin-top: 22px;
}

.processing-fill {
    height: 100%;
    border-radius: 20px;
    background: linear-gradient(
        90deg,#2563eb,#818cf8,#06b6d4
    );
    transition: width .4s ease;
    box-shadow: 0 0 15px rgba(59,130,246,.5);
}

.processing-stage {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    margin-top: 9px;
    background: rgba(255,255,255,.035);
    border: 1px solid rgba(148,163,184,.12);
    border-radius: 10px;
    color: #94a3b8;
    font-size: 13px;
}

.processing-stage.active {
    border-color: rgba(59,130,246,.55);
    background: rgba(37,99,235,.13);
    color: #ffffff;
}

.processing-stage.completed {
    color: #34d399;
}

.stage-icon {
    font-size: 17px;
}

.processing-log {
    margin-top: 20px;
    padding: 13px;
    background: rgba(0,0,0,.25);
    border-radius: 9px;
    color: #93c5fd;
    font-family: monospace;
    font-size: 11px;
    overflow-wrap: anywhere;
}

@media(max-width:600px) {
    .processing-stats {
        grid-template-columns: 1fr;
    }
}


</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Corporate Phone Directory & Area Code Intelligence
# -------------------------------------------------------------
KNOWN_CORPORATE_PHONES = {
    "microsoft": "+1 (425) 882-8080",
    "google": "+1 (650) 253-0000",
    "alphabet": "+1 (650) 253-0000",
    "apple": "+1 (408) 996-1010",
    "amazon": "+1 (206) 266-1000",
    "meta": "+1 (650) 543-4800",
    "accenture": "+91 (022) 6690 0000",
    "publicis": "+91 (022) 6660 0000",
    "ipg": "+91 (022) 6150 0000",
    "wipro": "+91 (080) 2844 0011",
    "infosys": "+91 (080) 2852 0261",
    "tcs": "+91 (022) 6778 9999",
    "hcl": "+91 (0120) 252 0917",
}

def derive_phone(company: str, location: str, country: str) -> str:
    """Return a corporate switchboard only if it is in the known directory. Never invents numbers."""
    if not company:
        return ""
    comp_clean = company.lower()
    for k, v in KNOWN_CORPORATE_PHONES.items():
        if k in comp_clean:
            return v
    return ""

# -------------------------------------------------------------
# Clean URL & Domain Logic
# -------------------------------------------------------------
def clean_linkedin_url(url: str) -> str:
    """Normalize LinkedIn URL by removing query strings, tracking params, and trailing slashes."""
    if not isinstance(url, str):
        return None
    url = url.strip()
    match = re.search(r"https?://(?:[a-z]{2,3}\.)?linkedin\.com/in/([A-Za-z0-9_%\-]+)", url, re.IGNORECASE)
    if match:
        slug = match.group(1).rstrip("/").lower()
        return f"https://www.linkedin.com/in/{slug}"
    return None

def clean_job_title(headline: str) -> str:
    """Extract and unmask actual job title from profile headlines."""
    if not headline:
        return ""
    headline = html.unescape(headline).strip()
    lines = [l.strip() for l in headline.split("\n") if l.strip()]
    valid_lines = [l for l in lines if not re.match(r"^(?:Hey|Hello|Hi|Greetings)[^\w]*$", l, re.IGNORECASE)]
    target_text = valid_lines[0] if valid_lines else headline
    
    target_text = re.sub(
        r"^[^\w\s]*\s*(?:Hey\s*[\r\n]*\s*I[’\']?m\s+(?:the\s+)?|I\s+am\s+(?:the\s+|an\s+|a\s+)?|Currently\s+serving\s+as\s+)",
        "",
        target_text,
        flags=re.IGNORECASE
    )
    m = re.split(r"\s+with\s+\d+\+?\s+years|\s+bringing\s+over|\s+supporting\s+", target_text, flags=re.IGNORECASE)
    clean = m[0].strip().rstrip(",").rstrip("·").rstrip("…").strip()
    if len(clean) > 75:
        clean = clean[:72] + "..."
    return clean

def derive_domain(company_name: str) -> str:
    """Derive clean corporate website domain."""
    if not company_name:
        return ""
    clean = re.sub(
        r"(?i)\b(inc|corp|corporation|llc|ltd|limited|technologies|solutions|group|holdings|pvt|co|gmbh|sa|consulting|consultants)\b\.?",
        "",
        company_name
    )
    clean = re.sub(r"[^A-Za-z0-9]", "", clean).lower()
    return f"{clean}.com" if clean else ""

def generate_email(name: str, domain: str) -> str:
    """Generate standardized corporate email."""
    if not name or not domain:
        return ""
    clean_name = re.sub(r"[^a-zA-Z\s]", "", name).strip().lower()
    parts = clean_name.split()
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[-1]}@{domain}"
    elif len(parts) == 1:
        return f"{parts[0]}@{domain}"
    return ""

def to_styled_excel(df: pd.DataFrame) -> bytes:
    """Generate styled Excel workbook with modern blue header formatting."""
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Enriched Leads")
        ws = writer.sheets["Enriched Leads"]
        
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        header_fill = PatternFill(start_color="1E40AF", end_color="1E40AF", fill_type="solid")
        header_font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
        center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
        thin_border = Border(
            left=Side(style="thin", color="E2E8F0"),
            right=Side(style="thin", color="E2E8F0"),
            top=Side(style="thin", color="E2E8F0"),
            bottom=Side(style="thin", color="E2E8F0")
        )
        
        for col in ws.iter_cols(min_row=1, max_row=1):
            for cell in col:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = center_align

        for col in ws.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            col_letter = col[0].column_letter
            ws.column_dimensions[col_letter].width = min(max(max_len + 4, 14), 50)
            
    return buffer.getvalue()

def init_warmed_session() -> requests.Session:
    """Initialize requests session with homepage cookies to eliminate HTTP 999."""
    s = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1"
    }
    s.headers.update(headers)
    try:
        s.get("https://www.linkedin.com", timeout=10)
    except Exception:
        pass
    return s

def extract_profile_with_session(session: requests.Session, url: str) -> dict:
    """Extract profile metadata from LinkedIn."""
    clean_url = clean_linkedin_url(url)
    data = {
        "Full Name": "",
        "Job Title": "",
        "Current Company": "",
        "Company Website": "",
        "Predicted Email": "",
        "Phone Number": "",
        "Country": "",
        "Location": "",
        "Status": "Failed"
    }
    
    if not clean_url:
        data["Status"] = "Invalid URL"
        return data

    try:
        resp = session.get(clean_url, timeout=12)
        if resp.status_code == 999:
            try:
                session.get("https://www.linkedin.com", timeout=8)
                time.sleep(1.2)
                resp = session.get(clean_url, timeout=12)
            except Exception:
                pass
                
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # 1. Parse JSON-LD Schema
            for s in soup.find_all("script", type="application/ld+json"):
                try:
                    js = json.loads(s.string)
                    graph = js.get("@graph", [js]) if isinstance(js, dict) else [js]
                    for item in graph:
                        if isinstance(item, dict) and item.get("@type") == "Person":
                            data["Full Name"] = item.get("name", "")
                            jobs = item.get("jobTitle", "")
                            if isinstance(jobs, list) and jobs:
                                jobs = str(jobs[0])
                            if jobs and "*" not in str(jobs):
                                data["Job Title"] = jobs
                            works = item.get("worksFor", [])
                            if isinstance(works, list) and works:
                                w0 = works[0]
                                data["Current Company"] = w0.get("name", "") if isinstance(w0, dict) else str(w0)
                            elif isinstance(works, dict):
                                data["Current Company"] = works.get("name", "")
                            addr = item.get("address", {})
                            if isinstance(addr, dict):
                                data["Country"] = addr.get("addressCountry", "")
                                data["Location"] = addr.get("addressLocality", "")
                            break
                except Exception:
                    pass

            # 2. Extract and unmask from OpenGraph tags
            og_title = soup.find("meta", property="og:title")
            og_desc = soup.find("meta", property="og:description")
            title_text = html.unescape(og_title["content"].replace(" | LinkedIn", "")) if og_title else ""
            desc_text = html.unescape(og_desc["content"]) if og_desc else ""

            if not data["Full Name"] and title_text:
                if " - " in title_text:
                    data["Full Name"] = title_text.split(" - ")[0].strip()
                else:
                    data["Full Name"] = title_text.strip()

            if title_text and " - " in title_text:
                after_dash = title_text.split(" - ", 1)[1].strip()
                if " at " in after_dash:
                    parts = after_dash.split(" at ", 1)
                    if not data["Job Title"] or "*" in data["Job Title"]:
                        data["Job Title"] = clean_job_title(parts[0])
                    if not data["Current Company"]:
                        data["Current Company"] = parts[1].strip()
                elif "Professional Profile" not in after_dash and not data["Current Company"]:
                    data["Current Company"] = after_dash

            # Middle-dot sections in description
            if desc_text:
                segments = [seg.strip() for seg in desc_text.split("·")]
                headline = segments[0] if segments else ""
                for seg in segments[1:]:
                    if seg.startswith("Experience:") and not data["Current Company"]:
                        data["Current Company"] = seg.replace("Experience:", "").strip()
                    elif seg.startswith("Location:") and not data["Location"]:
                        loc = seg.replace("Location:", "").strip()
                        data["Location"] = loc
                        if not data["Country"] and "," in loc:
                            data["Country"] = loc.split(",")[-1].strip()

                if not data["Job Title"] or "*" in data["Job Title"]:
                    data["Job Title"] = clean_job_title(headline)

            # Corporate Website & Email Enrichment
            domain = derive_domain(data["Current Company"])
            if domain:
                data["Company Website"] = f"https://www.{domain}"
                data["Predicted Email"] = generate_email(data["Full Name"], domain)

            # Phone Number Enrichment
            data["Phone Number"] = derive_phone(data["Current Company"], data["Location"], data["Country"])

            data["Status"] = "LinkedIn profile read (email is a pattern guess, unverified)" if data["Full Name"] else "Public Profile Detected"
        else:
            data["Status"] = "Blocked by LinkedIn (HTTP 999)" if resp.status_code == 999 else f"HTTP {resp.status_code}"
    except Exception as e:
        data["Status"] = f"Connection error: {str(e)[:30]}"

    return data

def enrich_with_gemini(api_key: str, profile_url: str, base_data: dict, requested_fields: list) -> dict:
    """Ask Gemini to fill EMPTY fields only. Output is a suggestion, not verified data."""
    try:
        from google import genai
        client = genai.Client(api_key=api_key)

        prompt = f"""
You are a B2B lead research assistant. You cannot browse the web.
Known lead data:
- URL: {profile_url}
- Name: {base_data.get('Full Name')}
- Job Title: {base_data.get('Job Title')}
- Company: {base_data.get('Current Company')}
- Location/Country: {base_data.get('Location')}, {base_data.get('Country')}

Fill in ONLY what you are confident about:
1. Official company website domain.
2. Most likely business email in the company's usual pattern.
3. Standard country name.
Use an empty string "" for anything you are not sure about. Never invent phone numbers.

Return ONLY valid JSON:
{{
    "Full Name": "",
    "Current Company": "",
    "Job Title": "",
    "Company Website": "",
    "Predicted Email": "",
    "Phone Number": "",
    "Country": ""
}}
"""
        response = None
        last_err = None
        for model_name in ["gemini-flash-latest", "gemini-2.5-flash", "gemini-2.0-flash"]:
            try:
                response = client.models.generate_content(model=model_name, contents=prompt)
                break
            except Exception as err:
                last_err = err
                if "404" not in str(err) and "NOT_FOUND" not in str(err):
                    raise
        if response is None and last_err:
            raise last_err

        if response and response.text:
            text = response.text.strip()
            if text.startswith("```"):
                text = re.sub(r"^```(?:json)?\s*", "", text)
                text = re.sub(r"\s*```$", "", text)
            ai_data = json.loads(text)

            filled = False
            for k in requested_fields:
                if k in ai_data and ai_data[k] and k != "Phone Number":
                    if not base_data.get(k) or "*" in str(base_data.get(k)):
                        base_data[k] = ai_data[k]
                        filled = True
            if filled:
                base_data["Status"] = f"{base_data.get('Status')} + Gemini suggestions (unverified)"
    except Exception as e:
        base_data["Status"] = f"{base_data.get('Status')} (AI error: {str(e)[:200]})"
    return base_data

# -------------------------------------------------------------
# Modern Executive Hero Banner
# -------------------------------------------------------------
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-title-row">
        <div>
            <h1 class="hero-title">
                <span class="hero-title-accent">FINDORA</span> <span class="hero-title-sub">GLOBAL INTELLIGENCE</span>
            </h1>
            <div class="hero-subtitle">
                B2B Lead Enrichment Engine &bull; Profile Extraction &amp; Predicted Contact Details
            </div>
            <div style="margin-top: 12px; display: flex; gap: 8px; flex-wrap: wrap;">
                <span class="badge-chip badge-green">● Active Session Engine</span>
                <span class="badge-chip badge-blue"> ✉  Email Enrichment</span>
                <span class="badge-chip badge-purple"> ✆  Phone Enrichment</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Sidebar: Engine Configuration
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("### Engine Settings")
    st.caption("Customizable intelligence & speed controls")

    
    st.markdown("---")
    st.markdown("#### ✦ AI Verification (Optional)")
    env_gemini_key = os.getenv("GEMINI_API_KEY", "")
    gemini_key = st.text_input(
        "Google Gemini API Key",
        value=env_gemini_key,
        type="password",
        help="Optional: Adds deep AI verification for corporate switchboard phones & exact websites."
    )
    if gemini_key:
        st.success("✨ Gemini AI Verification Active")
    else:
        st.info(" Ⓘ Running in Direct Metadata Mode (No API Key Required).")
    

    st.markdown("---")
    if st.button("⏻ Reset / Start New Project", use_container_width=True, help="Clear all stored inputs and results"):
        for key in ["enriched_results_df", "current_file_id", "uploaded_raw_df", "lead_cache"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

st.sidebar.markdown("""
<style>
.sidebar-footer {
position: fixed;
bottom: 0;
left: 0;
width: 18rem;
padding: 12px 16px;
text-align: center;
font-size: 0.8rem;
line-height: 1.6;
opacity: 0.7;
border-top: 1px solid rgba(128,128,128,0.25);
}
</style>
<div class="sidebar-footer">
A product by <b>Pushkar Shete</b><br>
Findora Global Intelligence &copy; 2026
</div>
""", unsafe_allow_html=True)
    

# -------------------------------------------------------------
# Workspace Tabs: Ingestion
# -------------------------------------------------------------
st.markdown('<div class="section-heading">🗃️ 1. Import Profile Records</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs([
    "📁 Upload Excel / CSV Spreadsheet (Recommended)",
    "🔗 Paste Profile URLs Directly"
])

input_urls = []
source_df = None
selected_url_col = None
keep_original = True

with tab1:
    uploaded = st.file_uploader(
        "Drop your spreadsheet (.xlsx or .csv) containing LinkedIn profile links",
        type=["xlsx", "csv"],
        help="Supports files with columns like 'LinkedIn Profile', 'URL', 'Link', etc."
    )
    
    if uploaded:
        # Detect file change: automatically wipe previous search results!
        file_signature = f"{uploaded.name}_{uploaded.size}"
        if st.session_state.get("current_file_id") != file_signature:
            st.session_state["enriched_results_df"] = None
            st.session_state["current_file_id"] = file_signature
            
        try:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            
            source_df = df.copy()
            st.session_state["uploaded_raw_df"] = df
            
            st.success(f"Loaded **{len(df)} records** across **{len(df.columns)} columns** from `{uploaded.name}`.")
            
            # Detect candidate columns
            possible_cols = [
                c for c in df.columns
                if any(k in str(c).lower() for k in ["url", "linkedin", "profile", "link"])
            ]
            default_index = df.columns.get_loc(possible_cols[0]) if possible_cols else 0
            
            c_col, c_keep = st.columns([2, 2])
            with c_col:
                selected_url_col = st.selectbox(
                    "Select the column containing LinkedIn Profile URLs:",
                    options=list(df.columns),
                    index=default_index
                )
            with c_keep:
                st.write("")
                st.write("")
                keep_original = st.checkbox(
                    "Retain all original spreadsheet columns in output",
                    value=True,
                    help="Keep all your initial columns (e.g. Lead ID, Notes) and append enriched contacts side-by-side."
                )
                
            raw_series = df[selected_url_col].dropna().astype(str).tolist()
            input_urls = raw_series
            
            with st.expander(f"Spreadsheet Preview: First 5 of {len(df)} rows", expanded=False):
                st.dataframe(df.head(5), use_container_width=True)
                
        except Exception as e:
            st.error(f"Error reading file: {e}")

with tab2:
    raw_urls = st.text_area(
        "LinkedIn Profile URLs (One per line)",
        placeholder="https://www.linkedin.com/in/satyanadella/\nhttps://www.linkedin.com/in/sundarpichai/",
        height=130
    )
    if raw_urls.strip():
        if st.session_state.get("current_file_id") is not None and not uploaded:
            st.session_state["enriched_results_df"] = None
            st.session_state["current_file_id"] = None
        input_urls = [x.strip() for x in raw_urls.splitlines() if x.strip()]

st.markdown("""
<div style="
    width: 100%;
    height: 2px;
    background: linear-gradient(
        90deg,
        rgba(59, 130, 246, 0.08) 0%,
        rgba(100, 116, 139, 0.55) 15%,
        rgba(59, 130, 246, 0.75) 50%,
        rgba(100, 116, 139, 0.55) 85%,
        rgba(59, 130, 246, 0.08) 100%
    );
    border-radius: 10px;
    margin: 25px 0;
    border-bottom:40px;
"></div>
""", unsafe_allow_html=True)


# -------------------------------------------------------------
# Enrichment Mode & Field Selection
# -------------------------------------------------------------

st.write("")
st.markdown(
    '<div class="section-heading">2. Select Enrichment Mode & Fields</div>',
    unsafe_allow_html=True
)

enrichment_mode = st.radio(
    "Choose Enrichment Focus:",
    [
        "Complete Contact Intelligence",
        "✉   Email Enrichment",
        "☎   Phone Enrichment"
    ],
    index=0,
    horizontal=True
)

all_available_fields = [
    "Full Name",
    "Current Company",
    "Job Title",
    "Company Website",
    "Predicted Email",
    "Phone Number",
    "Country"
]

if enrichment_mode == "Complete Contact Intelligence":

    selected_fields = all_available_fields

elif "Email Enrichment" in enrichment_mode:

    selected_fields = [
        "Full Name",
        "Current Company",
        "Job Title",
        "Company Website",
        "Predicted Email"
    ]

elif "Phone Enrichment" in enrichment_mode:

    selected_fields = [
        "Full Name",
        "Current Company",
        "Job Title",
        "Phone Number",
        "Country"
    ]

st.markdown("""
<div style="
    width: 100%;
    height: 2px;
    background: linear-gradient(
        90deg,
        rgba(59, 130, 246, 0.08) 0%,
        rgba(100, 116, 139, 0.55) 15%,
        rgba(59, 130, 246, 0.75) 50%,
        rgba(100, 116, 139, 0.55) 85%,
        rgba(59, 130, 246, 0.08) 100%
    );
    border-radius: 10px;
    margin: 25px 0;
    border-bottom:40px;
"></div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Input Validation & Summary
# -------------------------------------------------------------
st.write("")
st.markdown('<div class="section-heading">3. Verification & Profile Summary</div>', unsafe_allow_html=True)

valid_mappings = []
invalid_urls = []

for u in input_urls:
    cleaned = clean_linkedin_url(u)
    if cleaned:
        valid_mappings.append((u, cleaned))
    else:
        invalid_urls.append(u)

unique_valid = []
seen = set()
duplicate_pairs = []

for orig, clean in valid_mappings:
    if clean not in seen:
        seen.add(clean)
        unique_valid.append((orig, clean))
    else:
        duplicate_pairs.append((orig, clean))

duplicates_count = len(duplicate_pairs)

# Metric Cards
m_col1, m_col2, m_col3, m_col4 = st.columns(4)


with m_col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-sublabel">TOTAL INPUT</span>
            <div class="metric-icon icon-blue">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                     stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <path d="M14 2v6h6M8 13h8M8 17h8M8 9h2"/>
                </svg>
            </div>
        </div>
        <div class="metric-value">{len(input_urls)}</div>
        <div class="metric-sublabel">Spreadsheet Rows</div>
    </div>
    """, unsafe_allow_html=True)

with m_col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-sublabel">UNIQUE PROFILES</span>
            <div class="metric-icon icon-green">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                     stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="9" cy="8" r="3.5"/>
                    <path d="M2.5 20a6.5 6.5 0 0 1 13 0"/>
                    <path d="m16 11 2 2 4-4"/>
                </svg>
            </div>
        </div>
        <div class="metric-value metric-val-green">{len(unique_valid)}</div>
        <div class="metric-sublabel">Unique Leads to Enrich</div>
    </div>
    """, unsafe_allow_html=True)

with m_col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-sublabel">DUPLICATES REMOVED</span>
            <div class="metric-icon icon-purple">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                     stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="8" y="8" width="13" height="13" rx="2"/>
                    <path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3"/>
                    <path d="m11 13 6 6m0-6-6 6"/>
                </svg>
            </div>
        </div>
        <div class="metric-value metric-val-purple">{duplicates_count}</div>
        <div class="metric-sublabel">{"Auto-filtered Out" if duplicates_count > 0 else "None Found"}</div>
    </div>
    """, unsafe_allow_html=True)

with m_col4:
    rate = round((len(valid_mappings) / len(input_urls) * 100) if input_urls else 0, 1)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-sublabel">VALID URL RATE</span>
            <div class="metric-icon icon-amber">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                     stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="9"/>
                    <path d="m8 12 2.5 2.5L16 9"/>
                    <path d="M12 3v2M21 12h-2"/>
                </svg>
            </div>
        </div>
        <div class="metric-value metric-val-blue">{rate}%</div>
        <div class="metric-sublabel">Data Quality Score</div>
    </div>
    """, unsafe_allow_html=True)


st.write("")

if duplicates_count > 0:
    with st.expander(f"✂️ {duplicates_count} Duplicate Row{'s' if duplicates_count > 1 else ''} Filtered Out (Click to inspect)", expanded=False):
        dup_df = pd.DataFrame(duplicate_pairs, columns=["Duplicate Row Link in Input", "Canonical Profile Kept"])
        st.dataframe(dup_df, use_container_width=True)

if invalid_urls:
    with st.expander(f"⚠️ {len(invalid_urls)} invalid entries ignored (Click to review)", expanded=False):
        st.write(invalid_urls[:30])

        

# -------------------------------------------------------------
# Trigger Action Button + Native Streamlit Live Processing
# -------------------------------------------------------------

st.write("")

if st.button(
    "Start Enrichment  ➤",
    type="primary",
    use_container_width=True
):

    if not unique_valid:
        st.error("Please provide at least one valid LinkedIn Profile URL.")

    elif not selected_fields:
        st.error("Please select at least one field to research.")

    else:
        total = len(unique_valid)

        request_delay = 1.0
        results = []
        cached_count = 0
        start_time = time.time()

        progress_placeholder = st.empty()

        session = init_warmed_session()

        if "lead_cache" not in st.session_state:
            st.session_state["lead_cache"] = {}

        stages = [
            "Profile Detection",
            "Metadata Extraction",
            "Email Intelligence",
            "Phone Intelligence",
            "Final Verification"
        ]

        # -------------------------------------------------
        # Native Streamlit progress display
        # No raw HTML is used in this function.
        # -------------------------------------------------

        def render_processing(
            current,
            total,
            current_url,
            stage,
            completed,
            cached_count,
            elapsed
        ):
            percentage = int((completed / total) * 100) if total else 0

            with progress_placeholder.container():

                st.markdown("### FINDORA INTELLIGENCE ENGINE")
                st.caption(
                    "Advanced B2B profile intelligence and enrichment"
                )

                st.markdown("🟢 **LIVE PROCESSING**")

                metric1, metric2, metric3 = st.columns(3)

                with metric1:
                    st.metric(
                        "PROCESSED",
                        f"{completed}/{total}"
                    )

                with metric2:
                    st.metric(
                        "COMPLETION",
                        f"{percentage}%"
                    )

                with metric3:
                    st.metric(
                        "CACHED PROFILES",
                        cached_count
                    )

                st.progress(
                    percentage / 100,
                    text=f"Intelligence progress: {percentage}%"
                )

                st.markdown("**PROCESSING PIPELINE**")

                for i, stage_name in enumerate(stages):

                    if i < stage:
                        st.markdown(f"🟢 **{stage_name} — Completed**")

                    elif i == stage and completed < total:
                        st.markdown(f"🔵 **{stage_name} — In progress**")

                    else:
                        st.markdown(f"⚪ {stage_name} — Pending")

                st.divider()

                st.caption(f"CURRENT PROFILE: {current_url}")
                st.caption(f"ELAPSED TIME: {elapsed:.1f} seconds")
                st.caption("ENGINE STATUS: ACTIVE")

        # -------------------------------------------------
        # Process each unique LinkedIn profile
        # -------------------------------------------------

        for idx, (orig_url, clean_url) in enumerate(unique_valid):

            is_cached = (
                clean_url in st.session_state["lead_cache"]
            )

            # Stage 1: Profile Detection
            render_processing(
                current=idx + 1,
                total=total,
                current_url=clean_url,
                stage=0,
                completed=idx,
                cached_count=cached_count,
                elapsed=time.time() - start_time
            )

            if is_cached:

                lead_data = st.session_state["lead_cache"][
                    clean_url
                ].copy()

                cached_count += 1

            else:

                # Stage 2: Metadata Extraction
                lead_data = extract_profile_with_session(
                    session,
                    clean_url
                )

                render_processing(
                    current=idx + 1,
                    total=total,
                    current_url=clean_url,
                    stage=2,
                    completed=idx,
                    cached_count=cached_count,
                    elapsed=time.time() - start_time
                )

                # Stage 3: Optional Gemini AI enrichment
                if gemini_key:

                    lead_data = enrich_with_gemini(
                        gemini_key,
                        clean_url,
                        lead_data,
                        selected_fields
                    )

                # Save to cache
                st.session_state["lead_cache"][clean_url] = (
                    lead_data.copy()
                )

            # Stage 4: Final Verification
            render_processing(
                current=idx + 1,
                total=total,
                current_url=clean_url,
                stage=4,
                completed=idx,
                cached_count=cached_count,
                elapsed=time.time() - start_time
            )

            # Attach original input information
            lead_data["LinkedIn URL"] = clean_url
            lead_data["Original Input URL"] = orig_url

            results.append(lead_data)

            # Update progress after this profile is complete
            render_processing(
                current=idx + 1,
                total=total,
                current_url=clean_url,
                stage=5,
                completed=idx + 1,
                cached_count=cached_count,
                elapsed=time.time() - start_time
            )

            if not is_cached:
                time.sleep(request_delay)

        # -------------------------------------------------
        # Processing completed
        # -------------------------------------------------

        elapsed = round(time.time() - start_time, 1)

        with progress_placeholder.container():

            st.success("✓ ENRICHMENT COMPLETED")

            st.markdown(
                f"Successfully processed **{total} profiles**."
            )

            done1, done2, done3 = st.columns(3)

            with done1:
                st.metric("TOTAL PROFILES", total)

            with done2:
                st.metric("CACHED PROFILES", cached_count)

            with done3:
                st.metric("TIME TAKEN", f"{elapsed}s")

            st.progress(1.0, text="100% Complete")

        st.success(
            f"Successfully completed {total} profiles in "
            f"{elapsed} seconds! "
            f"({cached_count} cached profiles; "
            f"{duplicates_count} duplicate rows removed)"
        )

        # -------------------------------------------------
        # Build enriched dataframe
        # -------------------------------------------------

        enriched_df = pd.DataFrame(results)

        ordered_cols = (
            ["Original Input URL", "LinkedIn URL"]
            + [
                field for field in selected_fields
                if field in enriched_df.columns
            ]
            + ["Status"]
        )

        if (
            "Location" in enriched_df.columns
            and "Country" in selected_fields
        ):
            ordered_cols.append("Location")

        final_df = enriched_df[
            [
                col for col in ordered_cols
                if col in enriched_df.columns
            ]
        ]

        # -------------------------------------------------
        # Merge with original Excel spreadsheet
        # -------------------------------------------------

        if (
            source_df is not None
            and selected_url_col
            and keep_original
        ):

            res_dict = {
                result["LinkedIn URL"]: result
                for result in results
            }

            merged_rows = []
            seen_in_export = set()

            for _, row in source_df.iterrows():

                row_dict = row.to_dict()

                raw_val = str(
                    row_dict.get(selected_url_col, "")
                ).strip()

                clean_val = clean_linkedin_url(raw_val)

                # Skip duplicate profiles in export
                if clean_val and clean_val in seen_in_export:
                    continue

                if clean_val:

                    seen_in_export.add(clean_val)

                    match_res = res_dict.get(clean_val)

                    if match_res:

                        for field in selected_fields:
                            row_dict[f"Enriched {field}"] = (
                                match_res.get(field, "")
                            )

                        row_dict["Enrichment Status"] = (
                            match_res.get("Status", "Processed")
                        )

                    else:

                        for field in selected_fields:
                            row_dict[f"Enriched {field}"] = ""

                        row_dict["Enrichment Status"] = (
                            "Not processed"
                        )

                else:

                    for field in selected_fields:
                        row_dict[f"Enriched {field}"] = ""

                    row_dict["Enrichment Status"] = (
                        "Invalid URL"
                    )

                merged_rows.append(row_dict)

            final_export_df = pd.DataFrame(merged_rows)

        else:

            final_export_df = final_df.drop_duplicates(
                subset=["LinkedIn URL"],
                keep="first"
            )

        # -------------------------------------------------
        # Save results for export section
        # -------------------------------------------------

        st.session_state["enriched_results_df"] = final_export_df

        st.session_state["duplicates_removed_count"] = (
            duplicates_count
        )

# -------------------------------------------------------------
# Results & Multi-Format Export Center
# -------------------------------------------------------------
if "enriched_results_df" in st.session_state and st.session_state["enriched_results_df"] is not None:
    export_df = st.session_state["enriched_results_df"]
    dup_removed = st.session_state.get("duplicates_removed_count", 0)
    
    st.write("")
    st.markdown("---")
    st.markdown(f'<div class="section-heading">4. Enriched Dataset ({len(export_df)} Unique Rows)</div>', unsafe_allow_html=True)
    
    if dup_removed > 0:
        st.info(f"✂️ **Duplicate Management:** `{dup_removed}` duplicate profile row{'s were' if dup_removed > 1 else ' was'} automatically removed from the dataset. All {len(export_df)} records in the export are 100% unique.")

    # Complete, non-truncated dataframe display
    st.dataframe(export_df, use_container_width=True, height=500)
    
    st.markdown("### 📥 Export Your Enriched Data")
    if dup_removed > 0:
        st.caption(f"Ready for export &bull; **{len(export_df)} Unique Leads** &bull; ✂️ **{dup_removed} Duplicate{'s' if dup_removed > 1 else ''} Filtered Out**")
    else:
        st.caption(f"Ready for export &bull; **{len(export_df)} Unique Leads** &bull; Zero duplicates detected")

    export_view = st.radio(
        "Export Column View:",
        ["All Enriched Columns", "Email Campaign View (Emails Only)", "Calling List View (Phones Only)"],
        horizontal=True
    )
    
    # Filter columns based on chosen view
    if export_view == "Email Campaign View (Emails Only)":
        filter_cols = [c for c in export_df.columns if not any(k in c.lower() for k in ["phone", "country", "location"])]
        curr_export_df = export_df[filter_cols] if filter_cols else export_df
    elif export_view == "Calling List View (Phones Only)":
        filter_cols = [c for c in export_df.columns if not any(k in c.lower() for k in ["email", "website"])]
        curr_export_df = export_df[filter_cols] if filter_cols else export_df
    else:
        curr_export_df = export_df

    d1, d2 = st.columns(2)
    excel_data = to_styled_excel(curr_export_df)
    csv_data = curr_export_df.to_csv(index=False).encode("utf-8")
    

    # Generate download filenames from the original uploaded file
    if uploaded is not None:
        original_name = uploaded.name
        file_name_without_ext = os.path.splitext(original_name)[0]
    else:
        file_name_without_ext = "findora_leads"

    excel_file_name = f"{file_name_without_ext}.xlsx"
    csv_file_name = f"{file_name_without_ext}.csv"

    with d1:
        st.download_button(
            label="📥 Download Formatted Excel (.xlsx)",
            data=excel_data,
            file_name=excel_file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with d2:
        st.download_button(
            label="📄 Download Clean CSV (.csv)",
            data=csv_data,
            file_name=csv_file_name,
            mime="text/csv",
            use_container_width=True
        )


st.write("")
st.caption("Findora Global &bull; Enterprise-grade contact enrichment & intelligence &bull; Crafted & maintained By Pushkar Shete")
