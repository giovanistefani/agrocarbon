import streamlit as st
from utils.persistencia import carregar_produtores, salvar_produtores
import pandas as pd

def show_produtor_screen():
    """Exibe a tela de cadastro de produtores (apenas para admin)."""
    st.subheader("Cadastro de Produtores")
    df_produtores = carregar_produtores()

    with st.form("produtor_form", clear_on_submit=True):
        nome = st.text_input("Nome do Produtor")
        cpf_cnpj = st.text_input("CPF ou CNPJ")
        telefone = st.text_input("Telefone")
        email = st.text_input("E-mail")
        submitted = st.form_submit_button("Cadastrar Produtor")

        if submitted:
            if not nome or not cpf_cnpj:
                st.warning("Preencha pelo menos o nome e o CPF/CNPJ.")
            else:
                novo_produtor = pd.DataFrame([{
                    'Nome': nome,
                    'CPF/CNPJ': cpf_cnpj,
                    'Telefone': telefone,
                    'E-mail': email
                }])
                df_produtores = pd.concat([df_produtores, novo_produtor], ignore_index=True)
                salvar_produtores(df_produtores)
                st.success("Produtor cadastrado com sucesso!")

    st.markdown("---")
    st.header("Produtores Cadastrados")
    if df_produtores.empty:
        st.info("Nenhum produtor cadastrado ainda.")
    else:
        st.dataframe(df_produtores, use_container_width=True)
