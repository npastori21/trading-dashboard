import streamlit as st

chain_page = st.Page('pages/chain.py', title='Options Chain', icon='📊')
home_page = st.Page('pages/home.py', title='Home', icon='🏠')
strangle_page = st.Page('pages/strangle.py', title='Strangle Visualizer', icon='🏦')
usage_page = st.Page('pages/usage.py', title='Usage', icon='🧠')
education_page = st.Page('pages/education.py', title='Education', icon='📘')
payment_page = st.Page('pages/payments.py', title='Subscriptions', icon='💼')

pg = st.navigation([home_page, chain_page, strangle_page, education_page, usage_page, payment_page])

pg.run()
