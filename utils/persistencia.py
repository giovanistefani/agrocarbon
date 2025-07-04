import os
import pandas as pd
import hashlib

CSV_FILE = 'propriedades.csv'
USERS_FILE = 'usuarios.csv'
PRODUTORES_FILE = 'produtores.csv'

def carregar_dados():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=['Nome da Propriedade', 'Proprietário(a)', 'Município', 'UF', 'Área (ha)'])

def salvar_dados(df):
    df.to_csv(CSV_FILE, index=False)

def carregar_usuarios():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    else:
        return pd.DataFrame(columns=['username', 'password_hash'])

def salvar_usuarios(df):
    df.to_csv(USERS_FILE, index=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def carregar_produtores():
    if os.path.exists(PRODUTORES_FILE):
        return pd.read_csv(PRODUTORES_FILE)
    else:
        return pd.DataFrame(columns=['Nome', 'CPF/CNPJ', 'Telefone', 'E-mail'])

def salvar_produtores(df):
    df.to_csv(PRODUTORES_FILE, index=False)
