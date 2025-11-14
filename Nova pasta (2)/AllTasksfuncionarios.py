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
def exibir_tabela_tickets(id_usuario, nome_usuario):
    tickets = buscar_tickets()

    # Criação da janela principal
    root = tk.Tk()
    root.title("Tickets - All Tasks")
    root.geometry("1000x600")

    # Criação do Treeview (Tabela)
    tree = ttk.Treeview(root, columns=("ID Ticket", "ID", "Nome de Usuário", "Título", "descrição", "Tipo", "Data Criação", "Data Conclusão", "Status"), show="headings")

    # Definindo os cabeçalhos da tabela
    tree.heading("ID Ticket", text="ID do Ticket")
    tree.heading("ID", text="ID do cliente")
    tree.heading("Nome de Usuário", text="Nome do cliente")
    tree.heading("Título", text="Título")
    tree.heading("descrição", text="descrição")
    tree.heading("Tipo", text="Tipo")
    tree.heading("Data Criação", text="Data Criação")
    tree.heading("Data Conclusão", text="Data Conclusão")
    tree.heading("Status", text="Status")

    # Definindo a largura das colunas
    tree.column("ID Ticket", width=50, anchor="center")
    tree.column("ID", width=50, anchor="center")
    tree.column("Nome de Usuário", width=150, anchor="center")
    tree.column("Título", width=150, anchor="center")
    tree.column("descrição", width=300, anchor="w")
    tree.column("Tipo", width=200, anchor="center")
    tree.column("Data Criação", width=150, anchor="center")
    tree.column("Data Conclusão", width=150, anchor="center")
    tree.column("Status", width=100, anchor="center")

    # Inserir os dados na tabela
    for ticket in tickets:
        tree.insert("", tk.END, values=ticket)

    # Adicionar a tabela à interface gráfica
    tree.pack(pady=20)

    # Função para abrir os detalhes de um ticket
    def exibir_detalhes_ticket(ticket):
        ticket_id, cliente_id, nome_usuario, titulo, descrição, tipo, data_criação, data_conclusão, status = ticket

        # Criação da janela de detalhes
        detalhes_window = tk.Toplevel(root)
        detalhes_window.title(f"Detalhes do Ticket: {titulo}")
        detalhes_window.geometry("500x400")

        # Exibir os dados do ticket
        label_titulo = tk.Label(detalhes_window, text=f"Título: {titulo}")
        label_titulo.pack(pady=5)

        label_nome_usuario = tk.Label(detalhes_window, text=f"Nome do Cliente: {nome_usuario}")
        label_nome_usuario.pack(pady=5)

        label_descrição = tk.Label(detalhes_window, text=f"descrição: {descrição}")
        label_descrição.pack(pady=5)

        label_tipo = tk.Label(detalhes_window, text=f"Tipo: {tipo}")
        label_tipo.pack(pady=5)

        label_data_criação = tk.Label(detalhes_window, text=f"Data de Criação: {data_criação}")
        label_data_criação.pack(pady=5)

        label_data_conclusão = tk.Label(detalhes_window, text=f"Data de Conclusão: {data_conclusão if data_conclusão else 'Não concluído'}")
        label_data_conclusão.pack(pady=5)

        label_status = tk.Label(detalhes_window, text=f"Status: {status}")
        label_status.pack(pady=5)

        # Função para atualizar o status do ticket para "Em Progresso"
        def assumir_ticket():
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute("UPDATE tickets SET status = 'Em Progresso' WHERE id_ticket = %s", (ticket_id,))
            conn.commit()
            conn.close()
            detalhes_window.destroy()  # Fecha a janela de detalhes após atualizar
            exibir_tabela_tickets(id_usuario, nome_usuario)  # Atualiza a tabela de tickets

        # Função para atualizar o status do ticket para "Concluído"
        def ticket_concluido():
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute("UPDATE tickets SET status = 'Concluído' WHERE id_ticket = %s", (ticket_id,))
            conn.commit()
            conn.close()
            detalhes_window.destroy()  # Fecha a janela de detalhes após atualizar
            exibir_tabela_tickets(id_usuario, nome_usuario)  # Atualiza a tabela de tickets

        # Botões para assumir ou concluir o ticket
        botao_assumir = tk.Button(detalhes_window, text="Assumir Ticket", command=assumir_ticket)
        botao_assumir.pack(pady=10)

        botao_concluido = tk.Button(detalhes_window, text="Ticket Concluído", command=ticket_concluido)
        botao_concluido.pack(pady=10)

    # Vincula a ação de clicar na tabela aos detalhes do ticket
    tree.bind("<Double-1>", lambda event: exibir_detalhes_ticket(tree.item(tree.selection())["values"]))

    # Adicionar um botão para fechar a janela
    botao_fechar = tk.Button(root, text="Fechar", command=root.quit)
    botao_fechar.pack(pady=10)

    # Iniciar a interface gráfica
    root.mainloop()

# Função chamada no login
def iniciar_programa(id_usuario, nome_usuario):
    exibir_tabela_tickets(id_usuario, nome_usuario)
