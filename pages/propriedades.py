import streamlit as st
from utils.persistencia import carregar_dados, salvar_dados, carregar_produtores
import pandas as pd

def show_propriedades_screen():
    st.title("🚜 Plataforma AgroCarbon - Cadastro de Propriedades")
    st.markdown("---")

    # Carrega os dados existentes
    df_propriedades = carregar_dados()

    # --- Formulário de Cadastro ---
    st.header("Adicionar Nova Propriedade")

    produtores = carregar_produtores()
    produtores_nomes = produtores['Nome'].tolist() if not produtores.empty else []

    if not produtores_nomes:
        st.warning("Cadastre pelo menos um produtor antes de cadastrar propriedades.")
    else:
        with st.form("cadastro_form", clear_on_submit=True):
            nome_propriedade = st.text_input("Nome da Propriedade")
            nome_proprietario = st.selectbox("Proprietário(a)", produtores_nomes)
            municipio = st.text_input("Município")

            # Lista de Unidades Federativas (UFs) do Brasil
            ufs = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
            uf_selecionada = st.selectbox("UF", ufs)

            area_ha = st.number_input("Área (ha)", min_value=0.0, format="%.2f")

            # Botão de envio do formulário
            submitted = st.form_submit_button("Cadastrar Propriedade")

            if submitted:
                if not nome_propriedade or not nome_proprietario or not municipio:
                    st.warning("Por favor, preencha todos os campos obrigatórios.")
                else:
                    nova_propriedade = pd.DataFrame([{
                        'Nome da Propriedade': nome_propriedade,
                        'Proprietário(a)': nome_proprietario,
                        'Município': municipio,
                        'UF': uf_selecionada,
                        'Área (ha)': area_ha
                    }])
                    df_propriedades = pd.concat([df_propriedades, nova_propriedade], ignore_index=True)
                    salvar_dados(df_propriedades)
                    st.success("Propriedade cadastrada com sucesso!")

    # --- Exibição dos Dados ---
    st.markdown("---")
    st.header("Propriedades Cadastradas")

    if df_propriedades.empty:
        st.info("Nenhuma propriedade foi cadastrada ainda.")
    else:
        st.dataframe(df_propriedades, use_container_width=True)
