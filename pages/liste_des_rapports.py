import streamlit as st
import pandas as pd
from common import (
    render_topbar, ICON_DOC, ICON_STAR, ICON_SEARCH, ICON_FOLDER,
    ICON_FILTER, ICON_CHEVRON_DOWN, ICON_CHEVRON_RIGHT, ICON_INFO,
    ICON_LIST_VIEW, ICON_GRID_VIEW, ICON_SETTINGS, ICON_KEBAB
)

render_topbar("Production M3 13.4")

st.markdown('<div class="page-title font-serif">Liste des rapports</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Accédez à l\'ensemble des rapports disponibles et analysez vos données.</div>',
    unsafe_allow_html=True
)

# ============================================================
# SEARCH ROW
# ============================================================

# Search bar shortened: search_col ratio reduced (was 5), spacer_col
# increased to absorb the freed width so the button/favoris stay put.
search_col, btn_col, spacer_col, fav_col = st.columns([3, 1, 5, 1.4])

with search_col:
    st.text_input(
        "Recherche",
        placeholder="Rechercher un rapport...",
        label_visibility="collapsed",
        key="report_search"
    )

with btn_col:
    st.markdown('<div class="lr-search-btn">', unsafe_allow_html=True)
    st.button("Rechercher", key="report_search_btn", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with fav_col:
    st.button(f"☆  Mes favoris", key="mes_favoris_btn", use_container_width=True)

st.markdown('<div style="height:22px;"></div>', unsafe_allow_html=True)

# ============================================================
# MOCK DATA — REPORTS TABLE
# ============================================================

reports = pd.DataFrame([
    {"titre": "Mesures des Nouveaux Produits", "desc": "Suivi des mesures et performances produits",
     "numero": 1722, "dossier": "Logistique - Infolog", "proprietaire": "J. Martin",
     "maj": "23/05/2026", "usages": 124, "favori": False, "page": None},
    {"titre": "Article - Liste des Coloris / Taille", "desc": "Référentiel des coloris et tailles par article",
     "numero": 646, "dossier": "Nouvelles requêtes - Référentiel Article", "proprietaire": "A. Dubois",
     "maj": "22/05/2026", "usages": 312, "favori": False, "page": "article_coloris"},
    {"titre": "Commandes - Détail", "desc": "Détail des commandes et lignes associées",
     "numero": 667, "dossier": "Nouvelles requêtes - Gestion Commerciale", "proprietaire": "S. Bernard",
     "maj": "21/05/2026", "usages": 845, "favori": False, "page": None},
    {"titre": "Stock Disponible - Dépôt Métier", "desc": "Disponibilités stock par dépôt et métier",
     "numero": 662, "dossier": "Nouvelles requêtes - Gestion Commerciale", "proprietaire": "M. Moreau",
     "maj": "20/05/2026", "usages": 278, "favori": False, "page": None},
    {"titre": "Expéditions - Détail (après Facturation)", "desc": "Détail des expéditions après facturation",
     "numero": 669, "dossier": "Nouvelles requêtes - Gestion Commerciale", "proprietaire": "J. Martin",
     "maj": "20/05/2026", "usages": 193, "favori": False, "page": None},
    {"titre": "Commandes - Consolidation (Temps Réel)", "desc": "Consolidation temps réel des commandes",
     "numero": 986, "dossier": "Nouvelles requêtes - Gestion Commerciale", "proprietaire": "A. Dubois",
     "maj": "19/05/2026", "usages": 156, "favori": False, "page": None},
    {"titre": "Liste des Produits", "desc": "Référentiel complet des produits",
     "numero": 644, "dossier": "Nouvelles requêtes - Référentiel Article", "proprietaire": "S. Bernard",
     "maj": "19/05/2026", "usages": 98, "favori": False, "page": None},
    {"titre": "Factures - CA Consolidation (J-1)", "desc": "Chiffre d'affaires consolidé à J-1",
     "numero": 671, "dossier": "Nouvelles requêtes - Gestion Financière", "proprietaire": "M. Moreau",
     "maj": "18/05/2026", "usages": 211, "favori": False, "page": None},
])

REPERTOIRE_TREE = [
    {"label": "Tous les dossiers", "level": 0, "chevron": True, "state": "normal"},
    {"label": "Favoris", "level": 0, "chevron": False, "state": "normal", "star": True},
    {"label": "Informatique", "level": 0, "chevron": "down", "state": "parent-active"},
    {"label": "Production informatique", "level": 1, "chevron": True, "state": "normal"},
    {"label": "Infocentre", "level": 1, "chevron": True, "state": "active"},
    {"label": "Procédure tarifaire", "level": 1, "chevron": True, "state": "normal"},
    {"label": "Nouvelles requêtes", "level": 0, "chevron": True, "state": "normal"},
    {"label": "Référentiel Article", "level": 0, "chevron": True, "state": "normal"},
    {"label": "LMH - Gestion Commerciale", "level": 0, "chevron": True, "state": "normal"},
    {"label": "LMH - Gestion Financière", "level": 0, "chevron": True, "state": "normal"},
    {"label": "LMH - Gestion Production", "level": 0, "chevron": True, "state": "normal"},
    {"label": "LMH - Contrôle de gestion", "level": 0, "chevron": True, "state": "normal"},
    {"label": "LMH - Logistique", "level": 0, "chevron": True, "state": "normal"},
    {"label": "Référentiel Mercure", "level": 0, "chevron": True, "state": "normal"},
    {"label": "Divers", "level": 0, "chevron": True, "state": "normal"},
]

# ============================================================
# LAYOUT: REPERTOIRES (left) + TABLE (right)
# ============================================================

left_col, right_col = st.columns([1.15, 3.4], gap="medium")

# ---------------- LEFT: REPERTOIRES ----------------

with left_col:

    st.markdown('<div class="repertoire-panel">', unsafe_allow_html=True)
    st.markdown('<div class="repertoire-title font-serif">Répertoires</div>', unsafe_allow_html=True)

    st.text_input(
        "Rechercher un dossier",
        placeholder="Rechercher un dossier...",
        label_visibility="collapsed",
        key="folder_search"
    )

    st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)

    tree_html = ""
    for item in REPERTOIRE_TREE:
        indent_class = "tree-indent-1" if item["level"] == 1 else ""
        state_class = {
            "active": "tree-active",
            "parent-active": "tree-parent-active",
            "normal": "",
        }[item["state"]]

        if item.get("star"):
            chevron_html = f'<span class="tree-chevron">{ICON_STAR}</span>'
        elif item["chevron"] == "down":
            chevron_html = f'<span class="tree-chevron">{ICON_CHEVRON_DOWN}</span>'
        elif item["chevron"]:
            chevron_html = f'<span class="tree-chevron">{ICON_CHEVRON_RIGHT}</span>'
        else:
            chevron_html = '<span class="tree-chevron" style="width:15px;"></span>'

        icon_html = "" if item.get("star") else f'<span class="tree-icon">{ICON_FOLDER}</span>'

        tree_html += (
            f'<div class="tree-item {state_class} {indent_class}">'
            f'{chevron_html}{icon_html}<span>{item["label"]}</span></div>'
        )

    st.markdown(tree_html, unsafe_allow_html=True)

    st.markdown(
        f'<div class="tree-footer">{ICON_SETTINGS}<span>Gérer les dossiers</span></div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- RIGHT: REPORTS TABLE ----------------

with right_col:

    count_col, filt_col, sort_label_col, sort_col, view1_col, view2_col = st.columns(
        [3, 1.1, 0.9, 1.5, 0.55, 0.55]
    )

    with count_col:
        st.markdown(f'<div class="rl-count">{len(reports)} rapports</div>', unsafe_allow_html=True)

    with filt_col:
        st.button(f"▽  Filtres", key="filters_btn", use_container_width=True)

    with sort_label_col:
        st.markdown('<div style="padding-top:6px; font-size:13px; color:#6E6A63;">Trier par</div>', unsafe_allow_html=True)

    with sort_col:
        st.selectbox(
            "Trier par", ["Nom (A-Z)", "Nom (Z-A)", "Dernière modif.", "Utilisations"],
            label_visibility="collapsed", key="sort_select"
        )

    with view1_col:
        st.markdown(
            f'<div class="pill-btn active" style="padding:8px 10px;">{ICON_LIST_VIEW}</div>',
            unsafe_allow_html=True
        )

    with view2_col:
        st.markdown(
            f'<div class="pill-btn" style="padding:8px 10px;">{ICON_GRID_VIEW}</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)

    # Header: "Propriétaire", "Dernière modif." and "Utilisations" columns
    # removed. Only Rapport / Numéro / Dossier + the two action cells remain.
    st.markdown(
        f"""
        <div class="rl-table-header rl-table-header-compact">
            <div>Rapport</div>
            <div>Numéro</div>
            <div>Dossier</div>
            <div></div>
            <div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    rows_html = ""
    for _, r in reports.iterrows():
        star_class = "filled" if r["favori"] else ""
        title_html = r["titre"]
        # The "Article - Liste des Coloris / Taille" row links to the
        # real Snowflake-connected report page via st.page_link below
        # the table (kept as a plain highlighted row here so the grid
        # stays visually consistent; see the linked-row note underneath).
        rows_html += f"""
        <div class="rl-row rl-row-compact">
            <div class="rl-report-cell">
                <div class="rl-report-icon">{ICON_DOC}</div>
                <div>
                    <div class="rl-report-title">{title_html}</div>
                    <div class="rl-report-desc">{r['desc']}</div>
                </div>
            </div>
            <div class="rl-cell">{r['numero']}</div>
            <div class="rl-cell">{r['dossier']}</div>
            <div class="rl-star {star_class}">{ICON_STAR}</div>
            <div class="rl-kebab">{ICON_KEBAB}</div>
        </div>
        """

    st.markdown(rows_html, unsafe_allow_html=True)

    # Real, working navigation into the Snowflake-connected report,
    # for the row that corresponds to an actual page in this app.
    linked_row = reports[reports["page"] == "article_coloris"].iloc[0]
    st.page_link(
        "pages/article_coloris.py",
        label=f"Ouvrir « {linked_row['titre']} » (rapport n°{linked_row['numero']})",
        icon=":material/open_in_new:",
    )

    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

    # ---------------- FOOTER: PAGE SIZE + PAGINATION ----------------

    foot_left, foot_right = st.columns([2, 3])

    with foot_left:
        pp_label, pp_select = st.columns([2, 1])
        with pp_label:
            st.markdown('<div style="padding-top:6px; font-size:13.5px; color:#4A4640;">Afficher</div>', unsafe_allow_html=True)
        with pp_select:
            st.selectbox("Résultats par page", ["25", "50", "100"], label_visibility="collapsed", key="page_size")

    with foot_right:
        st.markdown(
            f"""
            <div class="pagination-row" style="justify-content:flex-end;">
                <div class="page-pill">‹</div>
                <div class="page-pill current">1</div>
                <div class="page-pill">2</div>
                <div class="page-pill">3</div>
                <div class="page-pill">4</div>
                <div class="page-pill">5</div>
                <div class="page-pill">…</div>
                <div class="page-pill">›</div>
            </div>
            """,
            unsafe_allow_html=True,
        )