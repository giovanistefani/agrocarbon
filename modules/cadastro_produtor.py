import streamlit as st
from utils.persistencia import adicionar_produtor

ESTADOS_BR = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]

def show_produtor_screen():
    st.title("Cadastro de Produtores")
    st.write("Preencha os dados do produtor abaixo:")
    with st.form("cadastro_produtor_form"):
        nome = st.text_input("Nome do Produtor")
        documento = st.text_input("CPF ou CNPJ")
        rua = st.text_input("Rua")
        numero = st.text_input("Número")
        complemento = st.text_input("Complemento")
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        estado = st.selectbox("Estado", ESTADOS_BR)
        cep = st.text_input("CEP")
        submitted = st.form_submit_button("Cadastrar Produtor")
        if submitted:
            if not nome or not documento or not rua or not numero or not bairro or not cidade or not estado or not cep:
                st.warning("Preencha todos os campos obrigatórios.")
            else:
                try:
                    user_id = st.session_state.get('user_id')
                    adicionar_produtor(nome, documento, rua, numero, complemento, bairro, cidade, estado, cep, user_id)
                    st.success(f"Produtor '{nome}' cadastrado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao cadastrar produtor: {e}")
