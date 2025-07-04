import streamlit as st
from utils.persistencia import adicionar_propriedade_com_produtores, listar_propriedades, listar_propriedades_com_produtores, listar_produtores_simples, editar_propriedade, excluir_propriedade, buscar_produtores_por_propriedade, atualizar_vinculos_propriedade_produtor

ESTADOS_BR = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]

def show_propriedades_screen():
    st.title("Cadastro de Propriedades")
    st.write("Preencha os dados da propriedade abaixo:")
    produtores = listar_produtores_simples()
    opcoes_produtores = {f"{p[1]} (id {p[0]})": p[0] for p in produtores}
    if not opcoes_produtores:
        st.warning("Cadastre pelo menos um produtor antes de cadastrar propriedades.")
        st.stop()
    with st.form("cadastro_propriedade_form"):
        nome = st.text_input("Nome da Propriedade")
        rua = st.text_input("Rua")
        numero = st.text_input("Número")
        complemento = st.text_input("Complemento")
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        estado = st.selectbox("Estado", ESTADOS_BR)
        cep = st.text_input("CEP")
        tamanho = st.number_input("Tamanho (hectares)", min_value=0.0, step=0.01)
        latitude = st.text_input("Latitude")
        longitude = st.text_input("Longitude")
        produtores_selecionados = st.multiselect("Produtores vinculados", list(opcoes_produtores.keys()))
        submitted = st.form_submit_button("Cadastrar Propriedade")
        if submitted:
            if not nome or not rua or not numero or not bairro or not cidade or not estado or not cep or not tamanho or not latitude or not longitude or not produtores_selecionados:
                st.warning("Preencha todos os campos obrigatórios.")
            else:
                try:
                    produtores_ids = [opcoes_produtores[p] for p in produtores_selecionados]
                    adicionar_propriedade_com_produtores(nome, rua, numero, complemento, bairro, cidade, estado, cep, tamanho, latitude, longitude, produtores_ids)
                    st.success(f"Propriedade '{nome}' cadastrada com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao cadastrar propriedade: {e}")
    st.write("---")
    st.subheader("Propriedades cadastradas")
    df_propriedades = listar_propriedades_com_produtores()
    if not df_propriedades.empty:
        for idx, row in df_propriedades.iterrows():
            col1, col2, col3 = st.columns([4, 4, 2])
            with col1:
                st.write(f"**Nome:** {row['nome']}")
                st.write(f"**Cidade:** {row['cidade']} - {row['estado']}")
                st.write(f"**Tamanho:** {row['tamanho']} ha")
            with col2:
                if st.button("Editar", key=f"edit_prop_{row['id']}"):
                    st.session_state['edit_prop_id'] = row['id']
            with col3:
                if st.button("Excluir", key=f"del_prop_{row['id']}"):
                    excluir_propriedade(row['id'])
                    st.success("Propriedade excluída com sucesso!")
                    st.rerun()
        # Formulário de edição
        if 'edit_prop_id' in st.session_state:
            prop_id = st.session_state['edit_prop_id']
            # Busca dados completos da propriedade
            df_prop_full = listar_propriedades()
            prop_row = df_prop_full[df_prop_full['id'] == prop_id].iloc[0]
            st.subheader("Editar Propriedade")
            produtores_ids_vinculados = buscar_produtores_por_propriedade(prop_id)
            produtores_selecionados_edit = [k for k, v in opcoes_produtores.items() if v in produtores_ids_vinculados]
            with st.form("edit_prop_form"):
                new_nome = st.text_input("Nome da Propriedade", value=prop_row['nome'])
                new_rua = st.text_input("Rua", value=prop_row['rua'])
                new_numero = st.text_input("Número", value=prop_row['numero'])
                new_complemento = st.text_input("Complemento", value=prop_row['complemento'])
                new_bairro = st.text_input("Bairro", value=prop_row['bairro'])
                new_cidade = st.text_input("Cidade", value=prop_row['cidade'])
                new_estado = st.selectbox("Estado", ESTADOS_BR, index=ESTADOS_BR.index(prop_row['estado']))
                new_cep = st.text_input("CEP", value=prop_row['cep'])
                new_tamanho = st.number_input("Tamanho (hectares)", min_value=0.0, step=0.01, value=float(prop_row['tamanho']))
                new_latitude = st.text_input("Latitude", value=prop_row['latitude'])
                new_longitude = st.text_input("Longitude", value=prop_row['longitude'])
                new_produtores = st.multiselect("Produtores vinculados", list(opcoes_produtores.keys()), default=produtores_selecionados_edit)
                submitted_edit = st.form_submit_button("Salvar alterações")
                if submitted_edit:
                    editar_propriedade(prop_id, new_nome, new_rua, new_numero, new_complemento, new_bairro, new_cidade, new_estado, new_cep, new_tamanho, new_latitude, new_longitude)
                    produtores_ids = [opcoes_produtores[p] for p in new_produtores]
                    atualizar_vinculos_propriedade_produtor(prop_id, produtores_ids)
                    st.success("Propriedade atualizada com sucesso!")
                    del st.session_state['edit_prop_id']
                    st.rerun()
    else:
        st.info("Nenhuma propriedade cadastrada ainda.")
