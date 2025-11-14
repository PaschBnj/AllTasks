import pymysql
import tkinter as tk
from datetime import datetime
import bcrypt

# Função para conectar ao banco de dados
def conectar_banco():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1357924680aA.",
        database="MegaSistemInformaticabd"
    )

# Função para verificar o login do usuário
def login_usuario(nome_usuario, senha):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome_usuario, senha, cargo FROM usuarios WHERE nome_usuario = %s", (nome_usuario,))
    resultado = cursor.fetchone()

    if resultado is None:
        return False, None, None

    id_usuario = resultado[0]
    nome_usuario_bd = resultado[1]
    senha_hash = resultado[2]
    cargo = resultado[3]

    if bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8')):
        return True, id_usuario, nome_usuario_bd, cargo
    else:
        return False, None, None

# Função para criar o ticket no banco de dados
def criar_ticket(id, nome_usuario, titulo, descrição, tipo):
    conn = conectar_banco()
    cursor = conn.cursor()

    # Pegando a data e hora atuais
    data_criação = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Inserir o ticket na tabela "tickets"
    cursor.execute("""
        INSERT INTO tickets (id, nome_usuario, titulo, descrição, tipo, data_criação, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'Pendente')
    """, (id, nome_usuario, titulo, descrição, tipo, data_criação))

    conn.commit()  # Confirma a inserção
    conn.close()

# Função para mostrar o formulário e criar o ticket
def formulario(id, nome_usuario):
    def enviar_ticket():
        titulo = entry_ticket_titulo.get()
        descrição = text_ticket_descrição.get("1.0", tk.END)
        tipo = combo_tipo.get()

        # Chama a função para criar o ticket no banco de dados
        criar_ticket(id, nome_usuario, titulo, descrição, tipo)

        label_resultado.config(text="Ticket criado com sucesso!", fg="green")

    # Criação da interface gráfica para o formulário
    root = tk.Tk()
    root.title("Criar Ticket")
    root.geometry("600x400")

    label_ticket_titulo = tk.Label(root, text="Título do Ticket:")
    label_ticket_titulo.pack(pady=5)

    entry_ticket_titulo = tk.Entry(root, width=50)
    entry_ticket_titulo.pack(pady=5)

    label_ticket_descrição = tk.Label(root, text="Descrição do Ticket:")
    label_ticket_descrição.pack(pady=5)

    text_ticket_descrição = tk.Text(root, height=10, width=50)
    text_ticket_descrição.pack(pady=5)

    label_ticket_tipo = tk.Label(root, text="Tipo de Problema:")
    label_ticket_tipo.pack(pady=5)

    combo_tipo = tk.StringVar()
    combo_tipo.set("Bug")  # Default
    tipo_options = ["Bug", "Informação errada", "Adicionar/Remover produtos/grupos/menus", "Problema fiscal", "Outros"]
    dropdown_tipo = tk.OptionMenu(root, combo_tipo, *tipo_options)
    dropdown_tipo.pack(pady=5)

    botao_enviar = tk.Button(root, text="Enviar Ticket", command=enviar_ticket)
    botao_enviar.pack(pady=10)

    label_resultado = tk.Label(root, text="")  # Label para resultado
    label_resultado.pack(pady=5)

    root.mainloop()

# Função para realizar o login
def tentar_login():
    nome_usuario = entry_usuario.get()
    senha = entry_senha.get()

    sucesso, id_usuario, nome_usuario_bd, cargo = login_usuario(nome_usuario, senha)

    if sucesso:
        resultado_label.config(text="Login bem-sucedido!", fg="green")
        root.quit()  # Fecha a janela de login após login bem-sucedido
        formulario(id_usuario, nome_usuario_bd)  # Chama a função para criar o ticket
    else:
        resultado_label.config(text="Usuário ou senha incorretos.", fg="red")

# Interface de Login
root = tk.Tk()
root.title("Tela de Login")
root.geometry("300x200")

label_usuario = tk.Label(root, text="Nome de Usuário:")
label_usuario.pack(pady=5)

entry_usuario = tk.Entry(root)
entry_usuario.pack(pady=5)

label_senha = tk.Label(root, text="Senha:")
label_senha.pack(pady=5)

entry_senha = tk.Entry(root, show="*")
entry_senha.pack(pady=5)

login_button = tk.Button(root, text="Login", command=tentar_login)
login_button.pack(pady=10)

resultado_label = tk.Label(root, text="")
resultado_label.pack(pady=5)

root.mainloop()
