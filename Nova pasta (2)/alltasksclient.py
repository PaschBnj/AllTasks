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

# Função para iniciar o programa do cliente
def iniciar_programa(id_usuario, nome_usuario):
    formulario(id_usuario, nome_usuario)
