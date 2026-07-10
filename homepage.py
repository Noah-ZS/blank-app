import streamlit as st
import pandas as pd

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(layout="wide", page_title="Infocentre")

# ============================================================
# ICONS
# Small inline SVGs (Lucide-style outline icons) so the app has
# no external icon-font dependency. Each accepts currentColor so
# it inherits whatever text color wraps it.
# ============================================================

def icon(path, size=18, stroke_width=1.8):
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round">{path}</svg>'
    )

ICON_HOME = icon('<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v9a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-9"/><path d="M9.5 20v-6h5v6"/>')
ICON_DOC = icon('<path d="M7 3h7l5 5v13a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Z"/><path d="M14 3v5h5"/>')
ICON_CHART = icon('<path d="M4 19V11"/><path d="M10 19V5"/><path d="M16 19v-8"/><path d="M3 19h18"/>')
ICON_BAG = icon('<path d="M6 8h12l-1 12H7L6 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>')
ICON_CLOCK = icon('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>')
ICON_STAR = icon('<path d="M12 3.5l2.5 5.5 6 .6-4.5 4 1.3 6-5.3-3-5.3 3 1.3-6-4.5-4 6-.6 2.5-5.5Z"/>', stroke_width=1.6)
ICON_CHEVRON_RIGHT = icon('<path d="m9 6 6 6-6 6"/>', size=15, stroke_width=2.1)
ICON_CHEVRON_DOWN = icon('<path d="m6 9 6 6 6-6"/>', size=15, stroke_width=2.1)
ICON_ARROW_UP = icon('<path d="M12 19V6"/><path d="m6 12 6-6 6 6"/>', size=13, stroke_width=2.3)
ICON_ARROW_DOWN = icon('<path d="M12 5v13"/><path d="m18 12-6 6-6-6"/>', size=13, stroke_width=2.3)
ICON_KEBAB = icon('<circle cx="12" cy="5" r="1.3"/><circle cx="12" cy="12" r="1.3"/><circle cx="12" cy="19" r="1.3"/>', size=16)
ICON_LOGOUT = icon('<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="M16 17l5-5-5-5"/><path d="M21 12H9"/>', size=17)

# ============================================================
# GLOBAL STYLE
# Token system:
#   ink        #1C1B19  headings / primary text
#   ink-soft   #6E6A63  secondary text
#   accent     #D9642A  Hermès-inspired terracotta-orange
#   accent-bg  #FBEAE0  soft accent chip background
#   cream      #FAF8F4  sidebar background
#   card       #F8F6F2  KPI card background
#   line       #EAE5DC  hairline borders
#   success    #1E8A5F  positive delta
# Display face: 'Fraunces' (serif) — body/UI face: 'Inter'
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap');

    :root {
        --ink: #1C1B19;
        --ink-soft: #6E6A63;
        --accent: #D9642A;
        --accent-bg: #FBEAE0;
        --cream: #FAF8F4;
        --card: #F8F6F2;
        --line: #EAE5DC;
        --success: #1E8A5F;
    }

    #MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }

    .stApp { background: #FFFFFF; }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: var(--ink); }

    .font-serif { font-family: 'Fraunces', serif; }

section.main .block-container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 3rem 4rem 3rem; /* Changed top padding to 0 */
}

[data-testid="stHeader"] {
    display: none;
}
div.block-container {
    padding-top: 1rem !important;
}

    /* ---------------- SIDEBAR ---------------- */

    section[data-testid="stSidebar"] {
        background: var(--cream);
        border-right: 1px solid var(--line);
        min-width: 272px;
        max-width: 272px;
    }
    section[data-testid="stSidebar"] > div { padding: 1.6rem 1.3rem; }

    .brand-word {
        font-family: 'Fraunces', serif;
        font-size: 30px;
        font-weight: 600;
        color: var(--ink);
        line-height: 1.1;
        margin: 4px 0 2px 0;
    }
    .brand-sub {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.14em;
        color: var(--accent);
        margin-bottom: 28px;
    }

    .nav-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 12px;
        border-radius: 8px;
        margin-bottom: 4px;
        font-size: 14.5px;
        font-weight: 500;
        color: #57534A;
        border-left: 3px solid transparent;
    }
    .nav-item svg { flex-shrink: 0; color: #8A857B; }
    .nav-item.active {
        color: var(--accent);
        background: var(--accent-bg);
        border-left: 3px solid var(--accent);
    }
    .nav-item.active svg { color: var(--accent); }

    .sidebar-divider { height: 1px; background: var(--line); margin: 20px 0; }

    .lang-pill {
        display: inline-flex; align-items: center; justify-content: center;
        padding: 6px 16px; border-radius: 7px; font-size: 12.5px; font-weight: 600;
    }
    .lang-active { border: 1.4px solid var(--accent); color: var(--accent); }
    .lang-inactive { color: var(--ink-soft); }

    .logout-row {
        display: flex; align-items: center; gap: 10px;
        color: #57534A; font-size: 14px; font-weight: 500; margin-top: 18px;
    }

    /* ---------------- MAIN HEADER ---------------- */

    .topbar {
        display: flex; align-items: center; justify-content: flex-end;
        gap: 14px; color: var(--ink-soft); font-size: 13.5px; margin-bottom: 30px;
    }
    .avatar {
        width: 34px; height: 34px; border-radius: 50%;
        background: #EFECE6; color: var(--ink);
        display: flex; align-items: center; justify-content: center;
        font-size: 12.5px; font-weight: 600;
    }

    .page-title {
        font-family: 'Fraunces', serif;
        font-size: 40px;
        font-weight: 600;
        color: var(--ink);
        margin-bottom: 6px;
    }
    .page-subtitle { color: var(--ink-soft); font-size: 15px; margin-bottom: 34px; }

    /* ---------------- KPI CARDS ---------------- */

    .kpi-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 22px 22px 20px 22px;
        height: 100%;
    }
    .kpi-icon {
        width: 42px; height: 42px; border-radius: 10px;
        background: #FFFFFF; border: 1px solid var(--line);
        display: flex; align-items: center; justify-content: center;
        color: var(--accent); margin-bottom: 14px;
    }
    .kpi-label { font-size: 13.5px; color: var(--ink-soft); margin-bottom: 6px; }
    .kpi-value { font-family: 'Fraunces', serif; font-size: 30px; font-weight: 600; color: var(--ink); margin-bottom: 8px; }
    .kpi-delta { display: flex; align-items: center; gap: 5px; font-size: 12.5px; color: var(--success); font-weight: 500; }

    /* ---------------- LIST PANELS ---------------- */

    .panel {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 22px 22px 12px 22px;
        height: 100%;
    }
    .panel-header {
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 6px;
    }
    .panel-title { font-family: 'Fraunces', serif; font-size: 19px; font-weight: 600; color: var(--ink); }
    .panel-link { display: flex; align-items: center; gap: 3px; color: var(--accent); font-size: 13px; font-weight: 600; }

    .panel-divider { height: 1px; background: var(--line); margin: 10px 0 2px 0; }

    .list-row {
        display: flex; align-items: center; gap: 12px;
        padding: 13px 2px; border-bottom: 1px solid var(--line);
    }
    .list-row:last-child { border-bottom: none; }
    .list-icon {
        width: 30px; height: 30px; border-radius: 7px;
        background: var(--card); border: 1px solid var(--line);
        display: flex; align-items: center; justify-content: center;
        color: #8A857B; flex-shrink: 0;
    }
    .list-icon.starred { color: var(--accent); background: var(--accent-bg); border-color: var(--accent-bg); }
    .list-title { font-size: 14.5px; font-weight: 500; color: var(--ink); }
    .list-category { font-size: 12.5px; color: var(--ink-soft); margin-top: 1px; }
    .list-meta { margin-left: auto; font-size: 12.5px; color: var(--ink-soft); white-space: nowrap; }
    .list-kebab { margin-left: auto; color: #B4AFA6; }

    .panel-footer {
        display: flex; align-items: center; gap: 4px;
        color: var(--accent); font-size: 13.5px; font-weight: 600;
        padding: 14px 2px 4px 2px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# MOCK DATA
# ============================================================

recent_reports = pd.DataFrame([
    {"titre": "Commandes - Détail", "categorie": "Gestion Commerciale", "quand": "Il y a 2 h"},
    {"titre": "Article - Liste des coloris / Taille", "categorie": "Référentiel Article", "quand": "Il y a 5 h"},
    {"titre": "Stock Disponible - Dépôt", "categorie": "Gestion Commerciale", "quand": "Hier"},
    {"titre": "Expéditions - Détail", "categorie": "Gestion Commerciale", "quand": "Hier"},
    {"titre": "Factures - CA Consolidation (J-1)", "categorie": "Gestion Financière", "quand": "Il y a 2 jours"},
])

favorite_reports = pd.DataFrame([
    {"titre": "Commande - Détail", "categorie": "Gestion Commerciale"},
    {"titre": "Article - Emballage", "categorie": "Référentiel Article"},
    {"titre": "Suivi de l'exploit", "categorie": "Production"},
    {"titre": "Open to buy - Synthèse", "categorie": "Pilotage"},
    {"titre": "Ventes - Par pays", "categorie": "Gestion Commerciale"},
])

kpis = [
    {"label": "Rapports générés ce mois", "value": "142", "delta": "+12% vs mois précédent", "trend": "up", "icon": ICON_DOC},
    {"label": "Temps moyen d'exécution", "value": "1.8 s", "delta": "-0.4 s vs mois précédent", "trend": "down", "icon": ICON_CLOCK},
    {"label": "Rapports favoris", "value": "18", "delta": "+3 vs mois précédent", "trend": "up", "icon": ICON_STAR},
]

nav_items = [
    {"icon": ICON_HOME, "label": "Accueil", "active": True},
    {"icon": ICON_DOC, "label": "Liste des rapports", "active": False},
    {"icon": ICON_CHART, "label": "Suivi de l'exploit", "active": False},
    {"icon": ICON_BAG, "label": "Open to buy", "active": False},
]

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # Company logo. Falls back to a text wordmark if image.png
    # isn't present, so the layout still renders cleanly.
    try:
        st.image("image.png", width=180)
    except Exception:
        st.markdown('<div class="brand-word">Infocentre</div>', unsafe_allow_html=True)

    st.markdown('<div class="brand-sub">HERMÈS PARIS</div>', unsafe_allow_html=True)

    nav_html = ""
    for item in nav_items:
        active_class = "active" if item["active"] else ""
        nav_html += (
            f'<div class="nav-item {active_class}">{item["icon"]}'
            f'<span>{item["label"]}</span></div>'
        )
    st.markdown(nav_html, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div style="display:flex; gap:8px;">'
        '<span class="lang-pill lang-active">FR</span>'
        '<span class="lang-pill lang-inactive">EN</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="logout-row">{ICON_LOGOUT}<span>Déconnexion</span></div>',
        unsafe_allow_html=True,
    )

# ============================================================
# TOP BAR
# ============================================================

st.markdown(
    f"""
    <div class="topbar">
        <span>Version Production 5.2.1</span>
        <div class="avatar">UE</div>
        {ICON_CHEVRON_DOWN}
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# TITLE
# ============================================================

st.markdown('<div class="page-title font-serif">Bienvenue sur votre Infocentre</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Votre portail de Business Intelligence dédié à la performance.</div>', unsafe_allow_html=True)

# ============================================================
# KPI CARDS
# ============================================================

kpi_cols = st.columns(3, gap="medium")

for col, kpi in zip(kpi_cols, kpis):
    arrow = ICON_ARROW_UP if kpi["trend"] == "up" else ICON_ARROW_DOWN
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">{kpi['icon']}</div>
                <div class="kpi-label">{kpi['label']}</div>
                <div class="kpi-value font-serif">{kpi['value']}</div>
                <div class="kpi-delta">{kpi['delta']} {arrow}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)

# ============================================================
# TWO-COLUMN LIST PANELS
# ============================================================

left_col, right_col = st.columns(2, gap="large")

with left_col:
    rows_html = ""
    for _, r in recent_reports.iterrows():
        rows_html += f"""
        <div class="list-row">
            <div class="list-icon">{ICON_DOC}</div>
            <div>
                <div class="list-title">{r['titre']}</div>
                <div class="list-category">{r['categorie']}</div>
            </div>
            <div class="list-meta">{r['quand']}</div>
        </div>
        """

    st.markdown(
        f"""
        <div class="panel">
            <div class="panel-header">
                <div class="panel-title font-serif">Rapports récents</div>
                <div class="panel-link">Voir tout {ICON_CHEVRON_RIGHT}</div>
            </div>
            <div class="panel-divider"></div>
            {rows_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_col:
    rows_html = ""
    for _, r in favorite_reports.iterrows():
        rows_html += f"""
        <div class="list-row">
            <div class="list-icon starred">{ICON_STAR}</div>
            <div>
                <div class="list-title">{r['titre']}</div>
                <div class="list-category">{r['categorie']}</div>
            </div>
            <div class="list-kebab">{ICON_KEBAB}</div>
        </div>
        """

    st.markdown(
        f"""
        <div class="panel">
            <div class="panel-header">
                <div class="panel-title font-serif">Vos favoris</div>
                <div class="panel-link">Voir tout {ICON_CHEVRON_RIGHT}</div>
            </div>
            <div class="panel-divider"></div>
            {rows_html}
        </div>
        """,
        unsafe_allow_html=True,
    )