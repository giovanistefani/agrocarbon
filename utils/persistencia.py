import hashlib
import pandas as pd
import mysql.connector
from mysql.connector import Error
import secrets
from datetime import datetime, timedelta

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # ajuste para seu usuário
        password='Gb$127311',  # ajuste para sua senha
        database='agrocarbon'  # ajuste para seu banco
    )

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def carregar_usuarios():
    try:
        conn = get_connection()
        query = "SELECT username, password_hash FROM usuarios"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Error as e:
        print(f"Erro ao carregar usuários: {e}")
        return pd.DataFrame(columns=['username', 'password_hash'])

def adicionar_usuario(username: str, password: str, email: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        hash_senha = hash_password(password)
        cursor.execute("INSERT INTO usuarios (username, password_hash, email) VALUES (%s, %s, %s)", (username, hash_senha, email))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao adicionar usuário: {e}")

def verificar_usuario(username: str, password: str) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        hash_senha = hash_password(password)
        cursor.execute("SELECT * FROM usuarios WHERE username=%s AND password_hash=%s", (username, hash_senha))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is not None
    except Error as e:
        print(f"Erro ao verificar usuário: {e}")
        return False

def gerar_token_reset(email):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM usuarios WHERE email=%s", (email,))
        user = cursor.fetchone()
        if not user:
            cursor.close()
            conn.close()
            return None
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=1)
        cursor.execute("INSERT INTO reset_tokens (user_id, token, expires_at) VALUES (%s, %s, %s)", (user['id'], token, expires_at))
        conn.commit()
        cursor.close()
        conn.close()
        return token
    except Exception as e:
        print(f"Erro ao gerar token de reset: {e}")
        return None

def validar_token_reset(token):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id, expires_at FROM reset_tokens WHERE token=%s", (token,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row and row['expires_at'] > datetime.now():
            return row['user_id']
        return None
    except Exception as e:
        print(f"Erro ao validar token: {e}")
        return None

def atualizar_senha_por_token(token, nova_senha):
    try:
        user_id = validar_token_reset(token)
        if not user_id:
            return False
        conn = get_connection()
        cursor = conn.cursor()
        hash_senha = hash_password(nova_senha)
        cursor.execute("UPDATE usuarios SET password_hash=%s WHERE id=%s", (hash_senha, user_id))
        cursor.execute("DELETE FROM reset_tokens WHERE token=%s", (token,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao atualizar senha: {e}")
        return False

def adicionar_produtor(nome, documento, rua, numero, complemento, bairro, cidade, estado, cep, user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO produtores (nome, documento, rua, numero, complemento, bairro, cidade, estado, cep, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (nome, documento, rua, numero, complemento, bairro, cidade, estado, cep, user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao adicionar produtor: {e}")

def get_user_id_by_username(username):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE username=%s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return result[0]
        return None
    except Exception as e:
        print(f"Erro ao buscar user_id: {e}")
        return None

def listar_usuarios():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return usuarios
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        return []

def listar_produtores():
    try:
        conn = get_connection()
        query = '''
            SELECT p.id, p.nome, p.documento, p.rua, p.numero, p.complemento, p.bairro, p.cidade, p.estado, p.cep, p.user_id, u.username
            FROM produtores p
            JOIN usuarios u ON p.user_id = u.id
        '''
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Erro ao listar produtores: {e}")
        return pd.DataFrame()

def listar_usuarios_df():
    try:
        conn = get_connection()
        df = pd.read_sql("SELECT id, username, email FROM usuarios", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        return pd.DataFrame()

def listar_propriedades():
    try:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM propriedades", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Erro ao listar propriedades: {e}")
        return pd.DataFrame()

def excluir_produtor(produtor_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtores WHERE id=%s", (produtor_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao excluir produtor: {e}")

def editar_produtor(produtor_id, nome, documento, rua, numero, complemento, bairro, cidade, estado, cep, user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE produtores SET nome=%s, documento=%s, rua=%s, numero=%s, complemento=%s, bairro=%s, cidade=%s, estado=%s, cep=%s, user_id=%s
            WHERE id=%s
            """,
            (nome, documento, rua, numero, complemento, bairro, cidade, estado, cep, user_id, produtor_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao editar produtor: {e}")

def adicionar_propriedade(nome, rua, numero, complemento, bairro, cidade, estado, cep, tamanho, latitude, longitude):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO propriedades (nome, rua, numero, complemento, bairro, cidade, estado, cep, tamanho, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (nome, rua, numero, complemento, bairro, cidade, estado, cep, tamanho, latitude, longitude)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao adicionar propriedade: {e}")

def listar_produtores_simples():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM produtores")
        produtores = cursor.fetchall()
        cursor.close()
        conn.close()
        return produtores
    except Exception as e:
        print(f"Erro ao listar produtores: {e}")
        return []

def adicionar_propriedade_com_produtores(nome, rua, numero, complemento, bairro, cidade, estado, cep, tamanho, latitude, longitude, produtores_ids):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO propriedades (nome, rua, numero, complemento, bairro, cidade, estado, cep, tamanho, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (nome, rua, numero, complemento, bairro, cidade, estado, cep, tamanho, latitude, longitude)
        )
        propriedade_id = cursor.lastrowid
        for produtor_id in produtores_ids:
            cursor.execute(
                "INSERT INTO propriedade_produtor (propriedade_id, produtor_id) VALUES (%s, %s)",
                (propriedade_id, produtor_id)
            )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        import streamlit as st
        st.error(f"Erro ao adicionar propriedade com produtores: {e}")
        print(f"Erro ao adicionar propriedade com produtores: {e}")
        raise

def listar_propriedades_com_produtores():
    """
    Lista propriedades exibindo os produtores vinculados (join N:N).
    Retorna um DataFrame com colunas: id, nome, cidade, estado, tamanho, produtores (lista de nomes)
    """
    try:
        conn = get_connection()
        query = '''
            SELECT p.id, p.nome, p.cidade, p.estado, p.tamanho,
                   GROUP_CONCAT(pr.nome SEPARATOR ', ') as produtores
            FROM propriedades p
            LEFT JOIN propriedade_produtor pp ON p.id = pp.propriedade_id
            LEFT JOIN produtores pr ON pp.produtor_id = pr.id
            GROUP BY p.id, p.nome, p.cidade, p.estado, p.tamanho
        '''
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Erro ao listar propriedades com produtores: {e}")
        return pd.DataFrame()

def buscar_produtores_por_propriedade(propriedade_id):
    """
    Retorna uma lista de IDs dos produtores vinculados a uma propriedade.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT produtor_id FROM propriedade_produtor WHERE propriedade_id=%s", (propriedade_id,))
        ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return ids
    except Exception as e:
        print(f"Erro ao buscar produtores da propriedade: {e}")
        return []

def editar_usuario(usuario_id, username, email):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE usuarios SET username=%s, email=%s WHERE id=%s
            """,
            (username, email, usuario_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao editar usuário: {e}")

def excluir_usuario(usuario_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=%s", (usuario_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao excluir usuário: {e}")

def editar_propriedade(propriedade_id, nome, rua, numero, complemento, bairro, cidade, estado, cep, tamanho, latitude, longitude):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE propriedades SET nome=%s, rua=%s, numero=%s, complemento=%s, bairro=%s, cidade=%s, estado=%s, cep=%s, tamanho=%s, latitude=%s, longitude=%s
            WHERE id=%s
            """,
            (nome, rua, numero, complemento, bairro, cidade, estado, cep, tamanho, latitude, longitude, propriedade_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao editar propriedade: {e}")

def excluir_propriedade(propriedade_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Remove vínculos na tabela de associação
        cursor.execute("DELETE FROM propriedade_produtor WHERE propriedade_id=%s", (propriedade_id,))
        cursor.execute("DELETE FROM propriedades WHERE id=%s", (propriedade_id,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao excluir propriedade: {e}")

def atualizar_vinculos_propriedade_produtor(propriedade_id, produtores_ids):
    """
    Atualiza os vínculos de produtores para uma propriedade (remove todos e insere os novos).
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM propriedade_produtor WHERE propriedade_id=%s", (propriedade_id,))
        for produtor_id in produtores_ids:
            cursor.execute(
                "INSERT INTO propriedade_produtor (propriedade_id, produtor_id) VALUES (%s, %s)",
                (propriedade_id, produtor_id)
            )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao atualizar vínculos de produtores da propriedade: {e}")
