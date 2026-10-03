"""Design System, CSS Styling and HTML Rendering Utilities for Re:Learn.

Provides a sophisticated dark theme, glassmorphic card tokens, typography hierarchy,
and guaranteed-safe HTML rendering via st.html() to avoid CommonMark code block conversion.
"""

import textwrap
import streamlit as st


def render_html(html_str: str) -> None:
    """Safely render HTML in Streamlit.
    
    Uses st.html() with textwrap.dedent to ensure no markdown-it 4-space code block
    escaping occurs, completely preventing raw HTML/CSS source code from displaying as text.
    """
    cleaned = textwrap.dedent(html_str).strip()
    if hasattr(st, "html"):
        st.html(cleaned)
    else:
        st.markdown(cleaned, unsafe_allow_html=True)


DARK_THEME_CSS = """
<style>
/* -------------------------------------------------------------------------
   RE:LEARN DESIGN SYSTEM — SOPHISTICATED DARK PALETTE & TOKENS
   ------------------------------------------------------------------------- */
:root {
  --re-bg-main: #060911;
  --re-bg-surface: #0a0f1d;
  --re-bg-card: rgba(14, 21, 38, 0.75);
  --re-bg-card-hover: rgba(22, 33, 58, 0.85);
  --re-bg-card-alt: rgba(18, 26, 47, 0.60);
  
  --re-border-subtle: rgba(255, 255, 255, 0.07);
  --re-border-card: rgba(255, 255, 255, 0.10);
  --re-border-focus: #6366f1;
  
  --re-accent-indigo: #6366f1;
  --re-accent-violet: #8b5cf6;
  --re-accent-purple: #a855f7;
  --re-accent-cyan: #06b6d4;
  --re-accent-emerald: #10b981;
  --re-accent-amber: #f59e0b;
  --re-accent-rose: #f43f5e;
  
  --re-text-primary: #f8fafc;
  --re-text-secondary: #94a3b8;
  --re-text-muted: #64748b;
  --re-text-highlight: #c7d2fe;
  
  --re-radius-xl: 18px;
  --re-radius-lg: 14px;
  --re-radius-md: 10px;
  --re-radius-sm: 6px;
  
  --re-shadow-card: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
  --re-shadow-glow: 0 0 25px rgba(99, 102, 241, 0.25);
  --re-shadow-glow-emerald: 0 0 25px rgba(16, 185, 129, 0.25);
  --re-shadow-glow-amber: 0 0 25px rgba(245, 158, 11, 0.25);
}

/* -------------------------------------------------------------------------
   GLOBAL STREAMLIT RESETS & BACKGROUND
   ------------------------------------------------------------------------- */
.stApp {
  background-color: var(--re-bg-main) !important;
  background-image: 
    radial-gradient(circle at 10% -10%, rgba(99, 102, 241, 0.12) 0%, transparent 45%),
    radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
    radial-gradient(circle at 50% 50%, rgba(6, 182, 212, 0.03) 0%, transparent 50%) !important;
  color: var(--re-text-primary) !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
  letter-spacing: -0.01em;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
  background-color: var(--re-bg-surface) !important;
  border-right: 1px solid var(--re-border-subtle) !important;
}

[data-testid="stSidebar"] > div:first-child {
  padding-top: 1.5rem !important;
  padding-left: 1.2rem !important;
  padding-right: 1.2rem !important;
}

/* Clean up Streamlit default header/footer */
header[data-testid="stHeader"] {
  background-color: transparent !important;
  display: none !important;
}

footer {
  display: none !important;
}

/* Block container padding adjustment */
.main .block-container {
  max-width: 1360px !important;
  padding-top: 1.2rem !important;
  padding-bottom: 3.5rem !important;
  padding-left: 1.8rem !important;
  padding-right: 1.8rem !important;
}

/* -------------------------------------------------------------------------
   STREAMLIT FORM CONTROLS & INPUTS
   ------------------------------------------------------------------------- */
div[data-baseweb="select"] > div {
  background-color: rgba(14, 21, 38, 0.8) !important;
  border: 1px solid var(--re-border-card) !important;
  border-radius: var(--re-radius-md) !important;
  color: var(--re-text-primary) !important;
  transition: all 0.2s ease;
}

div[data-baseweb="select"] > div:hover {
  border-color: var(--re-accent-indigo) !important;
}

div[data-baseweb="select"] * {
  color: var(--re-text-primary) !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
.stTextInput input,
.stTextArea textarea {
  background-color: rgba(14, 21, 38, 0.8) !important;
  border: 1px solid var(--re-border-card) !important;
  border-radius: var(--re-radius-md) !important;
  color: var(--re-text-primary) !important;
  font-size: 0.96rem !important;
  line-height: 1.55 !important;
  transition: all 0.2s ease !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
  border-color: var(--re-accent-indigo) !important;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.22) !important;
  outline: none !important;
}

/* -------------------------------------------------------------------------
   STREAMLIT BUTTONS
   ------------------------------------------------------------------------- */
button[kind="primary"] {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 60%, #a855f7 100%) !important;
  border: none !important;
  color: #ffffff !important;
  font-weight: 600 !important;
  font-size: 0.95rem !important;
  letter-spacing: 0.02em !important;
  border-radius: var(--re-radius-md) !important;
  padding: 0.7rem 1.5rem !important;
  box-shadow: 0 4px 18px rgba(99, 102, 241, 0.4) !important;
  transition: all 0.2s ease !important;
}

button[kind="primary"]:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 24px rgba(99, 102, 241, 0.55) !important;
  filter: brightness(1.08) !important;
}

button[kind="primary"]:active {
  transform: translateY(1px) !important;
}

button[kind="secondary"] {
  background-color: rgba(255, 255, 255, 0.04) !important;
  border: 1px solid var(--re-border-card) !important;
  color: var(--re-text-secondary) !important;
  font-weight: 500 !important;
  font-size: 0.85rem !important;
  border-radius: var(--re-radius-md) !important;
  padding: 0.45rem 0.9rem !important;
  transition: all 0.2s ease !important;
}

button[kind="secondary"]:hover {
  background-color: rgba(99, 102, 241, 0.12) !important;
  border-color: rgba(99, 102, 241, 0.35) !important;
  color: var(--re-text-primary) !important;
}

/* -------------------------------------------------------------------------
   STREAMLIT TABS STYLING
   ------------------------------------------------------------------------- */
div[data-testid="stTabs"] {
  margin-top: 0.2rem;
}

button[data-baseweb="tab"] {
  background-color: transparent !important;
  color: var(--re-text-secondary) !important;
  border-radius: var(--re-radius-sm) !important;
  padding: 0.6rem 1.2rem !important;
  font-weight: 600 !important;
  font-size: 0.92rem !important;
  transition: color 0.15s ease !important;
}

button[data-baseweb="tab"]:hover {
  color: var(--re-text-primary) !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
  color: #ffffff !important;
  border-bottom: 2px solid var(--re-accent-indigo) !important;
}

/* -------------------------------------------------------------------------
   EXPANDERS
   ------------------------------------------------------------------------- */
div[data-testid="stExpander"] {
  background: rgba(14, 21, 38, 0.6) !important;
  border: 1px solid var(--re-border-subtle) !important;
  border-radius: var(--re-radius-md) !important;
  margin-bottom: 0.65rem !important;
  overflow: hidden;
}

div[data-testid="stExpander"] details summary {
  color: var(--re-text-primary) !important;
  font-weight: 600 !important;
  padding: 0.75rem 1rem !important;
}

/* -------------------------------------------------------------------------
   CUSTOM GLASSMORPHIC UTILITY CLASSES
   ------------------------------------------------------------------------- */
.re-glass-panel {
  background: var(--re-bg-card);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--re-border-card);
  border-radius: var(--re-radius-lg);
  box-shadow: var(--re-shadow-card);
}

.re-glass-panel-subtle {
  background: var(--re-bg-card-alt);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--re-border-subtle);
  border-radius: var(--re-radius-md);
}

.re-hero-card {
  background: linear-gradient(135deg, rgba(16, 24, 44, 0.9) 0%, rgba(11, 16, 31, 0.9) 100%);
  border: 1px solid rgba(99, 102, 241, 0.28);
  border-radius: var(--re-radius-xl);
  box-shadow: var(--re-shadow-glow), var(--re-shadow-card);
}

.re-gradient-text {
  background: linear-gradient(135deg, #818cf8 0%, #c084fc 50%, #38bdf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
}
</style>
"""


def apply_custom_styles():
    """Inject the dark premium CSS styles into the active Streamlit app."""
    render_html(DARK_THEME_CSS)
