import streamlit as st
from utils.persistencia import adicionar_usuario, listar_usuarios_df, editar_usuario, excluir_usuario
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
    st.write("---")
    st.subheader("Usuários cadastrados")
    df_usuarios = listar_usuarios_df()
    if not df_usuarios.empty:
        for idx, row in df_usuarios.iterrows():
            col1, col2, col3 = st.columns([4, 4, 2])
            with col1:
                st.write(f"**Usuário:** {row['username']}")
                st.write(f"**E-mail:** {row['email']}")
            with col2:
                if st.button("Editar", key=f"edit_{row['id']}"):
                    st.session_state['edit_user_id'] = row['id']
            with col3:
                if st.button("Excluir", key=f"del_{row['id']}"):
                    excluir_usuario(row['id'])
                    st.success("Usuário excluído com sucesso!")
                    st.rerun()
        # Formulário de edição
        if 'edit_user_id' in st.session_state:
            user_id = st.session_state['edit_user_id']
            user_row = df_usuarios[df_usuarios['id'] == user_id].iloc[0]
            st.subheader("Editar Usuário")
            with st.form("edit_user_form"):
                new_username = st.text_input("Novo usuário", value=user_row['username'])
                new_email = st.text_input("Novo e-mail", value=user_row['email'])
                submitted_edit = st.form_submit_button("Salvar alterações")
                if submitted_edit:
                    editar_usuario(user_id, new_username, new_email)
                    st.success("Usuário atualizado com sucesso!")
                    del st.session_state['edit_user_id']
                    st.rerun()
    else:
        st.info("Nenhum usuário cadastrado ainda.")
