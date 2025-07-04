import streamlit as st
from utils.persistencia import adicionar_produtor, listar_usuarios, listar_produtores, excluir_produtor, editar_produtor

ESTADOS_BR = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]

def show_produtor_screen():
    st.title("Cadastro de Produtores")
    st.write("Preencha os dados do produtor abaixo:")
    usuarios = listar_usuarios()
    opcoes_usuarios = {f"{u[1]} (id {u[0]})": u[0] for u in usuarios}

    # Edição
    editar_id = st.session_state.get('editar_produtor_id')
    editar_dados = None
    if editar_id:
        df = listar_produtores()
        row = df[df['id'] == editar_id]
        if not row.empty:
            editar_dados = row.iloc[0]

    with st.form("cadastro_produtor_form"):
        nome = st.text_input("Nome do Produtor", value=editar_dados['nome'] if editar_dados is not None else "")
        documento = st.text_input("CPF ou CNPJ", value=editar_dados['documento'] if editar_dados is not None else "")
        rua = st.text_input("Rua", value=editar_dados['rua'] if editar_dados is not None else "")
        numero = st.text_input("Número", value=editar_dados['numero'] if editar_dados is not None else "")
        complemento = st.text_input("Complemento", value=editar_dados['complemento'] if editar_dados is not None else "")
        bairro = st.text_input("Bairro", value=editar_dados['bairro'] if editar_dados is not None else "")
        cidade = st.text_input("Cidade", value=editar_dados['cidade'] if editar_dados is not None else "")
        estado = st.selectbox("Estado", ESTADOS_BR, index=ESTADOS_BR.index(editar_dados['estado']) if editar_dados is not None else 0)
        cep = st.text_input("CEP", value=editar_dados['cep'] if editar_dados is not None else "")
        usuario_selecionado = st.selectbox(
            "Usuário de acesso vinculado",
            list(opcoes_usuarios.keys()),
            index=list(opcoes_usuarios.values()).index(editar_dados['user_id']) if editar_dados is not None else 0
        ) if opcoes_usuarios else None
        if editar_id:
            submitted = st.form_submit_button("Salvar Alterações")
        else:
            submitted = st.form_submit_button("Cadastrar Produtor")
        if submitted:
            if not nome or not documento or not rua or not numero or not bairro or not cidade or not estado or not cep or not usuario_selecionado:
                st.warning("Preencha todos os campos obrigatórios.")
            else:
                try:
                    user_id = opcoes_usuarios[usuario_selecionado]
                    if editar_id:
                        editar_produtor(editar_id, nome, documento, rua, numero, complemento, bairro, cidade, estado, cep, user_id)
                        st.success(f"Produtor '{nome}' atualizado com sucesso!")
                        st.session_state.editar_produtor_id = None
                    else:
                        adicionar_produtor(nome, documento, rua, numero, complemento, bairro, cidade, estado, cep, user_id)
                        st.success(f"Produtor '{nome}' cadastrado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao cadastrar/editar produtor: {e}")

    st.write("---")
    st.subheader("Produtores cadastrados")
    df_produtores = listar_produtores()
    if not df_produtores.empty:
        for i, row in df_produtores.iterrows():
            col1, col2 = st.columns([8, 1])
            with col1:
                st.write(f"**{row['nome']}** | {row['documento']} | {row['cidade']}/{row['estado']} | Usuário: {row['username']}")
            with col2:
                if st.button("Editar", key=f"editar_{row['id']}"):
                    st.session_state.editar_produtor_id = row['id']
                    st.rerun()
                if st.button("Excluir", key=f"excluir_{row['id']}"):
                    excluir_produtor(row['id'])
                    st.success("Produtor excluído com sucesso!")
                    st.rerun()
    else:
        st.info("Nenhum produtor cadastrado ainda.")
