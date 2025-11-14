import pymysql
import tkinter as tk
from tkinter import ttk

# Função para conectar ao banco de dados
def conectar_banco():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1357924680aA.",
        database="MegaSistemInformaticabd"
    )

# Função para buscar todos os tickets do banco de dados
def buscar_tickets():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("SELECT id_ticket, id, nome_usuario, titulo, descrição, tipo, data_criação, data_conclusão, status FROM tickets")
    tickets = cursor.fetchall()
    
    conn.close()
    return tickets

# Função para exibir os tickets em uma tabela
def exibir_tabela_tickets():
    tickets = buscar_tickets()

    # Criação da janela principal
    root = tk.Tk()
    root.title("Tickets - All Tasks")
    root.geometry("1000x600")  # Ajuste o tamanho conforme necessário

    # Criação do Treeview (Tabela)
    tree = ttk.Treeview(root, columns=("ID Ticket", "ID", "Nome de Usuário", "Título", "Descrição", "Tipo", "Data Criação", "Data Conclusão", "Status"), show="headings")

    # Definindo os cabeçalhos da tabela
    tree.heading("ID Ticket", text="ID do Ticket")
    tree.heading("ID", text="ID do cliente")
    tree.heading("Nome de Usuário", text="Nome do cliente")
    tree.heading("Título", text="Título")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Tipo", text="Tipo")
    tree.heading("Data Criação", text="Data Criação")
    tree.heading("Data Conclusão", text="Data Conclusão")
    tree.heading("Status", text="Status")

    # Definindo a largura das colunas
    tree.column("ID Ticket", width=50, anchor="center")
    tree.column("ID", width=50, anchor="center")
    tree.column("Nome de Usuário", width=150, anchor="center")
    tree.column("Título", width=150, anchor="center")
    tree.column("Descrição", width=300, anchor="w")
    tree.column("Tipo", width=200, anchor="center")
    tree.column("Data Criação", width=150, anchor="center")
    tree.column("Data Conclusão", width=150, anchor="center")
    tree.column("Status", width=100, anchor="center")

    # Inserir os dados na tabela
    for ticket in tickets:
        tree.insert("", tk.END, values=ticket)

    # Adicionar a tabela à interface gráfica
    tree.pack(pady=20)

    # Adicionar um botão para fechar a janela
    botao_fechar = tk.Button(root, text="Fechar", command=root.quit)
    botao_fechar.pack(pady=10)

    # Iniciar a interface gráfica
    root.mainloop()

# Função para iniciar o programa do funcionário
def iniciar_programa(id_usuario, nome_usuario):
    exibir_tabela_tickets()
