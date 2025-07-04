import streamlit as st
from utils.persistencia import carregar_usuarios, salvar_usuarios, hash_password
import pandas as pd

def show_register_screen():
    """Exibe a tela de cadastro de novo usuário (apenas para usuários autenticados)."""
    st.subheader("Cadastro de Novo Usuário")
    with st.form("register_form"):
        new_username = st.text_input("Novo usuário")
        new_password = st.text_input("Nova senha", type="password")
        confirm_password = st.text_input("Confirme a senha", type="password")
        submitted = st.form_submit_button("Cadastrar")

        if submitted:
            if not new_username or not new_password:
                st.warning("Preencha todos os campos.")
            elif new_password != confirm_password:
                st.warning("As senhas não coincidem.")
            else:
                usuarios = carregar_usuarios()
                if new_username in usuarios['username'].values:
                    st.error("Usuário já existe.")
                else:
                    novo_usuario = pd.DataFrame([{
                        'username': new_username,
                        'password_hash': hash_password(new_password)
                    }])
                    usuarios = pd.concat([usuarios, novo_usuario], ignore_index=True)
                    salvar_usuarios(usuarios)
                    st.success("Usuário cadastrado com sucesso!")
