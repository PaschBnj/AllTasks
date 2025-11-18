import pymysql
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Classe Entry com placeholder
class PlaceholderEntry(ttk.Entry):
    def __init__(self, master, placeholder, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.default_fg = self['foreground'] if 'foreground' in self.keys() else "black"
        self['foreground'] = '#888'
        self.insert(0, self.placeholder)
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

    def _clear_placeholder(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self['foreground'] = self.default_fg

    def _add_placeholder(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self['foreground'] = '#888'

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
    root.state('zoomed')  # Janela maximizada
    root.title("Tickets - All Tasks")
    root.geometry("1100x600")

    # Filtros: placeholders e widgets em linha única
    frame_filtros = tk.Frame(root)
    frame_filtros.pack(pady=20)

    entries_infos = [
        ("ID Ticket", "id_ticket"),
        ("ID", "id"),
        ("Nome do Usuário", "nome_usuario"),
        ("Título", "titulo"),
        ("Descrição", "descrição"),
        ("Tipo", "tipo"),
        ("Data Criação", "data_criação"),
        ("Data Conclusão", "data_conclusão"),
        ("Status", "status"),
        ("Telefone", "numero_telefone"),
    ]

    entry_widgets = {}
    for col, (placeholder, var_name) in enumerate(entries_infos):
        entry = PlaceholderEntry(frame_filtros, placeholder)
        entry.grid(row=0, column=col, padx=5)
        entry_widgets[var_name] = entry

    # Função para buscar filtros
    def aplicar_filtro():
        filtros = {
            var_name: (entry_widgets[var_name].get() if entry_widgets[var_name].get() != placeholder else "")
            for (placeholder, var_name) in entries_infos
        }
        tickets = buscar_tickets(filtros)
        for item in tree.get_children():
            tree.delete(item)
        for ticket in tickets:
            tree.insert("", tk.END, values=ticket)

    tk.Button(frame_filtros, text="Filtrar", command=aplicar_filtro).grid(row=0, column=len(entries_infos), padx=10)

    # Treeview para exibir tickets
    columns = ("ID Ticket", "ID", "Nome de Usuário", "Título", "Descrição", "Tipo", 
               "Data Criação", "Data Conclusão", "Status", "Telefone")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    tree.pack(pady=20, fill=tk.BOTH, expand=True)


    # Detalhes do ticket em janela separada
    def exibir_detalhes_ticket(ticket):
        detalhes_window = tk.Toplevel(root)
        detalhes_window.title(f"Detalhes do Ticket: {ticket[3]}")
        detalhes_window.geometry("500x400")
        labels = [
            f"id ticket: {ticket[0]}",
            f"id: {ticket[1]}",
            f"Título: {ticket[3]}",
            f"Nome do Cliente: {ticket[2]}",
            f"Telefone: {ticket[9]}",
            f"Descrição: {ticket[4]}",
            f"Tipo: {ticket[5]}",
            f"Data de Criação: {ticket[6]}",
            f"Data de Conclusão: {ticket[7] if ticket[7] else 'Não concluído'}",
            f"Status: {ticket[8]}"
        ]
        for lbl in labels:
            tk.Label(detalhes_window, text=lbl).pack(pady=5)
        # Botões de status
        def atualizar_status(novo_status):
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute("UPDATE tickets SET status=%s WHERE id_ticket=%s", (novo_status, ticket[0]))
            conn.commit()
            conn.close()
            detalhes_window.destroy()
            aplicar_filtro() # Atualiza na tela principal

        tk.Button(detalhes_window, text="Assumir Ticket", command=lambda: atualizar_status("Em Progresso")).pack(pady=5)
        tk.Button(detalhes_window, text="Concluído", command=lambda: atualizar_status("Concluído")).pack(pady=5)

    def on_double_click(event):
        # Protege contra clique sem nada selecionado
        selected = tree.selection()
        if not selected:
            return
        ticket = tree.item(selected[0])["values"]
        if ticket:
            exibir_detalhes_ticket(ticket)
    tree.bind("<Double-1>", on_double_click)

    tk.Button(root, text="Fechar", command=root.quit).pack(pady=10)

    # Atualização automática da tabela
    def atualizar_tabela():
        filtros = {
            var_name: (entry_widgets[var_name].get() if entry_widgets[var_name].get() != placeholder else "")
            for (placeholder, var_name) in entries_infos
        }
        tickets = buscar_tickets(filtros)
        for item in tree.get_children():
            tree.delete(item)
        for ticket in tickets:
            tree.insert("", tk.END, values=ticket)
        root.after(1000, atualizar_tabela) # Chama novamente em 1s

    atualizar_tabela()
    root.mainloop()

def iniciar_programa(id_usuario, nome_usuario, numero_telefone):
    print(f"ID: {id_usuario}, Nome: {nome_usuario}, Telefone: {numero_telefone}")
    exibir_tabela_tickets()
