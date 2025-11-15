import pymysql
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Conexão com banco
def conectar_banco():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1357924680aA.",
        database="MegaSistemInformaticabd"
    )

# Buscar tickets
def buscar_tickets():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT id_ticket, id, nome_usuario, titulo, descrição, tipo, data_criação, data_conclusão, status, numero_telefone FROM tickets")
    tickets = cursor.fetchall()
    conn.close()
    return tickets

# Exibir tickets na tabela
def exibir_tabela_tickets(id_usuario, nome_usuario):
    tickets = buscar_tickets()
    root = tk.Tk()
    root.title("Tickets - All Tasks")
    root.geometry("1000x600")

    tree = ttk.Treeview(root, columns=("ID Ticket", "ID", "Nome de Usuário", "Título", "Descrição", "Tipo", "Data Criação", "Data Conclusão", "Status", "Telefone"), show="headings")
    headings = ["ID Ticket","ID","Nome de Usuário","Título","Descrição","Tipo","Data Criação","Data Conclusão","Status","Telefone"]
    for col in headings:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    for ticket in tickets:
        tree.insert("", tk.END, values=ticket)

    tree.pack(pady=20)

    # Detalhes do ticket
    def exibir_detalhes_ticket(ticket):
        id_ticket, cliente_id, nome_usuario, titulo, descricao, tipo, data_criacao, data_conclusao, status, numero_telefone = ticket
        detalhes_window = tk.Toplevel(root)
        detalhes_window.title(f"Detalhes do Ticket: {titulo}")
        detalhes_window.geometry("500x400")

        tk.Label(detalhes_window, text=f"Título: {titulo}").pack(pady=5)
        tk.Label(detalhes_window, text=f"Nome do Cliente: {nome_usuario}").pack(pady=5)
        tk.Label(detalhes_window, text=f"Telefone: {numero_telefone}").pack(pady=5)
        tk.Label(detalhes_window, text=f"Descrição: {descricao}").pack(pady=5)
        tk.Label(detalhes_window, text=f"Tipo: {tipo}").pack(pady=5)
        tk.Label(detalhes_window, text=f"Data de Criação: {data_criacao}").pack(pady=5)
        tk.Label(detalhes_window, text=f"Data de Conclusão: {data_conclusao if data_conclusao else 'Não concluído'}").pack(pady=5)
        tk.Label(detalhes_window, text=f"Status: {status}").pack(pady=5)

        # Botões de status
        def atualizar_status(novo_status):
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute("UPDATE tickets SET status=%s WHERE id_ticket=%s", (novo_status, id_ticket))
            conn.commit()
            conn.close()
            detalhes_window.destroy()
            exibir_tabela_tickets(id_usuario, nome_usuario)

        tk.Button(detalhes_window, text="Assumir Ticket", command=lambda: atualizar_status("Em Progresso")).pack(pady=5)
        tk.Button(detalhes_window, text="Concluído", command=lambda: atualizar_status("Concluído")).pack(pady=5)

    tree.bind("<Double-1>", lambda event: exibir_detalhes_ticket(tree.item(tree.selection())["values"]))
    tk.Button(root, text="Fechar", command=root.quit).pack(pady=10)

    root.mainloop()

# Função principal do funcionário
def iniciar_programa(id_usuario, nome_usuario, numero_telefone):
    print(f"ID: {id_usuario}, Nome: {nome_usuario}, Telefone: {numero_telefone}")
    exibir_tabela_tickets(id_usuario, nome_usuario)
