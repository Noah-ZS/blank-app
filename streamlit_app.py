import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Infocentre",
    layout="wide",
)

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

st.title("Infocentre")

# -------------------------------------------------------
# TOP NAVIGATION
# -------------------------------------------------------

tabs = st.tabs([
    "Menu",
    "Liste des rapports",
    "Article - Emballage",
    "Article - Liste des Coloris / Taille",
    "Article - Fournisseur",
])

with tabs[3]:

    # -------------------------------------------------------
    # REPORT HEADER
    # -------------------------------------------------------

    c1, c2, c3 = st.columns([4,1,2])

    with c1:
        st.text_input(
            "Rapport",
            value="Rapport n°646 : Article - Liste des Coloris / Taille",
            disabled=True
        )

    with c2:
        st.selectbox(
            "Vue",
            ["Initiale"],
        )

    with c3:
        st.write("")
        st.write("")
        st.button("Modification", use_container_width=True)

    st.markdown(
        "<h3 style='text-align:center'>Liste des articles - Coloris - Taille</h3>",
        unsafe_allow_html=True,
    )

    # -------------------------------------------------------
    # GENERAL / COLORIS
    # -------------------------------------------------------

    general_tab, coloris_tab = st.tabs(["Général", "Coloris"])

    with general_tab:

        left, middle, right = st.columns([3,3,3])

        # ---------------- LEFT ----------------

        with left:

            st.selectbox(
                "Métier",
                [
                    "M - ART DE VIVRE",
                    "TEXTILE",
                    "CHAUSSURES"
                ]
            )

            st.text_input("Code Coloris")

            st.text_input("Code Matière Principale")

            st.selectbox(
                "Modèle Supply Chain",
                [
                    "Tous",
                    "A DEFINIR",
                    "Collection",
                ]
            )

        # ---------------- MIDDLE ----------------

        with middle:

            st.text_input("Code Article (SKU)")

            st.text_input("Libellé Coloris")

            st.text_input("Famille")

        # ---------------- RIGHT ----------------

        with right:

            st.text_input("Libellé Article")

            st.radio(
                "Statut Article-Coloris",
                ["Actif", "Inactif"],
                horizontal=True,
            )

            st.columns(2)

            c1, c2 = st.columns(2)

            with c1:
                st.checkbox("Pod-New (O/N)")

            with c2:
                st.checkbox("Nouveauté SKU (O/N)")

            st.text_input("Code Podium")

    with coloris_tab:
        st.info("Coloris tab interface goes here.")

    st.divider()

    # -------------------------------------------------------
    # TOOLBAR
    # -------------------------------------------------------

    b1, b2, b3, b4 = st.columns([1.6,1,1,1.5])

    with b1:
        st.button("Afficher la requête SQL", use_container_width=True)

    with b2:
        st.button("Afficher", type="primary", use_container_width=True)

    with b3:
        st.button("Exporter", use_container_width=True)

    with b4:
        st.button("Sauvegarder la vue", use_container_width=True)

    st.divider()

    # -------------------------------------------------------
    # GRID TOOLBAR
    # -------------------------------------------------------

    g1, g2, g3 = st.columns(3)

    g1.button("Trier", use_container_width=True)
    g2.button("Filtrer", use_container_width=True)
    g3.button("Personnaliser", use_container_width=True)

    st.divider()

    # -------------------------------------------------------
    # SAMPLE TABLE
    # -------------------------------------------------------

    data = pd.DataFrame(
        {
            "Métier": ["M", "M", "M"],
            "Code SKU": [
                "000091MR00",
                "000099MR00",
                "000109MR00",
            ],
            "Réf Article": [
                "000091MR",
                "000099MR",
                "000109MR",
            ],
            "Code Coloris": [
                "00",
                "00",
                "00",
            ],
            "Libellé Coloris": [
                "",
                "",
                "",
            ],
            "Libellé Français": [
                "REPARATION NON REFERENCEE",
                "REPARATION ART DE VIVRE",
                "REMPLACEMENT BALEINE",
            ],
            "Supply Chain": [
                "A DEFINIR",
                "A DEFINIR",
                "A DEFINIR",
            ],
            "Produit": [
                "M981",
                "M981",
                "M981",
            ],
        }
    )

    st.data_editor(
        data,
        use_container_width=True,
        hide_index=True,
        height=450,
    )