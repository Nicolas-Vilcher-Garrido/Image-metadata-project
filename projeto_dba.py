import pyodbc 
import tkinter as tk
from tkinter import messagebox


# 1 - Conectar ao banco de dados
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS01;DATABASE=projetodba;Trusted_Connection=yes;')
cursor = conn.cursor()
    #1.1 Inserir dados
def insert_data():
    preco = entry_preco.get()
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()
    datavenda = entry_datavenda.get()
    #1.2 Tratativa de possíveis erros com try, except e finally
    try:
        cursor.execute("INSERT INTO INTERFACE (Preço, Nome, Quantidade, datavenda) Values (?,?,?,?)",
                       (preco, nome, quantidade, datavenda))
        conn.commit()
        messagebox.showinfo("Sucesso", "Dados inseridos!")
        clear_entries()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao inserir dados: {e}")
        
    # 1.3 Declarando clear entries para o app não fechar e limpar as entradas quando colocarmos novos dados
def clear_entries():
    entry_preco.delete(0, tk.END) 
    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_id.delete(0, tk.END)

    # 1.4- Deletando dados
def delete_data():
    id_delete = entry_id.get()
    try:
        cursor.execute("DELETE FROM INTERFACE WHERE ID = ?", (id_delete,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Dados deletados!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao deletar dados: {e}")
        
    
     
# 2 Criando a Janela principal
root = tk.Tk()
root.title("Interface de Manipulação de dados")

# 3 - Criando os labels
tk.Label(root, text='Preço:').grid(row=0, column=0)
entry_preco = tk.Entry(root)
entry_preco.grid(row=0, column=1)

tk.Label(root, text='Nome:').grid(row=1, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=1, column=1)

tk.Label(root, text='Quantidade:').grid(row=2, column=0)
entry_quantidade = tk.Entry(root)
entry_quantidade.grid(row=2, column=1)

tk.Label(root, text='Data da Venda').grid(row=3, column=0)
entry_datavenda = tk.Entry(root)
entry_datavenda.grid(row=3, column=1)

tk.Label(root, text='ID para Deletar:').grid(row=4, column=0)
entry_id = tk.Entry(root)
entry_id.grid(row=4, column=1)

# 4 Criando Botão de Inserir Dados
btn_insert = tk.Button(root, text='Inserir Dados', command=insert_data)
btn_insert.grid(row=4, column=9, columnspan=2)

# 4.1 Criando Botão de deletar dados
btn_delete = tk.Button(root, text='Deletar Dados', command=delete_data)
btn_delete.grid(row=5, column=10, columnspan=2)
# Iniciando aplicação
root.mainloop()

# Fechando conexão
conn.close()