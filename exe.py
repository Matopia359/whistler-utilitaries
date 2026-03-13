import tkinter as tk
from tkinter import messagebox, filedialog

# Funcao para adicionar item a lista
def adicionar_item():
    item = entrada.get().strip()
    if item:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(frame_itens, text=item, variable=var)
        checkbox.var = var
        checkbox.pack(anchor='w')
        itens.append(checkbox)
        entrada.delete(0, tk.END)
    else:
        messagebox.showwarning("Atencao", "Digite algo para adicionar!")

# Funcao para remover itens marcados
def remover_concluidos():
    for item in itens[:]:
        if item.var.get():
            item.destroy()
            itens.remove(item)

# Funcao para salvar a lista em arquivo
def salvar_lista():
    caminho = filedialog.asksaveasfilename(defaultextension=".txt",
                                           filetypes=[("Arquivos de texto", "*.txt")])
    if caminho:
        with open(caminho, "w", encoding="utf-8") as f:
            for item in itens:
                status = "1" if item.var.get() else "0"
                f.write(f"{status}|{item.cget('text')}\n")
        messagebox.showinfo("Sucesso", "Lista salva com sucesso!")

# Funcao para abrir lista de arquivo
def abrir_lista():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos de texto", "*.txt")])
    if caminho:
        # Limpa lista atual
        for item in itens[:]:
            item.destroy()
            itens.remove(item)
        # Carrega lista do arquivo
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    status, texto = linha.split("|", 1)
                    var = tk.BooleanVar(value=status=="1")
                    checkbox = tk.Checkbutton(frame_itens, text=texto, variable=var)
                    checkbox.var = var
                    checkbox.pack(anchor='w')
                    itens.append(checkbox)

# Criando a janela principal
janela = tk.Tk()
janela.title("To-Do List")
janela.geometry("300x450")

itens = []

# Entrada e botoes
entrada = tk.Entry(janela, width=25)
entrada.pack(pady=10)

btn_adicionar = tk.Button(janela, text="Adicionar", command=adicionar_item)
btn_adicionar.pack(pady=5)

btn_remover = tk.Button(janela, text="Remover Concluidos", command=remover_concluidos)
btn_remover.pack(pady=5)

btn_salvar = tk.Button(janela, text="Salvar Lista", command=salvar_lista)
btn_salvar.pack(pady=5)

btn_abrir = tk.Button(janela, text="Abrir Lista", command=abrir_lista)
btn_abrir.pack(pady=5)

# Frame com scroll
frame_itens = tk.Frame(janela)
frame_itens.pack(pady=10, fill='both', expand=True)

scrollbar = tk.Scrollbar(frame_itens)
scrollbar.pack(side='right', fill='y')

canvas = tk.Canvas(frame_itens, yscrollcommand=scrollbar.set)
canvas.pack(side='left', fill='both', expand=True)

scrollbar.config(command=canvas.yview)

inner_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor='nw')

def atualizar_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

inner_frame.bind("<Configure>", atualizar_scroll)
frame_itens = inner_frame

janela.mainloop()
