import pymysql
import tkinter as tk
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
def formulario(id_usuario, nome_usuario, numero_telefone):
    def enviar_ticket():
        titulo = entry_ticket_titulo.get()
        descricao = text_ticket_descricao.get("1.0", tk.END)
        tipo = combo_tipo.get()

        criar_ticket(id_usuario, nome_usuario, numero_telefone, titulo, descricao, tipo)
        label_resultado.config(text="Ticket criado com sucesso!", fg="green")


    root = tk.Tk()
    root.title("Criar Ticket")
    root.geometry("600x400")

    tk.Label(root, text="Título do Ticket:").pack(pady=5)
    entry_ticket_titulo = tk.Entry(root, width=50)
    entry_ticket_titulo.pack(pady=5)

    tk.Label(root, text="Descrição do Ticket:").pack(pady=5)
    text_ticket_descricao = tk.Text(root, height=10, width=50)
    text_ticket_descricao.pack(pady=5)

    tk.Label(root, text="Tipo de Problema:").pack(pady=5)
    combo_tipo = tk.StringVar(value="Bug")
    tipo_options = ["Bug", "Informação errada", "Adicionar/Remover produtos/grupos/menus", "Problema fiscal", "Outros"]
    tk.OptionMenu(root, combo_tipo, *tipo_options).pack(pady=5)

    tk.Button(root, text="Enviar Ticket", command=enviar_ticket).pack(pady=10)
    label_resultado = tk.Label(root, text="")
    label_resultado.pack(pady=5)

    root.mainloop()

# Função principal do cliente
def iniciar_programa(id_usuario, nome_usuario, numero_telefone):
    print(f"Cliente {nome_usuario} ({id_usuario}), Telefone: {numero_telefone}")
    formulario(id_usuario, nome_usuario, numero_telefone)
