import pymysql
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Conexão com o banco
def conectar_banco():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1357924680aA.",
        database="MegaSistemInformaticabd"
    )

# Função para criar ticket com número de telefone
def criar_ticket(id_usuario, nome_usuario, numero_telefone, titulo, descricao, tipo):
    conn = conectar_banco()
    cursor = conn.cursor()

    data_criacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute(""" 
        INSERT INTO tickets (id, nome_usuario, numero_telefone, titulo, descrição, tipo, data_criação, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'Pendente')
    """, (id_usuario, nome_usuario, numero_telefone, titulo, descricao, tipo, data_criacao))

    conn.commit()
    conn.close()

# Formulário para criar ticket
def buscar_tickets_usuario(id_usuario):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_ticket, titulo, descrição, tipo, data_criação, status
        FROM tickets WHERE id = %s
    """, (id_usuario,))
    tickets = cursor.fetchall()
    conn.close()
    return tickets

def formulario(id_usuario, nome_usuario, numero_telefone):
    def enviar_ticket():
        titulo = entry_ticket_titulo.get()
        descricao = text_ticket_descricao.get("1.0", tk.END)
        tipo = combo_tipo.get()
        criar_ticket(id_usuario, nome_usuario, numero_telefone, titulo, descricao, tipo)
        label_resultado.config(text="Ticket criado com sucesso!", fg="green")
        atualizar_tabela_tickets()

    root = tk.Tk()
    root.title("Criar Ticket")
    root.geometry("700x500")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # Tab 1: Criar Ticket
    frame_criar = tk.Frame(notebook)
    notebook.add(frame_criar, text="Criar Ticket")

    tk.Label(frame_criar, text="Título do Ticket:").pack(pady=5)
    entry_ticket_titulo = tk.Entry(frame_criar, width=50)
    entry_ticket_titulo.pack(pady=5)

    tk.Label(frame_criar, text="Descrição do Ticket:").pack(pady=5)
    text_ticket_descricao = tk.Text(frame_criar, height=10, width=50)
    text_ticket_descricao.pack(pady=5)

    tk.Label(frame_criar, text="Tipo de Problema:").pack(pady=5)
    combo_tipo = tk.StringVar(value="Bug")
    tipo_options = ["Bug", "Informação errada", "Adicionar/Remover produtos/grupos/menus", "Problema fiscal", "Outros"]
    tk.OptionMenu(frame_criar, combo_tipo, *tipo_options).pack(pady=5)

    tk.Button(frame_criar, text="Enviar Ticket", command=enviar_ticket).pack(pady=10)
    label_resultado = tk.Label(frame_criar, text="")
    label_resultado.pack(pady=5)

    # Tab 2: Meus Tickets
    frame_tickets = tk.Frame(notebook)
    notebook.add(frame_tickets, text="Meus Tickets")

    columns = ("ID Ticket", "Título", "Descrição", "Tipo", "Data Criação", "Status")
    tree = ttk.Treeview(frame_tickets, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill='both', expand=True, padx=10, pady=10)

    def atualizar_tabela_tickets():
        for row in tree.get_children():
            tree.delete(row)
        tickets = buscar_tickets_usuario(id_usuario)
        for ticket in tickets:
            tree.insert("", "end", values=ticket)

    atualizar_tabela_tickets()

    root.mainloop()

# Função principal do cliente
def iniciar_programa(id_usuario, nome_usuario, numero_telefone):
    print(f"Cliente {nome_usuario} ({id_usuario}), Telefone: {numero_telefone}")
    formulario(id_usuario, nome_usuario, numero_telefone)
