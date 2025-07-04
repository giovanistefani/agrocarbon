import streamlit as st
from utils.persistencia import adicionar_usuario
import yagmail

def show_register_screen():
    st.title("Cadastro de Novo Usuário")
    with st.form("cadastro_usuario_form"):
        username = st.text_input("Usuário")
        email = st.text_input("E-mail")
        password = st.text_input("Senha", type="password")
        confirm_password = st.text_input("Confirme a senha", type="password")
        submitted = st.form_submit_button("Cadastrar")
        if submitted:
            if not username or not password or not email:
                st.warning("Preencha todos os campos.")
            elif password != confirm_password:
                st.warning("As senhas não coincidem.")
            else:
                try:
                    adicionar_usuario(username, password, email)
                    st.success(f"Usuário '{username}' cadastrado com sucesso!")
                    # Envia e-mail de boas-vindas
                    try:
                        yag = yagmail.SMTP('seu_email@gmail.com', 'sua_senha_app')
                        yag.send(email, 'Bem-vindo à Plataforma AgroCarbon', f"Olá {username}, seu cadastro foi realizado com sucesso!")
                    except Exception as e:
                        st.warning(f"Não foi possível enviar o e-mail: {e}")
                except Exception as e:
                    st.error(f"Erro ao cadastrar usuário: {e}")
