import streamlit as st

def show_home_screen():
    """Exibe a tela inicial do sistema."""
    st.title("🌱 AgroCarbon")
    st.markdown("""
    <div style='text-align: center; font-size: 1.2em;'>
        Bem-vindo à plataforma AgroCarbon!<br>
        Utilize o menu ao lado para acessar as funcionalidades.
    </div>
    """, unsafe_allow_html=True)
