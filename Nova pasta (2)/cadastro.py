import pymysql
import bcrypt
import subprocess

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="1357924680aA.",
    database="MegaSistemInformaticabd"    
)

cursor = conn.cursor()

def cadastrar_usuario(nome_usuario, senha):
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt)
    
    cursor.execute("""
        INSERT INTO usuarios (nome_usuario, senha)
        VALUES (%s, %s)                 
    """, (nome_usuario, senha_hash))
    conn.commit()
    print("Usuário cadastrado com sucesso!")

    

while True:
    nome_usuario = input("Digite seu nome de usuário: ")
    senha = input("Digite sua senha: ")
    
    cadastrar_usuario(nome_usuario, senha)
    
    continuar = input("Deseja cadastrar outro usuário? (s/n): ")
    if continuar.lower() != 's':
        break

cursor.close()
conn.close()
