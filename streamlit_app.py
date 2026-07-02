import streamlit as st
import pandas as pd

# --------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------

st.set_page_config(
    page_title="Infocentre",
    layout="wide"
)

st.title("Infocentre")

# --------------------------------------------------------
# SAMPLE DATABASE
# --------------------------------------------------------

if "df" not in st.session_state:

    st.session_state.df = pd.DataFrame({
        "Métier": [
            "M","M","M","TEXTILE","TEXTILE","CHAUSSURES"
        ],

        "Code SKU": [
            "000091MR00",
            "000099MR00",
            "000109MR00",
            "TX0001",
            "TX0002",
            "SH0001"
        ],

        "Réf Article":[
            "000091MR",
            "000099MR",
            "000109MR",
            "TX0001",
            "TX0002",
            "SH0001"
        ],

        "Code Coloris":[
            "00",
            "01",
            "02",
            "BL",
            "BK",
            "WH"
        ],

        "Libellé Article":[
            "Réparation non référencée",
            "Réparation Art de vivre",
            "Remplacement Baleine",
            "Chemise Oxford",
            "Pantalon Chino",
            "Sneakers"
        ],

        "Libellé Coloris":[
            "Noir",
            "Rouge",
            "Bleu",
            "Blanc",
            "Noir",
            "Blanc"
        ],

        "Famille":[
            "SAV",
            "SAV",
            "SAV",
            "Homme",
            "Homme",
            "Chaussures"
        ],

        "Supply Chain":[
            "A DEFINIR",
            "Collection",
            "Collection",
            "Stock",
            "Stock",
            "Collection"
        ],

        "Produit":[
            "M981",
            "M981",
            "M981",
            "TX100",
            "TX200",
            "SH100"
        ],

        "Statut":[
            "Actif",
            "Actif",
            "Inactif",
            "Actif",
            "Actif",
            "Inactif"
        ]
    })

if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = st.session_state.df.copy()

df = st.session_state.df

# --------------------------------------------------------
# TOP NAVIGATION
# --------------------------------------------------------

tabs = st.tabs([
    "Menu",
    "Liste des rapports",
    "Article - Emballage",
    "Article - Liste des Coloris / Taille",
    "Article - Fournisseur"
])

with tabs[3]:

    # ----------------------------------------------------
    # REPORT HEADER
    # ----------------------------------------------------

    c1, c2, c3 = st.columns([5,1,1])

    with c1:
        st.text_input(
            "Rapport",
            value="Rapport n°646 : Article - Liste des Coloris / Taille",
            disabled=True
        )

    with c2:
        st.selectbox(
            "Vue",
            ["Initiale"]
        )

    with c3:
        st.write("")
        st.button("Modification")

    st.subheader("Liste des articles - Coloris - Taille")

    general_tab, coloris_tab = st.tabs([
        "Général",
        "Coloris"
    ])

    # ====================================================
    # GENERAL TAB
    # ====================================================

    with general_tab:

        left, middle, right = st.columns(3)

        # ---------------- LEFT -----------------

        with left:

            metier = st.selectbox(
                "Métier",
                ["Tous"] + sorted(df["Métier"].unique())
            )

            code_coloris = st.text_input(
                "Code Coloris"
            )

            code_matiere = st.text_input(
                "Code Matière"
            )

            supply = st.selectbox(
                "Supply Chain",
                ["Tous"] + sorted(df["Supply Chain"].unique())
            )

        # ---------------- MIDDLE ----------------

        with middle:

            sku = st.text_input(
                "Code SKU"
            )

            libelle_article = st.text_input(
                "Libellé Article"
            )

            famille = st.text_input(
                "Famille"
            )

        # ---------------- RIGHT ----------------

        with right:

            libelle_coloris = st.text_input(
                "Libellé Coloris"
            )

            statut = st.radio(
                "Statut",
                [
                    "Tous",
                    "Actif",
                    "Inactif"
                ]
            )

            podium = st.checkbox("Pod-New")

            nouveaute = st.checkbox("Nouveauté SKU")

            produit = st.text_input(
                "Produit"
            )

    with coloris_tab:
        st.info("Onglet Coloris")

    st.divider()

    # ====================================================
    # FILTER FUNCTION
    # ====================================================

    def apply_filters(data):

        filtered = data.copy()

        if metier != "Tous":
            filtered = filtered[
                filtered["Métier"] == metier
            ]

        if code_coloris:
            filtered = filtered[
                filtered["Code Coloris"]
                .str.contains(code_coloris, case=False)
            ]

        if sku:
            filtered = filtered[
                filtered["Code SKU"]
                .str.contains(sku, case=False)
            ]

        if libelle_article:
            filtered = filtered[
                filtered["Libellé Article"]
                .str.contains(libelle_article, case=False)
            ]

        if libelle_coloris:
            filtered = filtered[
                filtered["Libellé Coloris"]
                .str.contains(libelle_coloris, case=False)
            ]

        if famille:
            filtered = filtered[
                filtered["Famille"]
                .str.contains(famille, case=False)
            ]

        if produit:
            filtered = filtered[
                filtered["Produit"]
                .str.contains(produit, case=False)
            ]

        if supply != "Tous":
            filtered = filtered[
                filtered["Supply Chain"] == supply
            ]

        if statut != "Tous":
            filtered = filtered[
                filtered["Statut"] == statut
            ]

        return filtered

    # ====================================================
    # BUTTONS
    # ====================================================

    b1, b2, b3, b4 = st.columns(4)

    with b1:

        if st.button("Afficher"):

            st.session_state.filtered_df = apply_filters(df)

    with b2:

        if st.button("Réinitialiser"):

            st.session_state.filtered_df = df.copy()

    with b3:

        st.button("Exporter")

    with b4:

        st.button("Sauvegarder la vue")

    st.divider()

    # ====================================================
    # TABLE
    # ====================================================

    st.data_editor(
        st.session_state.filtered_df,
        use_container_width=True,
        hide_index=True,
        height=500
    )

    st.divider()

left, right = st.columns([3,1])

with left:
    global_search = st.text_input(
        "🔍 Recherche globale",
        placeholder="Search in every column..."
    )

with right:
    st.metric(
        "Résultats",
        len(st.session_state.filtered_df)
    )


    display_df = st.session_state.filtered_df.copy()

if global_search:

    mask = display_df.astype(str).apply(
        lambda col: col.str.contains(
            global_search,
            case=False,
            na=False
        )
    ).any(axis=1)

    display_df = display_df[mask]



    visible_columns = st.multiselect(
    "Colonnes visibles",
    display_df.columns.tolist(),
    default=display_df.columns.tolist()
)

display_df = display_df[visible_columns]



c1, c2 = st.columns(2)

with c1:

    sort_column = st.selectbox(
        "Trier par",
        ["Aucun"] + display_df.columns.tolist()
    )

with c2:

    sort_order = st.radio(
        "Ordre",
        ["Ascendant", "Descendant"],
        horizontal=True
    )

if sort_column != "Aucun":

    display_df = display_df.sort_values(
        by=sort_column,
        ascending=sort_order == "Ascendant"
    )


    ROWS_PER_PAGE = 20

total_rows = len(display_df)

pages = max(1, (total_rows - 1)//ROWS_PER_PAGE + 1)

page = st.number_input(
    "Page",
    min_value=1,
    max_value=pages,
    value=1
)

start = (page-1)*ROWS_PER_PAGE
end = start + ROWS_PER_PAGE

display_df = display_df.iloc[start:end]


def build_sql():

    where = []

    if metier != "Tous":
        where.append(f"Metier='{metier}'")

    if sku:
        where.append(f"CodeSKU LIKE '%{sku}%'")

    if code_coloris:
        where.append(f"CodeColoris LIKE '%{code_coloris}%'")

    if libelle_article:
        where.append(
            f"LibelleArticle LIKE '%{libelle_article}%'"
        )

    sql = "SELECT * FROM Articles"

    if where:
        sql += "\nWHERE " + "\nAND ".join(where)

    return sql


with st.expander("Afficher la requête SQL"):

    st.code(
        build_sql(),
        language="sql"
    )

    from io import BytesIO

buffer = BytesIO()

with pd.ExcelWriter(buffer) as writer:
    display_df.to_excel(writer, index=False)

st.download_button(
    "📥 Export Excel",
    data=buffer.getvalue(),
    file_name="articles.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.data_editor(
    display_df,
    hide_index=True,
    use_container_width=True,
    height=550
)