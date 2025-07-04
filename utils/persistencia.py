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

def adicionar_usuario(username: str, password: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        hash_senha = hash_password(password)
        cursor.execute("INSERT INTO usuarios (username, password_hash) VALUES (%s, %s)", (username, hash_senha))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
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
