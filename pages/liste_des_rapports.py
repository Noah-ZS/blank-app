import streamlit as st
import pandas as pd
from common import (
    render_topbar, ICON_DOC, ICON_STAR, ICON_SEARCH, ICON_FOLDER,
    ICON_FILTER, ICON_CHEVRON_DOWN, ICON_CHEVRON_RIGHT, ICON_INFO,
    ICON_LIST_VIEW, ICON_GRID_VIEW, ICON_SETTINGS, ICON_KEBAB,
    get_reports_catalog, get_favorites
)
from report_views import (
    render_article_coloris_view, render_mesures_produits_view,
    render_commandes_detail_view
)

render_topbar("Production M3 13.4", breadcrumb=["Accueil", "Liste des rapports"])

st.markdown('<div class="page-title font-serif">Liste des rapports</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Accédez à l\'ensemble des rapports disponibles et analysez vos données.</div>',
    unsafe_allow_html=True
)

# ============================================================
# PAGE-LOCAL STYLE: TAB BAR
# ============================================================

st.markdown(
    """
    <style>
    /* 1. Prevent text wrapping on tab labels */
    [class*="st-key-tab_"] button p {
        white-space: nowrap !important;
    }

    /* 2. Style the main tab buttons */
    [class*="st-key-tab_"]:not([class*="_close_btn"]) button {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        padding: 4px 4px 10px 16px !important; /* Left padding for spacing */
        margin: 0 !important;
        font-size: 14.5px !important;
        font-weight: 500 !important;
        color: var(--ink, #1C1B19) !important;
        border-bottom: 2px solid transparent !important;
    }

    [class*="st-key-tab_"]:not([class*="_close_btn"]) button:hover {
        color: var(--accent, #D9642A) !important;
        background: transparent !important;
    }

    /* 3. Style the Close (×) buttons to seamlessly attach to the label */
    [class*="st-key-tab_"][class*="_close_btn"] button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #B4AFA6 !important;
        padding: 4px 16px 10px 4px !important; /* Right padding for spacing */
        margin: 0 !important;
        font-size: 14px !important;
        border-bottom: 2px solid transparent !important;
    }

    [class*="st-key-tab_"][class*="_close_btn"] button:hover {
        color: #E0473B !important;
    }

    /* 4. Active state: apply the orange underline to BOTH the label and the close button */
    [class*="st-key-tab_"] button[kind="primary"],
    [class*="st-key-tab_"] [data-testid="stBaseButton-primary"],
    [class*="st-key-tab_"] [data-testid="baseButton-primary"] {
        color: var(--accent, #D9642A) !important;
        font-weight: 600 !important;
        border-bottom: 2px solid var(--accent, #D9642A) !important;
    }

    /* 5. FORCE COLUMNS TO HUG CONTENT */
    [data-testid="stHorizontalBlock"]:has([class*="st-key-tab_"]) {
        gap: 0px !important; 
    }

    [data-testid="stHorizontalBlock"]:has([class*="st-key-tab_"]) > [data-testid="column"] {
        min-width: max-content !important;
        width: max-content !important;
        flex: 0 0 auto !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# REPORT REGISTRY
# ============================================================

REPORT_TABS = {
    "mesures": {"label": "Mesures Nouveaux Produits", "render": render_mesures_produits_view},
    "article": {"label": "Article - Coloris / Taille", "render": render_article_coloris_view},
    "commandes": {"label": "Commandes - Détail", "render": render_commandes_detail_view},
}

# ============================================================
# MULTI-TAB STATE
# ============================================================

if "lr_active_tab" not in st.session_state:
    st.session_state.lr_active_tab = "liste"
if "lr_open_tabs" not in st.session_state:
    st.session_state.lr_open_tabs = []  


def _activate_tab(key):
    st.session_state.lr_active_tab = key


def _open_tab(key):
    if key not in st.session_state.lr_open_tabs:
        st.session_state.lr_open_tabs.append(key)
    st.session_state.lr_active_tab = key


def _close_tab(key):
    if key in st.session_state.lr_open_tabs:
        st.session_state.lr_open_tabs.remove(key)
    if st.session_state.lr_active_tab == key:
        st.session_state.lr_active_tab = "liste"


def _toggle_favorite(numero):
    favorites = get_favorites()
    if numero in favorites:
        favorites.remove(numero)
    else:
        favorites.add(numero)


# ------------------------------------------------------------
# TAB BAR
# ------------------------------------------------------------

open_tabs = st.session_state.lr_open_tabs

with st.container(key="tab_bar_row"):
    # Flattened layout: 1 for Home + 2 for each opened tab + 1 spacer at the end
    total_elements = 1 + (len(open_tabs) * 2)
    tab_cols = st.columns([1] * total_elements + [10])

    # 1. Home Tab
    with tab_cols[0]:
        st.button(
            "Liste des rapports",
            key="tab_liste_btn",
            type="primary" if st.session_state.lr_active_tab == "liste" else "secondary",
            on_click=_activate_tab,
            args=("liste",),
        )

    # 2. Dynamic Tabs
    col_index = 1
    for key in open_tabs:
        is_active = (st.session_state.lr_active_tab == key)

        # Label
        with tab_cols[col_index]:
            st.button(
                REPORT_TABS[key]["label"],
                key=f"tab_{key}_btn",
                type="primary" if is_active else "secondary",
                on_click=_activate_tab,
                args=(key,),
            )
        col_index += 1

        # Close Button
        with tab_cols[col_index]:
            st.button(
                "✖",
                key=f"tab_{key}_close_btn",
                type="primary" if is_active else "secondary", 
                on_click=_close_tab,
                args=(key,),
            )
        col_index += 1

st.divider()


# ============================================================
# TAB CONTENT 
# ============================================================

if st.session_state.lr_active_tab in REPORT_TABS:

    REPORT_TABS[st.session_state.lr_active_tab]["render"]()

else:

    # ---------------- SEARCH / FILTER / SORT ROW ----------------

    reports = get_reports_catalog()
    favorites = get_favorites()

    search_col, filt_col, sort_label_col, sort_col = st.columns([6, 1.3, 0.9, 1.7])

    with search_col:
        search_query = st.text_input(
            "Recherche",
            placeholder="🔍  Rechercher un rapport par nom, numéro ou mot-clé...",
            label_visibility="collapsed",
            key="report_search"
        )

    with filt_col:
        with st.popover("▽  Filtres", use_container_width=True):
            selected_categories = st.multiselect(
                "Catégorie",
                sorted(reports["categorie"].unique()),
                key="category_filter"
            )

    with sort_label_col:
        st.markdown('<div style="padding-top:8px; font-size:13px; color:#6E6A63;">Trier par</div>', unsafe_allow_html=True)

    with sort_col:
        sort_option = st.selectbox(
            "Trier par",
            ["Nom (A-Z)", "Nom (Z-A)", "Dernière modif.", "Favoris en premier"],
            label_visibility="collapsed", key="sort_select"
        )

    st.markdown('<div style="height:22px;"></div>', unsafe_allow_html=True)

    # ---------------- APPLY SEARCH / FILTER / SORT ----------------

    filtered_reports = reports.copy()

    if search_query:
        q = search_query.strip().lower()
        mask = (
            filtered_reports["titre"].str.lower().str.contains(q)
            | filtered_reports["desc"].str.lower().str.contains(q)
            | filtered_reports["numero"].astype(str).str.contains(q)
        )
        filtered_reports = filtered_reports[mask]

    if selected_categories:
        filtered_reports = filtered_reports[filtered_reports["categorie"].isin(selected_categories)]

    if sort_option == "Nom (A-Z)":
        filtered_reports = filtered_reports.sort_values("titre")
    elif sort_option == "Nom (Z-A)":
        filtered_reports = filtered_reports.sort_values("titre", ascending=False)
    elif sort_option == "Dernière modif.":
        filtered_reports = filtered_reports.assign(
            _maj_sort=pd.to_datetime(filtered_reports["maj"], format="%d/%m/%Y")
        ).sort_values("_maj_sort", ascending=False)
    elif sort_option == "Favoris en premier":
        filtered_reports = filtered_reports.assign(
            _is_fav=filtered_reports["numero"].isin(favorites)
        ).sort_values("_is_fav", ascending=False)

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

    # ---------------- LAYOUT: REPERTOIRES + CARD GRID ----------------

    left_col, right_col = st.columns([1.15, 3.4], gap="medium")

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

    with right_col:

        if filtered_reports.empty:

            st.info("Aucun rapport ne correspond à votre recherche.")

        else:

            reports_list = filtered_reports.to_dict("records")

            for row_start in range(0, len(reports_list), 2):
                pair = reports_list[row_start:row_start + 2]
                card_cols = st.columns(2, gap="medium")

                for card_col, r in zip(card_cols, pair):
                    with card_col:
                        with st.container(border=True):

                            is_favori = r["numero"] in favorites
                            star_icon = "⭐" if is_favori else "☆"

                            top_l, top_r = st.columns([1, 5])
                            with top_l:
                                st.button(
                                    star_icon,
                                    key=f"fav_btn_{r['numero']}",
                                    on_click=_toggle_favorite,
                                    args=(r["numero"],),
                                )
                            with top_r:
                                st.markdown(
                                    f'<div class="rc-kebab" style="text-align:right;">{ICON_KEBAB}</div>',
                                    unsafe_allow_html=True,
                                )

                            if pd.notna(r["key"]):
                                st.button(
                                    r["titre"],
                                    key=f"open_{r['key']}_title_btn",
                                    on_click=_open_tab,
                                    args=(r["key"],),
                                )
                            else:
                                st.markdown(
                                    f'<div class="rc-card-title">{r["titre"]}</div>',
                                    unsafe_allow_html=True,
                                )

                            st.markdown(
                                f'<div class="rc-card-meta">N° {r["numero"]} · {r["dossier"]}</div>',
                                unsafe_allow_html=True,
                            )

                            st.markdown('<div class="rc-card-footer-divider"></div>', unsafe_allow_html=True)

                            foot_l, foot_r = st.columns(2)
                            with foot_l:
                                st.markdown(
                                    '<div class="rc-card-footer-label">Dernière modif.</div>',
                                    unsafe_allow_html=True,
                                )
                            with foot_r:
                                st.markdown(
                                    f'<div class="rc-card-footer-label" style="text-align:right;">{r["maj"]}</div>',
                                    unsafe_allow_html=True,
                                )

                st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)

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
                """
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