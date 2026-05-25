import streamlit as st

PALETTE = {
    "bg_void": "#0a0c10",
    "panel": "#12151c",
    "panel_hover": "#181c26",
    "border": "#1e222d",
    "gold": "#d4a44a",
    "gold_bright": "#f0c96e",
    "parchment": "#e0ddd5",
    "parchment_bright": "#ece8df",
    "muted": "#8a8578",
    "dim": "#6b6560",
    "blue": "#6ab0d4",
    "success": "#7fae6a",
    "warning": "#d4a44a",
    "error": "#c2603f",
}


def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        :root {{
            --bg-void: {PALETTE["bg_void"]};
            --panel: {PALETTE["panel"]};
            --panel-hover: {PALETTE["panel_hover"]};
            --border: {PALETTE["border"]};
            --gold: {PALETTE["gold"]};
            --gold-bright: {PALETTE["gold_bright"]};
            --parchment: {PALETTE["parchment"]};
            --parchment-bright: {PALETTE["parchment_bright"]};
            --muted: {PALETTE["muted"]};
            --dim: {PALETTE["dim"]};
            --blue: {PALETTE["blue"]};
            --success: {PALETTE["success"]};
            --warning: {PALETTE["warning"]};
            --error: {PALETTE["error"]};
        }}

        .stApp {{
            background-color: var(--bg-void);
            color: var(--parchment);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
        }}

        .stApp header {{
            background-color: var(--bg-void) !important;
        }}

        .stApp [data-testid="stHeader"] {{
            background-color: var(--bg-void) !important;
        }}

        .stApp [data-testid="stToolbar"] {{
            display: none;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: var(--gold) !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 600;
        }}

        h1 {{
            font-size: 2.2rem !important;
            letter-spacing: 3px;
        }}

        p, li, span, label {{
            color: var(--parchment);
        }}

        .stMarkdown {{
            color: var(--parchment);
        }}

        /* Buttons */
        .stButton > button {{
            background-color: var(--panel) !important;
            color: var(--gold) !important;
            border: 1px solid var(--gold) !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
            transition: all 0.3s ease !important;
        }}

        .stButton > button:hover {{
            background-color: var(--gold) !important;
            color: var(--bg-void) !important;
            box-shadow: 0 0 15px rgba(212, 164, 74, 0.3) !important;
        }}

        .stButton > button:disabled {{
            background-color: var(--panel) !important;
            color: var(--dim) !important;
            border-color: var(--border) !important;
            box-shadow: none !important;
        }}

        /* Primary button (Go button) */
        .stButton > button[kind="primary"] {{
            background-color: var(--blue) !important;
            color: var(--bg-void) !important;
            border-color: var(--blue) !important;
            font-weight: 700 !important;
        }}

        .stButton > button[kind="primary"]:hover {{
            box-shadow: 0 0 20px rgba(106, 176, 212, 0.4) !important;
        }}

        /* File uploader */
        [data-testid="stFileUploader"] {{
            background-color: var(--panel) !important;
            border: 1px dashed var(--border) !important;
            border-radius: 10px !important;
            padding: 1rem !important;
        }}

        [data-testid="stFileUploader"]:hover {{
            border-color: var(--gold) !important;
        }}

        /* Select boxes */
        .stSelectbox > div > div {{
            background-color: var(--panel) !important;
            border-color: var(--border) !important;
            color: var(--parchment) !important;
        }}

        /* Metrics */
        [data-testid="stMetric"] {{
            background-color: var(--panel);
            border: 1px solid var(--border);
            border-left: 3px solid var(--gold);
            border-radius: 8px;
            padding: 1rem;
        }}

        [data-testid="stMetricLabel"] {{
            color: var(--muted) !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.75rem !important;
        }}

        [data-testid="stMetricValue"] {{
            color: var(--gold-bright) !important;
            font-weight: 600 !important;
        }}

        /* Progress bar */
        .stProgress > div > div > div {{
            background-color: var(--gold) !important;
        }}

        .stProgress > div > div {{
            background-color: var(--border) !important;
        }}

        /* Tables / dataframes */
        .stDataFrame {{
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
        }}

        [data-testid="stDataFrame"] th {{
            background-color: var(--panel) !important;
            color: var(--gold) !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            font-size: 0.75rem !important;
        }}

        [data-testid="stDataFrame"] td {{
            background-color: var(--bg-void) !important;
            color: var(--parchment) !important;
            border-color: var(--border) !important;
        }}

        /* Expander */
        .streamlit-expanderHeader {{
            background-color: var(--panel) !important;
            color: var(--gold) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: var(--panel) !important;
            border-right: 1px solid var(--border) !important;
        }}

        /* Toggle */
        .stCheckbox label span {{
            color: var(--parchment) !important;
        }}

        /* Alerts */
        .stAlert {{
            border-radius: 8px !important;
        }}

        /* Custom classes */
        .vai-title {{
            text-align: center;
            padding: 2rem 0 0.5rem 0;
        }}

        .vai-title h1 {{
            font-size: 2.8rem !important;
            letter-spacing: 4px !important;
            margin-bottom: 0 !important;
            color: var(--gold) !important;
        }}

        .vai-subtitle {{
            text-align: center;
            color: var(--muted);
            font-style: italic;
            font-size: 0.9rem;
            margin-bottom: 2rem;
            letter-spacing: 1px;
        }}

        .status-sent {{
            color: var(--success);
            font-weight: 600;
        }}

        .status-failed {{
            color: var(--error);
            font-weight: 600;
        }}

        .status-needs-review {{
            color: var(--warning);
            font-weight: 600;
        }}

        .status-pending {{
            color: var(--dim);
        }}

        .gold-divider {{
            border: none;
            border-top: 1px solid var(--border);
            margin: 2rem 0;
        }}

        .card {{
            background-color: var(--panel);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            transition: border-color 0.3s ease;
        }}

        .card:hover {{
            border-color: var(--gold);
            box-shadow: 0 0 10px rgba(212, 164, 74, 0.1);
        }}

        .badge {{
            display: inline-block;
            padding: 0.2rem 0.8rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .badge-gold {{
            background-color: rgba(212, 164, 74, 0.15);
            color: var(--gold);
            border: 1px solid var(--gold);
        }}

        .badge-success {{
            background-color: rgba(127, 174, 106, 0.15);
            color: var(--success);
            border: 1px solid var(--success);
        }}

        .badge-error {{
            background-color: rgba(194, 96, 63, 0.15);
            color: var(--error);
            border: 1px solid var(--error);
        }}

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0;
            background-color: var(--panel);
            border-radius: 8px;
            padding: 4px;
            border: 1px solid var(--border);
        }}

        .stTabs [data-baseweb="tab"] {{
            color: var(--muted) !important;
            border-radius: 6px;
            padding: 0.5rem 1.5rem;
        }}

        .stTabs [aria-selected="true"] {{
            background-color: var(--bg-void) !important;
            color: var(--gold) !important;
            border: 1px solid var(--border);
        }}

        /* Number input */
        .stNumberInput input {{
            background-color: var(--panel) !important;
            color: var(--parchment) !important;
            border-color: var(--border) !important;
        }}

        /* Text input */
        .stTextInput input {{
            background-color: var(--panel) !important;
            color: var(--parchment) !important;
            border-color: var(--border) !important;
        }}

        /* Download button */
        .stDownloadButton > button {{
            background-color: var(--panel) !important;
            color: var(--gold) !important;
            border: 1px solid var(--gold) !important;
            border-radius: 8px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_title():
    st.markdown(
        '<div class="vai-title"><h1>vAI Send Mail</h1></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="vai-subtitle">The mailing must flow.</p>',
        unsafe_allow_html=True,
    )
