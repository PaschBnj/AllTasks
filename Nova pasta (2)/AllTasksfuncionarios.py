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

# Função para buscar tickets com filtros
def buscar_tickets(filtros):
    conn = conectar_banco()
    cursor = conn.cursor()

    query = """
        SELECT id_ticket, id, nome_usuario, titulo, descrição, tipo, data_criação, data_conclusão, status, numero_telefone
        FROM tickets WHERE 1
    """
    params = []

    # Adicionando filtros à consulta
    if filtros["id_ticket"]:
        query += " AND id_ticket LIKE %s"
        params.append(f"%{filtros['id_ticket']}%")
    
    if filtros["id"]:
        query += " AND id LIKE %s"
        params.append(f"%{filtros['id']}%")

    if filtros["nome_usuario"]:
        query += " AND nome_usuario LIKE %s"
        params.append(f"%{filtros['nome_usuario']}%")

    if filtros["titulo"]:
        query += " AND titulo LIKE %s"
        params.append(f"%{filtros['titulo']}%")

    if filtros["descrição"]:
        query += " AND descrição LIKE %s"
        params.append(f"%{filtros['descrição']}%")
    
    if filtros["tipo"]:
        query += " AND tipo LIKE %s"
        params.append(f"%{filtros['tipo']}%")

    if filtros["data_criação"]:
        query += " AND data_criação LIKE %s"
        params.append(f"%{filtros['data_criação']}%")

    if filtros["data_conclusão"]:
        query += " AND data_conclusão LIKE %s"
        params.append(f"%{filtros['data_conclusão']}%")

    if filtros["status"]:
        query += " AND status LIKE %s"
        params.append(f"%{filtros['status']}%")

    if filtros["numero_telefone"]:
        query += " AND numero_telefone LIKE %s"
        params.append(f"%{filtros['numero_telefone']}%")

    cursor.execute(query, params)
    tickets = cursor.fetchall()
    conn.close()

    return tickets

# Exibir tickets na tabela
def exibir_tabela_tickets():
    root = tk.Tk()
    root.title("Tickets - All Tasks")
    root.geometry("1000x600")

    # Filtros
    def aplicar_filtro():
        filtros = {
            "id_ticket": entry_id_ticket.get(),
            "id": entry_id.get(),
            "nome_usuario": entry_nome_usuario.get(),
            "titulo": entry_titulo.get(),
            "descrição": entry_descrição.get(),
            "tipo": entry_tipo.get(),
            "data_criação": entry_data_criação.get(),
            "data_conclusão": entry_data_conclusão.get(),
            "status": entry_status.get(),
            "numero_telefone": entry_telefone.get(),
        }
        tickets = buscar_tickets(filtros)
        
        # Limpa a tabela existente
        for item in tree.get_children():
            tree.delete(item)

        # Insere os tickets filtrados na tabela
        for ticket in tickets:
            tree.insert("", tk.END, values=ticket)

    # Filtros na parte superior da tela
    frame_filtros = tk.Frame(root)
    frame_filtros.pack(pady=20)

    tk.Label(frame_filtros, text="ID Ticket:").grid(row=0, column=0, padx=10)
    entry_id_ticket = tk.Entry(frame_filtros)
    entry_id_ticket.grid(row=0, column=1, padx=10)

    tk.Label(frame_filtros, text="ID:").grid(row=0, column=2, padx=10)
    entry_id = tk.Entry(frame_filtros)
    entry_id.grid(row=0, column=3, padx=10)

    tk.Label(frame_filtros, text="Nome do Usuário:").grid(row=1, column=0, padx=10)
    entry_nome_usuario = tk.Entry(frame_filtros)
    entry_nome_usuario.grid(row=1, column=1, padx=10)

    tk.Label(frame_filtros, text="Título:").grid(row=1, column=2, padx=10)
    entry_titulo = tk.Entry(frame_filtros)
    entry_titulo.grid(row=1, column=3, padx=10)

    tk.Label(frame_filtros, text="Descrição:").grid(row=2, column=0, padx=10)
    entry_descrição = tk.Entry(frame_filtros)
    entry_descrição.grid(row=2, column=1, padx=10)

    tk.Label(frame_filtros, text="Tipo:").grid(row=2, column=2, padx=10)
    entry_tipo = tk.Entry(frame_filtros)
    entry_tipo.grid(row=2, column=3, padx=10)

    tk.Label(frame_filtros, text="Data Criação:").grid(row=3, column=0, padx=10)
    entry_data_criação = tk.Entry(frame_filtros)
    entry_data_criação.grid(row=3, column=1, padx=10)

    tk.Label(frame_filtros, text="Data Conclusão:").grid(row=3, column=2, padx=10)
    entry_data_conclusão = tk.Entry(frame_filtros)
    entry_data_conclusão.grid(row=3, column=3, padx=10)

    tk.Label(frame_filtros, text="Status:").grid(row=4, column=0, padx=10)
    entry_status = tk.Entry(frame_filtros)
    entry_status.grid(row=4, column=1, padx=10)

    tk.Label(frame_filtros, text="Telefone:").grid(row=4, column=2, padx=10)
    entry_telefone = tk.Entry(frame_filtros)
    entry_telefone.grid(row=4, column=3, padx=10)

    tk.Button(frame_filtros, text="Filtrar", command=aplicar_filtro).grid(row=5, column=3, pady=10)

    # Configurar Treeview
    tree = ttk.Treeview(root, columns=("ID Ticket", "ID", "Nome de Usuário", "Título", "Descrição", "Tipo", "Data Criação", "Data Conclusão", "Status", "Telefone"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    
    # Inserir tickets iniciais (sem filtro)
    tickets = buscar_tickets({
        "id_ticket": "", 
        "id": "", 
        "nome_usuario": "", 
        "titulo": "", 
        "descrição": "", 
        "tipo": "", 
        "data_criação": "", 
        "data_conclusão": "", 
        "status": "", 
        "numero_telefone": ""
    })

    for ticket in tickets:
        tree.insert("", tk.END, values=ticket)

    tree.pack(pady=20)

    # Detalhes do ticket
    def exibir_detalhes_ticket(ticket):
        id_ticket, cliente_id, nome_usuario, titulo, descrição, tipo, data_criação, data_conclusão, status, numero_telefone = ticket
        detalhes_window = tk.Toplevel(root)
        detalhes_window.title(f"Detalhes do Ticket: {titulo}")
        detalhes_window.geometry("500x400")

        tk.Label(detalhes_window, text=f"id ticket: {id_ticket}").pack(pady=5)
        tk.Label(detalhes_window, text=f"id: {cliente_id}").pack(pady=5)
        tk.Label(detalhes_window, text=f"Título: {titulo}").pack(pady=5)
        tk.Label(detalhes_window, text=f"Nome do Cliente: {nome_usuario}").pack(pady=5)
        tk.Label(detalhes_window, text=f"Telefone: {numero_telefone}").pack(pady=5)
        tk.Label(detalhes_window, text=f"Descrição: {descrição}").pack(pady=5)
        tk.Label(detalhes_window, text=f"Tipo: {tipo}").pack(pady=5)
        tk.Label(detalhes_window, text=f"Data de Criação: {data_criação}").pack(pady=5)
        tk.Label(detalhes_window, text=f"Data de Conclusão: {data_conclusão if data_conclusão else 'Não concluído'}").pack(pady=5)
        tk.Label(detalhes_window, text=f"Status: {status}").pack(pady=5)


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
        tk.Label(detalhes_window, text="Status: Pendente", fg="red").pack(pady=5)
        tk.Label(detalhes_window, text=f"Status: {status}").pack(pady=5)

        # Botões de status
        def atualizar_status(novo_status):
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute("UPDATE tickets SET status=%s WHERE id_ticket=%s", (novo_status, id_ticket))
            conn.commit()
            conn.close()
            detalhes_window.destroy()
            exibir_tabela_tickets(id, nome_usuario)

        tk.Button(detalhes_window, text="Assumir Ticket", command=lambda: atualizar_status("Em Progresso")).pack(pady=5)
        tk.Button(detalhes_window, text="Concluído", command=lambda: atualizar_status("Concluído")).pack(pady=5)

    tree.bind("<Double-1>", lambda event: exibir_detalhes_ticket(tree.item(tree.selection())["values"]))
    tk.Button(root, text="Fechar", command=root.quit).pack(pady=10)


    root.mainloop()

# Chama a função para exibir os tickets após login bem-sucedido
# Isso deve ser feito pela sua lógica de login, ou seja, você já está chamando `exibir_tabela_tickets()` após o login.
def iniciar_programa(id_usuario, nome_usuario, numero_telefone):
    print(f"ID: {id_usuario}, Nome: {nome_usuario}, Telefone: {numero_telefone}")
    exibir_tabela_tickets()

