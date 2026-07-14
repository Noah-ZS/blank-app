import streamlit as st
from common import render_topbar
from report_views import render_commandes_detail_view

render_topbar("Version Production 5.2.1")

st.markdown(
    '<div class="page-title font-serif" style="font-size:28px; margin-bottom:18px;">'
    'Commandes - Détail</div>',
    unsafe_allow_html=True
)

render_commandes_detail_view()