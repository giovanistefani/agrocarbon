import streamlit as st
from pages.home import show_home_screen
from pages.produtores import show_produtor_screen
from pages.usuarios import show_register_screen
from pages.propriedades import show_propriedades_screen
from utils.persistencia import hash_password, carregar_usuarios

# --- Lógica de Controle de Acesso ---
def show_login_screen():
    st.set_page_config(page_title="Login", layout="centered")
    st.title("Login - Plataforma AgroCarbon")

    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            # Primeiro tenta autenticar como admin (secrets.toml)
            if username == st.secrets["credentials"]["username"] and password == st.secrets["credentials"]["password"]:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()
            else:
                # Tenta autenticar como usuário cadastrado
                usuarios = carregar_usuarios()
                if not usuarios.empty and username in usuarios['username'].values:
                    hash_senha = hash_password(password)
                    user_row = usuarios[usuarios['username'] == username]
                    if user_row.iloc[0]['password_hash'] == hash_senha:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.rerun()
                st.error("Usuário ou senha incorretos.")

def show_main_app():
    st.set_page_config(
        page_title="Cadastro de Propriedades Rurais",
        page_icon="🚜",
        layout="wide"
    )

    with st.sidebar:
        st.write(f"Bem-vindo, **{st.session_state.get('username', 'usuário')}**!")
        is_admin = st.session_state.get('username', None) == st.secrets["credentials"]["username"]
        menu_option = st.session_state.get('menu_option', 'Início')
        if st.button("Início"):
            st.session_state.menu_option = "Início"
            st.rerun()
        if st.button("Cadastro de Propriedades"):
            st.session_state.menu_option = "Cadastro de Propriedades"
            st.rerun()
        if is_admin:
            if st.button("Cadastrar novo usuário"):
                st.session_state.menu_option = "Cadastrar novo usuário"
                st.rerun()
            if st.button("Cadastro de Produtores"):
                st.session_state.menu_option = "Cadastro de Produtores"
                st.rerun()
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.menu_option = 'Início'
            st.rerun()

    menu = st.session_state.get('menu_option', 'Início')

    if menu == "Cadastrar novo usuário" and is_admin:
        show_register_screen()
        return
    elif menu == "Cadastro de Produtores" and is_admin:
        show_produtor_screen()
        return
    elif menu == "Cadastro de Propriedades":
        show_propriedades_screen()
        return
    elif menu == "Início":
        show_home_screen()
        return

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

if st.session_state.authenticated:
    show_main_app()
else:
    show_login_screen()