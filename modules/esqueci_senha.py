import streamlit as st
import yagmail
from utils.persistencia import gerar_token_reset, atualizar_senha_por_token, validar_token_reset

def show_forgot_password_screen():
    st.title("Recuperação de Senha")
    st.write("Informe seu e-mail cadastrado para receber um link de redefinição de senha.")
    with st.form("forgot_password_form"):
        email = st.text_input("E-mail")
        submitted = st.form_submit_button("Enviar link de redefinição")
        if submitted:
            if not email:
                st.warning("Preencha o campo de e-mail.")
            else:
                token = gerar_token_reset(email)
                if token:
                    reset_link = f"http://localhost:8501/?page=reset_senha&token={token}"
                    try:
                        yag = yagmail.SMTP('seu_email@gmail.com', 'sua_senha_app')
                        yag.send(email, 'Redefinição de senha - Plataforma AgroCarbon',
                            f"Clique no link para redefinir sua senha: {reset_link}")
                        st.success("E-mail de redefinição enviado! Verifique sua caixa de entrada.")
                    except Exception as e:
                        st.error(f"Erro ao enviar e-mail: {e}")
                else:
                    st.error("E-mail não encontrado.")

def show_reset_password_screen(token):
    st.title("Redefinir Senha")
    user_id = validar_token_reset(token)
    if not user_id:
        st.error("Token inválido ou expirado.")
        return
    with st.form("reset_password_form"):
        new_password = st.text_input("Nova senha", type="password")
        confirm_password = st.text_input("Confirme a nova senha", type="password")
        submitted = st.form_submit_button("Redefinir senha")
        if submitted:
            if not new_password or not confirm_password:
                st.warning("Preencha todos os campos.")
            elif new_password != confirm_password:
                st.warning("As senhas não coincidem.")
            else:
                if atualizar_senha_por_token(token, new_password):
                    st.success("Senha redefinida com sucesso! Faça login com sua nova senha.")
                else:
                    st.error("Erro ao redefinir senha. Tente novamente.")
