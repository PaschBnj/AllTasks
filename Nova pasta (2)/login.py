import tkinter as tk
import pymysql
import bcrypt
import AllTasksfuncionarios
import alltasksclient

# Função para conectar ao banco de dados
def conectar_banco():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1357924680aA.",
        database="MegaSistemInformaticabd"
    )

# Função de login
def login_usuario(nome_usuario, senha):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nome_usuario, senha, cargo, numero_telefone FROM usuarios WHERE nome_usuario = %s",
        (nome_usuario,)
    )
    resultado = cursor.fetchone()
    conn.close()

    if resultado is None:
        return False, "Usuário não encontrado.", None, None, None

    id_usuario, nome_usuario_db, senha_hash, cargo, numero_telefone = resultado

    # Validação da senha
    if isinstance(senha_hash, bytes):
        senha_valida = bcrypt.checkpw(senha.encode('utf-8'), senha_hash)
    else:
        senha_valida = bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8'))

    if senha_valida:
        return True, "Login bem-sucedido!", id_usuario, cargo, numero_telefone
    else:
        return False, "Senha incorreta.", None, None, None

# Função chamada ao tentar fazer login
def tentar_login():
    nome_usuario = entry_usuario.get()
    senha = entry_senha.get()
    
    sucesso, mensagem, id_usuario, cargo, numero_telefone = login_usuario(nome_usuario, senha)
    resultado_label.config(text=mensagem, fg="green" if sucesso else "red")
    
    if sucesso:
        root.quit()  # Fecha a janela de login após login bem-sucedido
        
        # Passando número de telefone junto com os outros argumentos
        if cargo == "cliente":
            alltasksclient.iniciar_programa(id_usuario, nome_usuario, numero_telefone)  
        else:
            AllTasksfuncionarios.iniciar_programa(id_usuario, nome_usuario, numero_telefone)  

# Criação da janela de login
root = tk.Tk()
root.title("Tela de Login")
root.geometry("300x200")

tk.Label(root, text="Nome de Usuário:").pack(pady=5)
entry_usuario = tk.Entry(root)
entry_usuario.pack(pady=5)

tk.Label(root, text="Senha:").pack(pady=5)
entry_senha = tk.Entry(root, show="*")
entry_senha.pack(pady=5)

tk.Button(root, text="Login", command=tentar_login).pack(pady=10)

resultado_label = tk.Label(root, text="")
resultado_label.pack(pady=5)

root.mainloop()
