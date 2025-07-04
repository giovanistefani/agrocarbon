import streamlit as st
from utils.persistencia import hash_password, carregar_usuarios, get_user_id_by_username
from modules.cadastro_usuario import show_register_screen
from modules.esqueci_senha import show_forgot_password_screen, show_reset_password_screen
from modules.cadastro_produtor import show_produtor_screen
from modules.cadastro_propriedade import show_propriedades_screen

# --- Telas do app ---
def show_home_screen():
    st.title("Bem-vindo à Plataforma Terra que Vale")
    st.write("Escolha uma opção no menu à esquerda.")

# --- Lógica de Controle de Acesso ---
def show_login_screen():
    st.set_page_config(page_title="Login", layout="centered", initial_sidebar_state="collapsed")
    st.sidebar.empty()
    st.markdown("""
        <div style='text-align: center;'>
            <h1>🌱 Plataforma Terra que Vale</h1>
            <h3>Bem-vindo! Faça login para acessar o sistema.</h3>
        </div>
        <br>
    """, unsafe_allow_html=True)
    query_params = st.query_params
    if query_params.get("page", [None])[0] == "reset_senha" and "token" in query_params:
        show_reset_password_screen(query_params["token"][0])
        return
    if st.session_state.get('show_forgot', False):
        show_forgot_password_screen()
        if st.button("Voltar para o login"):
            st.session_state.show_forgot = False
            st.rerun()
        return
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")
        if submitted:
            # Autenticação admin (ajuste conforme seu uso de secrets)
            if "credentials" in st.secrets and username == st.secrets["credentials"]["username"] and password == st.secrets["credentials"]["password"]:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()
            else:
                usuarios = carregar_usuarios()
                if not usuarios.empty and username in usuarios['username'].values:
                    hash_senha = hash_password(password)
                    user_row = usuarios[usuarios['username'] == username]
                    if user_row.iloc[0]['password_hash'] == hash_senha:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.user_id = get_user_id_by_username(username)
                        st.rerun()
                st.error("Usuário ou senha incorretos.")
    if st.button("Esqueci minha senha?"):
        st.session_state.show_forgot = True
        st.rerun()

def show_main_app():
    st.set_page_config(page_title="Cadastro de Propriedades Rurais", page_icon="🚜", layout="wide")
    with st.sidebar:
        st.write(f"Bem-vindo, **{st.session_state.get('username', 'usuário')}**!")
        is_admin = "credentials" in st.secrets and st.session_state.get('username', None) == st.secrets["credentials"]["username"]
        menu_option = st.session_state.get('menu_option', 'Início')
        if st.button("Início"):
            st.session_state.menu_option = "Início"
            st.rerun()
        if st.button("Cadastrar novo usuário"):
            st.session_state.menu_option = "Cadastrar novo usuário"
            st.rerun()
        if st.button("Cadastro de Produtores"):
            st.session_state.menu_option = "Cadastro de Produtores"
            st.rerun()
        if is_admin:
            if st.button("Cadastro de Propriedades"):
                st.session_state.menu_option = "Cadastro de Propriedades"
                st.rerun()
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.menu_option = 'Início'
            st.rerun()
    menu = st.session_state.get('menu_option', 'Início')
    if menu == "Cadastrar novo usuário":
        show_register_screen()
    elif menu == "Cadastro de Produtores":
        show_produtor_screen()
    elif menu == "Cadastro de Propriedades" and is_admin:
        show_propriedades_screen()
    elif menu == "Início":
        show_home_screen()

# --- Inicialização do estado ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

# --- Execução principal ---
if st.session_state.authenticated:
    show_main_app()
else:
    show_login_screen()