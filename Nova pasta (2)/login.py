import pymysql
import bcrypt

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="1357924680aA.",
    database="MegaSistemInformaticabd"    
)

cursor = conn.cursor()

def login_usuario(nome_usuario, senha):
    cursor.execute("SELECT senha FROM usuarios WHERE nome_usuario = %s", (nome_usuario,))
    resultado = cursor.fetchone()
    
    if resultado is None:
        print("Usuário não encontrado.")
        return False
    
    senha_hash = resultado[0]
    
    if bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8')):
        print("Login bem-sucedido!")
        return True
    else:
        print("Senha incorreta.")
        return False

while True:
    nome_usuario = input("Digite seu nome de usuário: ")
    senha = input("Digite sua senha: ")
    
    if login_usuario(nome_usuario, senha):
        break  # Sai do loop se o login for bem-sucedido

cursor.close()
conn.close()
