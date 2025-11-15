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

def cadastrar_usuario(nome_usuario, senha, cargo, numero_telefone):
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt)
    
    cursor.execute("""
        INSERT INTO usuarios (nome_usuario, senha, cargo, numero_telefone)
        VALUES (%s, %s, %s, %s)                 
    """, (nome_usuario, senha_hash, cargo, numero_telefone))
    conn.commit()
    print("Usuário cadastrado com sucesso!")

    

while True:
    nome_usuario = input("Digite o nome de usuário a ser cadastrado: ")
    senha = input("Digite sua senha: ")
    cargo = input("Qual o cargo do usuario a ser cadastrado? (cliente/funcionario/gerente)")
    numero_telefone = input("Qual o numero de contato(telefone) do usuario a ser cadastrado?")
    
    cadastrar_usuario(nome_usuario, senha, cargo, numero_telefone)
    
    continuar = input("Deseja cadastrar outro usuário? (s/n): ")
    if continuar.lower() != 's':
        break

cursor.close()
conn.close()
